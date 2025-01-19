var express = require('express');
var router = express.Router();
var Project = require("../controllers/project")
const { executeProject } = require('../controllers/execution');

/* GET home page. */
router.get('/projects', function (req, res, next) {
  Project.list()
    .then(data => res.jsonp(data))
    .catch(erro => res.jsonp(erro))
});


router.get('/users/:userId/projects', function (req, res) {
  Project.listUser(req.params.userId)
    .then(data => res.jsonp(data))
    .catch(erro => res.jsonp(erro))
}
);
router.get('/users/:userId/projects/:id', function (req, res) {
  Project.findById(req.params.id)
    .then(data => res.jsonp(data))
    .catch(erro => res.jsonp(erro))
});

router.post('/users/:userId/projects', function (req, res) {
  console.log(req.body)
  Project.insert(req.body)
    .then(data => res.status(201).jsonp(data))
    .catch(erro => res.status(523).jsonp(erro))
});
router.put('/users/:userId/projects/:id/exec', function (req, res) {
  console.log(req.body);
  Project.findById(req.params.id)
    .then(async (data) => {
      if (!data) {
        return res.status(404).json({ error: 'Projeto não encontrado.' });
      }

      // Enviar o projeto atualizado para a fila
      try {
        await executeProject(data); // Usar o resultado do findById
        console.log('Projeto enviado para a fila com sucesso.');
        res.status(201).jsonp(data);
      }
      catch (queueError) {
        console.error('Erro ao enviar projeto para a fila:', queueError);
        res.status(201).jsonp({
          message: 'Projeto atualizado, mas não foi possível enviar para a fila.',
          project: data,
        });
      }
    })
    .catch((erro) => res.status(524).jsonp(erro));
});

router.put('/users/:userId/projects/:id', function (req, res) {
  console.log(req.body)
  Project.updateProject(req.params.id, req.body)
    .then(data => res.status(201).jsonp(data))
    .catch(erro => res.status(524).jsonp(erro))
});

router.delete('/users/:userId/projects/:id', function (req, res) {
  console.log(req.body)
  Project.deleteProject(req.params.id, req.body)
    .then(data => res.status(200).jsonp(data))
    .catch(erro => res.status(525).jsonp(erro))
});

module.exports = router;
