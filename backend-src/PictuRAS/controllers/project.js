var Project = require('../models/project')

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
    return Project.create(projeto)
}

module.exports.updateProject = function(id, projeto){
    return Project.updateOne({_id:id},projeto)
}

module.exports.deleteProject = function(id){
    return Project.deleteOne({_id:id})
}
