const { io } = require('socket.io-client');

// Connect to the Socket.IO server
const socket = io('http://localhost:8080');

// Handle connection open event
socket.on('connect', () => {
    console.log('Connected to WebSocket server');

    // Send a "run_project" request to the server
    const projectRequest = { type: 'run_project', projectId: '516d3862-2a87-4e04-baf8-5bf640b94838' };
    console.log('Sending:', projectRequest);
    socket.emit('run_project', projectRequest);
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
