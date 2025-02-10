var Project = require('../models/project')
const { v4: uuidv4 } = require('uuid');

module.exports.list = function(){
    return Project.find().sort({nome: 1}).exec()
}

module.exports.listUser = function(userId){
    return Project.find({user_id: userId}).exec()
}

module.exports.findById = function(id){
    return Project.findOne({_id: id}).exec()
}

module.exports.insert = function(projeto){
    projeto._id = uuidv4();
    return Project.create(projeto)
}

module.exports.updateProject = function(id, projeto){
    return Project.updateOne({_id:id},projeto)
}

module.exports.deleteProject = function(id){
    return Project.deleteOne({_id:id})
}
