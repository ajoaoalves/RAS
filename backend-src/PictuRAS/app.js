var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

// MongoDB connection
var mongoose = require('mongoose');
var mongoDB = 'mongodb://mongo:27017/projects';  // Updated to use 'mongo' as the service name in Docker Compose
mongoose.connect(mongoDB, { useNewUrlParser: true, useUnifiedTopology: true });

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'Erro de conexão ao MongoDB'));
db.once('open', function () {
  console.log('Conexão ao MongoDB realizada com sucesso');
});

var projectRouter = require('./routes/project');

var app = express();

// Middlewares
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// Routing
app.use('/', projectRouter);

// Start server on a specific port
var port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

module.exports = app;
