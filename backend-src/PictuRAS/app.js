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
  socket.on('image', async (data, callback) => {
    try {
      const { projectId, imageData } = data;

      if (!projectId || !imageData) {
        console.error('Invalid data received. Missing projectId or imageData.');
        const errorResponse = { success: false, error: 'Invalid data. projectId and imageData are required.' };
        if (callback) callback(errorResponse); // Send error response
        return;
      }

      console.log(`Received image data for project ID ${projectId}`);

      // Save the image URI to the MongoDB (example schema)
      const Project = require('./models/project'); // Your project model
      const project = await Project.findById(projectId);

      if (!project) {
        console.error('Project not found:', projectId);
        const errorResponse = { success: false, error: 'Project not found.' };
        if (callback) callback(errorResponse); // Send error response
        return;
      }

      // Save the image data using addImageFromBrowser
      await project.addImageFromBrowser(imageData, projectId);

      console.log(`Image saved for project ID ${projectId}`);

      // Send success response
      const successResponse = { success: true, message: 'Image saved successfully.', projectId };
      if (callback) callback(successResponse);

      // Emit acknowledgment to the original socket
      socket.emit('ack', { message: 'Image received and saved', projectId });
    } catch (error) {
      console.error('Error saving image:', error.message);
      const errorResponse = { success: false, error: `Failed to process image: ${error.message}` };
      if (callback) callback(errorResponse); // Send error response
      socket.emit('error', { message: 'Failed to process image.', error: error.message });
    }
  });

  // Listen for preview_update event
  socket.on('preview_update', async (data, callback) => {
    try {
      const { projectId, key } = data;

      if (!projectId || !key) {
        console.error('Invalid data received. Missing projectId or key.');
        const errorResponse = { success: false, error: 'Invalid data. projectId and key are required.' };
        if (callback) callback(errorResponse); // Send error response
        return;
      }

      console.log(`Downloading preview image for project ID ${projectId} with key ${key}`);

      // Find the project to ensure it exists
      const Project = require('./models/project'); // Your project model
      const project = await Project.findById(projectId);

      if (!project) {
        console.error('Project not found:', projectId);
        const errorResponse = { success: false, error: 'Project not found.' };
        if (callback) callback(errorResponse); // Send error response
        return;
      }

      // Download the image from S3
      const { data: imageBuffer, contentType } = await project.downloadImageFromS3(`src/${projectId}/${key}`);

      console.log(`Preview image downloaded for project ID ${projectId}`);

      // Send the binary image data directly to the client
      if (callback) callback({ success: true, contentType });
      socket.emit('preview_update', { projectId, contentType }, imageBuffer); // Send the binary data
    } catch (error) {
      console.error('Error downloading preview image:', error.message);
      const errorResponse = { success: false, error: `Failed to download preview image: ${error.message}` };
      if (callback) callback(errorResponse); // Send error response
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
