const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const axios = require('axios'); // For HTTP communication with Projects Backend

const PORT = process.env.PORT || 8080;
const PROJECTS_BACKEND_URL = 'http://localhost:80/projects';
const PROJECTS_BACKEND_WS_URL = 'http://projects-backend-service:3000'; // Backend WebSocket URL

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


/**
// Handle WebSocket connections from browser

*/
io.on('connection', (socket) => {
    console.log(`New client connected: ${socket.id}`);


    // Handle "save_project" messages
    socket.on('save_project', async (data) => {
        console.log('Received save_project:', data);
        try {
            // Parse the incoming data to extract projectId
            const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
            const projectId = parsedData.projectData._id;

            if (!projectId) {
                throw new Error('Invalid project data: projectId is missing');
            }

            // Forward the request to the Projects Backend Service
            const response = await axios.put(`${PROJECTS_BACKEND_URL}/${projectId}`, { data: parsedData });
            console.log('Forwarded to Projects Backend:', response.data);

            // Map this connection to the project ID for state updates
            connections.set(projectId, socket);

            // Send acknowledgment back to the client
            socket.emit('ack', { message: 'Project save request forwarded', projectId });
        } catch (error) {
            console.error('Error processing request:', error.message);
            socket.emit('error', { message: 'Failed to process request', error: error.message });
        }
    });

    // Handle "run_project" messages
    socket.on('run_project', async (data) => {
        console.log('Received run_project:', data);

        try {
            // Parse the incoming data to extract projectId
            const parsedData = typeof data === 'string' ? JSON.parse(data) : data;
            const projectId = parsedData.projectData._id;

            if (!projectId) {
                throw new Error('Invalid project data: projectId is missing');
            }

            // Forward the request to the Projects Backend Service
            const response = await axios.put(`${PROJECTS_BACKEND_URL}/${projectId}/exec`, { data: parsedData });
            console.log('Forwarded to Projects Backend:', response.data);

            // Map this connection to the project ID for state updates
            connections.set(projectId, socket);

            // Send acknowledgment back to the client
            socket.emit('ack', { message: 'Project run request forwarded', projectId });
        } catch (error) {
            console.error('Error processing request:', error.message);
            socket.emit('error', { message: 'Failed to process request', error: error.message });
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

// Function to connect to the Projects Backend WebSocket
function connectToBackendWebSocket() {
    const backendSocket = require('socket.io-client')(PROJECTS_BACKEND_WS_URL);

    backendSocket.on('connect', () => {
        console.log('Connected to Projects Backend WebSocket');
    });

    // Handle project updates from the backend
    backendSocket.on('project_update', (update) => {
        console.log('Received project update from backend:', update);

        const socket = connections.get(update.projectId);
        if (socket) {
            socket.emit('project_update', { state: update.state, projectId: update.projectId });
        }
    });

    // Handle backend WebSocket disconnection
    backendSocket.on('disconnect', () => {
        console.warn('Projects Backend WebSocket disconnected. Reconnecting...');
        setTimeout(connectToBackendWebSocket, 5000); // Retry connection after 5 seconds
    });

    // Handle backend WebSocket errors
    backendSocket.on('error', (error) => {
        console.error('Error with Projects Backend WebSocket:', error.message);
    });
}

// Start listening for backend updates
connectToBackendWebSocket();

// Start the server
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
