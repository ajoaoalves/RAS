const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const axios = require('axios'); // For HTTP communication with Projects Backend

const PORT = process.env.PORT || 8080;
const PROJECTS_BACKEND_URL = 'http://projects-backend-service:3000/projects'; // Replace with the actual backend service URL

// Create an Express app and HTTP server
const app = express();
const server = http.createServer(app);

// Create a Socket.IO server
const io = new Server(server, {
    cors: {
        origin: '*', // Allow all origins (configure for production)
    },
});

// Maintain a mapping of Socket.IO connections to projects
const connections = new Map();

// Serve a basic HTTP endpoint
app.get('/', (req, res) => res.send('Socket.IO WebSocket Gateway is running...'));

// Handle WebSocket connections
io.on('connection', (socket) => {
    console.log(`New client connected: ${socket.id}`);

    // Handle "run_project" messages
    socket.on('run_project', async (data) => {
        console.log('Received run_project:', data);

        try {
            // Forward the request to the Projects Backend Service
            const response = await axios.post(PROJECTS_BACKEND_URL, { projectId: data.projectId });
            console.log('Forwarded to Projects Backend:', response.data);

            // Map this connection to the project ID for state updates
            connections.set(data.projectId, socket);

            // Send acknowledgment back to the client
            socket.emit('ack', { message: 'Project run request forwarded', projectId: data.projectId });
        } catch (error) {
            console.error('Error forwarding request:', error.message);
            socket.emit('error', { message: 'Failed to process request' });
        }
    });

    // Handle client disconnection
    socket.on('disconnect', () => {
        console.log(`Client disconnected: ${socket.id}`);

        // Clean up the mapping
        for (const [projectId, clientSocket] of connections.entries()) {
            if (clientSocket === socket) {
                connections.delete(projectId);
            }
        }
    });
});

// Function to handle updates from the Projects Backend Service
async function listenToProjectUpdates() {
    console.log('Listening for project updates...');

    // Simulate listening for updates (replace this with RabbitMQ, SSE, or WebSocket)
    setInterval(async () => {
        try {
            // Fetch project state updates from the backend service
            const response = await axios.get(`${PROJECTS_BACKEND_URL}/updates`);
            const updates = response.data;

            // Send updates to the corresponding clients
            updates.forEach((update) => {
                const socket = connections.get(update.projectId);
                if (socket) {
                    socket.emit('project_update', { state: update.state, projectId: update.projectId });
                }
            });
        } catch (error) {
            console.error('Error fetching project updates:', error.message);
        }
    }, 5000); // Check for updates every 5 seconds (adjust as needed)
}

// Start listening for project updates
listenToProjectUpdates();

// Start the server
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
