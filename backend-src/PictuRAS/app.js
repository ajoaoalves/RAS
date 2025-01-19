var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const http = require('http'); // HTTP server for socket.io
const { Server } = require('socket.io'); // Socket.io

// MongoDB connection
var mongoose = require('mongoose');
var mongoDB = 'mongodb://mongo-server:27017/projects';  // Updated to use 'mongo' as the service name in Docker Compose
mongoose.connect(mongoDB, { useNewUrlParser: true, useUnifiedTopology: true });

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'Erro de conexão ao MongoDB'));
db.once('open', function () {
  console.log('Conexão ao MongoDB realizada com sucesso');
});

var projectRouter = require('./routes/project');

var app = express();
const server = http.createServer(app); // Create HTTP server
const io = new Server(server); // Initialize socket.io

// Middlewares
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// Routing
app.use('/', projectRouter);

// WebSocket integration with socket.io
io.on('connection', (socket) => {
  console.log('New client connected:', socket.id);

  // Listen for image messages from the ws-gateway
  socket.on('image', async (data) => {
    try {

      const { projectId, imageData } = data;

      if (!projectId || !imageData) {
        console.error('Invalid data received. Missing projectId, imageData.');
        socket.emit('error', { message: 'Invalid data. projectId AND imageData are required.' });
        return;
      }

      console.log(`Received image data for project ID ${data.projectId}`);


      // Save the image URI to the MongoDB (example schema)
      const Project = require('./models/project'); // Your project model
      const project = await Project.findById(data.projectId);

      if (!project) {
        console.error('Project not found:', data.projectId);
        return;
      }
      console.error('Project Found:', data.projectId);

      project.images.push({ uri: data.imageUri });
      // Use the addImage method to upload the image and save the URL in the project
      await project.addImage(imageData, "IMAGEM");

      console.log(`Image saved for project ID ${data.projectId}`);
      socket.emit('ack', { message: 'Image received and saved', projectId: data.projectId });
    } catch (error) {
      console.error('Error saving image:', error.message);
      socket.emit('error', { message: 'Failed to process image', error: error.message });
    }
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});


// Start server on a specific port
const port = process.env.PORT || 3000;
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

module.exports = app;
