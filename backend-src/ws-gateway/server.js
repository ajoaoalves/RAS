const WebSocket = require('ws');
const express = require('express');

const PORT = process.env.PORT || 8080;

// Create an Express app
const app = express();
app.get('/', (req, res) => res.send('WebSocket Gateway is running...'));
app.listen(PORT, () => console.log(`HTTP server listening on port ${PORT}`));

// Create a WebSocket Server
const wss = new WebSocket.Server({ port: 8081 });

console.log(`WebSocket server listening on port 8081`);

wss.on('connection', (ws) => {
    console.log('New WebSocket connection');

    ws.on('message', (message) => {
        const decodedMessage = message.toString(); // Convert buffer to string
        console.log('Received:', decodedMessage);
        ws.send(`Echo: ${decodedMessage}`); // Echo the decoded message back
    });
    ws.on('close', () => {
        console.log('WebSocket connection closed');
    });
});
