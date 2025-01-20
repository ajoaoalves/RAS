const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { io: Client } = require('socket.io-client'); // For connecting to Projects WS
const axios = require('axios'); // For HTTP communication with Projects Backend

const PORT = process.env.PORT || 8180;
// const PROJECTS_BACKEND_URL = 'http://projects-api:18018/projects';
const PROJECTS_BACKEND_WS_URL = 'http://projects-api:3000'; // Backend WebSocket URL

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

            console.log(`Added client ${socket.id} to connections map.`);


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

    socket.on('request_images', async (projectId) => {
        try {
            if (!projectId) {
                console.error('Invalid request. Missing projectId.');
                socket.emit('error', { message: 'Invalid request. projectId is required.' });
                return;
            }
            connections.set(projectId, socket);


            console.log(`Received request for images of project ID: ${projectId}`);

            // Request images from the backend WebSocket server
            backendSocket.emit('request_images', { projectId }, (response) => {
                if (response.success && response.images && Array.isArray(response.images)) {
                    console.log(`Successfully retrieved images for project ID: ${projectId}`);

                    // Send each image to the client individually
                    response.images.forEach((image) => {
                        const { contentType, binaryData } = image;
                        socket.emit('image_data', { projectId, contentType, binaryData });
                    });

                    // Send an acknowledgment after all images have been sent
                    socket.emit('images_complete', { message: 'All images sent.', projectId });
                } else {
                    console.error(`Failed to retrieve images for project ID: ${projectId}`);
                    socket.emit('error', { message: response.error || 'Failed to retrieve images from backend.' });
                }
            });
        } catch (error) {
            console.error('Error while requesting images:', error.message);
            socket.emit('error', { message: 'Failed to request images.', error: error.message });
        }
    });


    socket.on('preview_update', (metadata, binaryData) => {
        const { projectId, numTool, contentType } = metadata;

        console.log(`Received preview update for project ${numTool}, Step : ${numTool}`);

        // Retrieve the client socket from the connections map
        const clientSocket = connections.get(projectId);

        if (!clientSocket) {
            console.error(`No client connected for project ID: ${projectId}`);
            return;
        }

        // Send the preview image to the client
        console.log(`Sending preview to client ${clientSocket.id} for project ID: ${projectId}`);
        clientSocket.emit('preview_update', { numTool, contentType }, binaryData);
    });


    socket.on('result', (data) => {
        const { projectId, output } = data;

        console.log(`Received result for project ID: ${projectId}`);

        // Retrieve the client socket from the connections map
        const clientSocket = connections.get(projectId);

        if (!clientSocket) {
            console.error(`No client connected for project ID: ${projectId}`);
            return;
        }

        // Send the result dictionary to the client
        console.log(`Sending result to client ${clientSocket.id} for project ID: ${projectId}`);
        clientSocket.emit('result', { output });
    });

    // Handle client disconnection
    socket.on('disconnect', () => {
        console.log(`Client disconnected: ${socket.id}`);

        // Remove the client from the connections map
        if (connections.has(socket.id)) {
            connections.delete(socket.id);
            console.log(`Removed client ${socket.id} from connections map.`);
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
