var User = require('../models/user');

module.exports.list = function () {
    return User.find().sort({ name: 1 }).exec();
};

module.exports.findById = function (id) {
    return User.findOne({ _id: id }).exec();
};

module.exports.findByUsername = function (username) {
    return User.findOne({ username: username }).exec();
};

module.exports.insert = function (user) {
    return User.create(user);
};

module.exports.updateUser = function (id, user) {
    return User.updateOne({ _id: id }, user);
};

module.exports.deleteUser = function (id) {
    return User.deleteOne({ _id: id });
};

// Autenticación de usuario (Login)
module.exports.authenticate = async function (emailOrUsername, password) {
    let user = await User.findOne({ $or: [{ email: emailOrUsername }, { username: emailOrUsername }] }).exec();
    if (!user) throw new Error('User not found');

    const isMatch = await user.comparePassword(password);
    if (!isMatch) throw new Error('Invalid credentials');

    return user;
};
