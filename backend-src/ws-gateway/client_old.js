const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8081');

ws.on('open', () => {
    console.log('Connected to WebSocket server');

    // Send a test message to the server
    const testMessage = JSON.stringify({ type: 'run_project', projectId: '12345' });
    console.log('Sending:', testMessage);
    ws.send(testMessage);

});

ws.on('message', (message) => {
    console.log('Received:', message.toString()); // Convert buffer to string
});

ws.on('close', () => {
    console.log('Disconnected from server');
});
