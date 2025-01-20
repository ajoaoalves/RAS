var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const http = require('http'); // HTTP server for socket.io
const { Server } = require('socket.io'); // Socket.io

// MongoDB connection
var mongoose = require('mongoose');
var mongoDB = 'mongodb://mongo-server:27017/users';  // Updated to use 'mongo' as the service name in Docker Compose
mongoose.connect(mongoDB, { useNewUrlParser: true, useUnifiedTopology: true });

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'Erro de conexão ao MongoDB'));
db.once('open', function () {
  console.log('Conexão ao MongoDB realizada com sucesso');
});

var userRouter = require('./routes/user');

var app = express();
const server = http.createServer(app); // Create HTTP server
const io = new Server(server); // Initialize socket.io

// Middlewares
app.use(logger('dev'));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// Routing
app.use('/', userRouter);

app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.jsonp(JSON.stringify(err));
});

module.exports = app;
