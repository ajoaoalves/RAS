const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8081');

ws.on('open', () => {
    console.log('Connected to WebSocket server');
    ws.send('Hello from client!');
});

ws.on('message', (message) => {
    console.log('Received:', message.toString()); // Convert buffer to string
});

ws.on('close', () => {
    console.log('Disconnected from server');
});
