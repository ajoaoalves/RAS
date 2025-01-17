const WebSocket = require('ws');
const express = require('express');
const axios = require('axios'); // For HTTP communication with Projects Backend

const PORT = process.env.PORT || 8080;
const PROJECTS_BACKEND_URL = 'http://projects-backend-service:3000/projects'; // Replace with the actual backend service URL

// Create an Express app
const app = express();
app.get('/', (req, res) => res.send('WebSocket Gateway is running...'));
app.listen(PORT, () => console.log(`HTTP server listening on port ${PORT}`));

// Create a WebSocket Server
const wss = new WebSocket.Server({ port: 8081 });

console.log(`WebSocket server listening on port 8081`);

// Maintain a mapping of WebSocket connections to projects
const connections = new Map();

wss.on('connection', (ws) => {
    console.log('New WebSocket connection');

    ws.on('message', async (message) => {
        const decodedMessage = message.toString(); // Convert buffer to string
        console.log('Received:', decodedMessage);

        try {
            // Parse the message (assuming it's JSON)
            const data = JSON.parse(decodedMessage);

            if (data.type === 'run_project') {
                // Forward the request to the Projects Backend Service
                const response = await axios.post(PROJECTS_BACKEND_URL, { projectId: data.projectId });
                console.log('Forwarded to Projects Backend:', response.data);

                // Map this connection to the project ID for state updates
                connections.set(data.projectId, ws);

                // Send acknowledgment back to the WebSocket client
                ws.send(JSON.stringify({ type: 'ack', message: 'Project run request forwarded', projectId: data.projectId }));
            } else {
                ws.send(JSON.stringify({ type: 'error', message: 'Unknown message type' }));
            }
        } catch (error) {
            console.error('Error handling message:', error);
            ws.send(JSON.stringify({ type: 'error', message: 'Failed to process request' }));
        }
    });

    ws.on('close', () => {
        console.log('WebSocket connection closed');
        // Optionally clean up the mapping
        for (const [projectId, connection] of connections.entries()) {
            if (connection === ws) {
                connections.delete(projectId);
            }
        }
    });
});

// Function to handle updates from the Projects Backend Service
async function listenToProjectUpdates() {
    // Example: Use long polling, SSE, or WebSocket to listen for updates
    console.log('Listening for project updates...');

    // Replace this with the actual subscription method (e.g., RabbitMQ, polling, or WebSocket)
    setInterval(async () => {
        try {
            // Fetch project state updates from the backend service
            const response = await axios.get(`${PROJECTS_BACKEND_URL}/updates`);
            const updates = response.data;

            // Send updates to the corresponding WebSocket clients
            updates.forEach((update) => {
                const ws = connections.get(update.projectId);
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'update', state: update.state, projectId: update.projectId }));
                }
            });
        } catch (error) {
            console.error('Error fetching project updates:', error);
        }
    }, 5000); // Check for updates every 5 seconds (adjust as needed)
}

// Start listening for project updates
listenToProjectUpdates();
