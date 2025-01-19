const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const axios = require('axios'); // For HTTP communication with Projects Backend

const PORT = process.env.PORT || 8180;
const PROJECTS_BACKEND_URL = 'http://localhost:18018/projects';
const PROJECTS_BACKEND_WS_URL = 'http://localhost:3000/'; // Backend WebSocket URL

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

    socket.on('image', async (data) => {
        try {
            const { projectId, imageData } = data;

            if (!projectId || !imageData) {
                console.error('Invalid data received. Missing projectId or imageData.');
                socket.emit('error', { message: 'Invalid data. projectId and imageData are required.' });
                return;
            }

            console.log(`Received image for project ID: ${projectId}`);

            // Forward the image data to the projects backend
            const response = await axios.post(`${PROJECTS_BACKEND_URL}/projects/${projectId}/images`, {
                imageData, // Forward the image data
            });

            console.log(`Image sent to projects backend for project ID: ${projectId}`);
            socket.emit('ack', { message: 'Image processed successfully', projectId });
        } catch (error) {
            console.error('Error processing image:', error.message);
            socket.emit('error', { message: 'Failed to process image', error: error.message });
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
