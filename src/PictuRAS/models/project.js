var mongoose = require('mongoose');

var imageSchema = new mongoose.Schema({
    _id: String,
    uri: String
}, { _id: false }); // Desativa o _id automático dos subdocumentos

var projectSchema = new mongoose.Schema({
    _id: String,
    name: String,
    user_id: String,
    images: [imageSchema] 
}, { versionKey: false });

module.exports = mongoose.model('projects', projectSchema);
