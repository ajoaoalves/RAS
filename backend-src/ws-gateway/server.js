const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { io: Client } = require('socket.io-client'); // For connecting to Projects WS
const axios = require('axios'); // For HTTP communication with Projects Backend

const PORT = process.env.PORT || 8180;
const PROJECTS_BACKEND_URL = 'http://localhost:18018/projects';
const PROJECTS_BACKEND_WS_URL = 'http://localhost:3000'; // Backend WebSocket URL

// Create an Express app and HTTP server
const app = express();
const server = http.createServer(app);

// Create a Socket.IO server
const io = new Server(server, {
    cors: {
        origin: '*', // Allow all origins (configure for production)
    },
});

// Create a WebSocket client for the Projects WebSocket server
const backendSocket = Client(PROJECTS_BACKEND_WS_URL);

// Maintain a mapping of Socket.IO connections to projects
const connections = new Map();

// Serve a basic HTTP endpoint
app.get('/', (req, res) => res.send('Socket.IO WebSocket Gateway is running...'));

/**
 * Handle WebSocket connections from browser
 */
io.on('connection', (socket) => {
    console.log(`New client connected: ${socket.id}`);

    // Handle "image" event from the client
    socket.on('image', async (data) => {
        try {
            const { projectId, imageData } = data;

            if (!projectId || !imageData) {
                console.error('Invalid data received. Missing projectId or imageData.');
                socket.emit('error', { message: 'Invalid data. projectId and imageData are required.' });
                return;
            }

            console.log(`Received image for project ID: ${projectId}`);

            // Forward the image data to the Projects WebSocket server
            backendSocket.emit('image', { projectId, imageData }, (response) => {
                if (response.success) {
                    console.log(`Image successfully sent to Projects WS for project ID: ${projectId}`);
                    socket.emit('ack', { message: 'Image processed successfully by Projects WS', projectId });
                } else {
                    console.error(`Error from Projects WS: ${response.error || 'Unknown error'}`);
                    socket.emit('error', { message: response.error || 'Failed to process image in Projects WS' });
                }
            });
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

// Handle connection to the Projects WebSocket server
backendSocket.on('connect', () => {
    console.log('Connected to Projects WebSocket server');
});

backendSocket.on('disconnect', () => {
    console.log('Disconnected from Projects WebSocket server');
});

backendSocket.on('error', (error) => {
    console.error('Error in Projects WebSocket connection:', error.message);
});

// Start the server
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
