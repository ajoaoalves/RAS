const { io } = require('socket.io-client');

// Connect to the Socket.IO server
const socket = io('http://localhost:8080');

// Handle connection open event
socket.on('connect', () => {
    console.log('Connected to WebSocket server');

    const projectRequest = {
        _id: "516d3862-2a87-4e04-baf8-5bf640b94838",
        name: "Fotografias de tudo",
        user_id: "0e6d0ce7-08c1-4de9-b7ff-82554bad32d8",
        images: [
            {
                _id: "d3011aad-7c20-4f4a-8191-7749325a49ae",
                uri: "https://s3.picturas.com/d3011aad-7c20-4f4a-8191-7749325a49ae.jpeg"
            }
        ],
        tools: [
            {
                _id: "a5c27b9d-1261-4291-ae34-4b70877a3e58",
                procedure: "Rotação",
                parameters: [
                    {
                        name: "Ângulo",
                        value: 90
                    }
                ]
            }
        ]
    };

    console.log('Sending:', projectRequest);
    socket.emit('save_project', projectRequest);
});

// Handle acknowledgment from the server
socket.on('ack', (data) => {
    console.log('Acknowledgment from server:', data);
});

// Handle project updates from the server
socket.on('project_update', (update) => {
    console.log('Received project update:', update);
});

// Handle errors
socket.on('error', (error) => {
    console.error('Error from server:', error);
});

// Handle disconnection
socket.on('disconnect', () => {
    console.log('Disconnected from WebSocket server');
});
