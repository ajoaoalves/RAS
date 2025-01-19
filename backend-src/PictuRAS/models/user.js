var mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid');

var userSchema = new mongoose.Schema({
    _id: { type: String, default: uuidv4 }, // UUID como ID
    name: { type: String, required: true },
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    type: { type: String, enum: ['admin', 'user'], default: 'user' }
}, { versionKey: false });

// Hash de la contraseña antes de guardarla
userSchema.pre('save', async function (next) {
    if (!this.isModified('password')) return next();

    try {
        const salt = await bcrypt.genSalt(10);
        this.password = await bcrypt.hash(this.password, salt);
        next();
    } catch (error) {
        next(error);
    }
});

// Método para comparar contraseñas
userSchema.methods.comparePassword = async function (candidatePassword) {
    return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('users', userSchema);
