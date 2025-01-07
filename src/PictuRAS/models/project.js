var mongoose = require('mongoose')

var projectSchema = new mongoose.Schema({
    _id: String,
    name: String,
    user_id: String,
}, {versionKey: false})

var imageSchema = new mongoose.Schema({
    _id: String,
    project_id: String,
    uri: String
})

module.exports = mongoose.model('projects',projectSchema)