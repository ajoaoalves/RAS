var express = require('express');
var router = express.Router();
var User = require("../controllers/user");

/* Obtener todos los usuarios */
router.get('/users', function (req, res) {
    User.list()
        .then(data => res.jsonp(data))
        .catch(error => res.status(500).jsonp(error));
});

/* Obtener un usuario por ID */
router.get('/users/:id', function (req, res) {
    User.findById(req.params.id)
        .then(data => res.jsonp(data))
        .catch(error => res.status(500).jsonp(error));
});

/* Registrar un nuevo usuario */
router.post('/users', async (req, res) => {
    console.log(req.body)
    User.insert(req.body)
        .then(data => res.status(201).jsonp(data))
        .catch(erro => res.status(523).jsonp(erro))
});

/* Actualizar datos de un usuario */
router.put('/users/:id', function (req, res) {
    console.log(req.body);
    User.updateUser(req.params.id, req.body)
        .then(data => res.status(200).jsonp(data))
        .catch(error => res.status(500).jsonp(error));
});

/* Eliminar un usuario */
router.delete('/users/:id', function (req, res) {
    console.log(req.body);
    User.deleteUser(req.params.id)
        .then(data => res.status(200).jsonp(data))
        .catch(error => res.status(500).jsonp(error));
});

/* Autenticación de usuario (Login) */
router.post('/users/login', async function (req, res) {
    try {
        const { emailOrUsername, password } = req.body;
        const user = await User.authenticate(emailOrUsername, password);
        res.status(200).jsonp(user);
    } catch (error) {
        res.status(401).jsonp({ error: error.message });
    }
});

module.exports = router;
