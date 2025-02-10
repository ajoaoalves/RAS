Para testar: 

Para construir a imagem: `docker build -t api-gateway .`

Para correr a imagem na porta 8080:`docker run -p 8080:8080 api-gateway`

Para ver o ID do container a correr: `docker ps`

Entrar dentro do container: `docker exec -it <id> sh`

Dentro do container correr o:`node client_test.js` 