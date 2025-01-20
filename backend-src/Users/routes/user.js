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
router.post('/users', function (req, res) {
    console.log(req.body);
    User.insert(req.body)
        .then(data => res.status(201).jsonp(data))
        .catch(error => res.status(500).jsonp(error));
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
router.post('/users/login', async (req, res) => {
    const { email, password } = req.body;
    console.log("Dados recebidos:", email, password); // Verificar os dados recebidos

    try {
        const user = await User.findByEmail( email );
        console.log("Usuário encontrado:", user); // Verificar se encontrou o usuário

        if (user && user.password === password) { // Comparação simples
            console.log("Login bem-sucedido!");
            res.json(user);
        } else {
            console.log("Credenciais inválidas");
            res.status(401).json({ message: 'Credenciais inválidas' });
        }
    } catch (error) {
        console.error("Erro no servidor:", error);
        res.status(500).json({ message: 'Erro no servidor', error });
    }
});


module.exports = router;
