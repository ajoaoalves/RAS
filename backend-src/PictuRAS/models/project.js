var mongoose = require('mongoose');

var parametersSchema = new mongoose.Schema({
    name: String,
    value: { type: mongoose.Schema.Types.Mixed } 
}, { _id: false });

var toolSchema = new mongoose.Schema({
    _id: String,
    procedure: String,
    parameters: { type: [parametersSchema], required: false }
  }, { _id: false });

var imageSchema = new mongoose.Schema({
    _id: String,
    uri: String
}, { _id: false }); // Desativa o _id automático dos subdocumentos

var projectSchema = new mongoose.Schema({
    _id: String,
    name: String,
    user_id: String,
    images: [imageSchema],
    tools : [toolSchema] 
}, { versionKey: false });

module.exports = mongoose.model('projects', projectSchema);
