## Base de dados
cd data
docker rm mongoRAS
docker run -d -p 27017:27017 --name mongoRAS mongo
docker cp database.json mongoRAS:/tmp
docker exec mongoRAS mongoimport -d projects -c projects /tmp/database.json --jsonArray

## Correr
cd PictuRAS
npm i
npm start

## Tudo
docker-compose up -d

### Ao fazer alterações
docker-compose down
docker-compose up -d --build
