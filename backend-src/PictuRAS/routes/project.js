var express = require('express');
var router = express.Router();
var Project = require("../controllers/project")
const sendToQueue = require('../controllers/send_to_queue');

/* GET home page. */
router.get('/projects', function(req, res, next) {
  Project.list()
  .then(data => res.jsonp(data))
  .catch(erro => res.jsonp(erro))
});

router.get('/projects/:id', function(req, res) {
  Project.findById(req.params.id)
  .then(data => res.jsonp(data))
  .catch(erro => res.jsonp(erro))
});

router.post('/projects', function(req, res) {
  console.log(req.body)
  Project.insert(req.body)
  .then(data => res.status(201).jsonp(data))
  .catch(erro => res.status(523).jsonp(erro))
});

router.put('/projects/:id/exec', function (req, res) {
  console.log(req.body);

  Project.updateProject(req.params.id, req.body)
    .then(async (data) => {
      // Enviar o projeto atualizado para a fila
      try {
        await sendToQueue(req.body); // `data` contém o projeto atualizado
        console.log('Projeto enviado para a fila com sucesso.');
        res.status(201).jsonp(data);
      } catch (queueError) {
        console.error('Erro ao enviar projeto para a fila:', queueError);
        res.status(201).jsonp({
          message: 'Projeto atualizado, mas não foi possível enviar para a fila.',
          project: data,
        });
      }
    })
    .catch((erro) => res.status(524).jsonp(erro));
});

router.put('/projects/:id', function(req, res) {
  console.log(req.body)
  Project.updateProject(req.params.id, req.body)
  .then(data => res.status(201).jsonp(data))
  .catch(erro => res.status(524).jsonp(erro))
});

router.delete('/projects/:id', function(req, res) {
  console.log(req.body)
  Project.deleteProject(req.params.id, req.body)
  .then(data => res.status(200).jsonp(data))
  .catch(erro => res.status(525).jsonp(erro))
});

module.exports = router;
