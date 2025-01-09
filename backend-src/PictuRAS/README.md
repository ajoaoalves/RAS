## Base de dados
docker rm mongoRAS
docker run -d -p 27017:27017 --name mongoRAS mongo
docker cp database.json mongoRAS:/tmp
docker exec mongoRAS mongoimport -d projects -c projects /tmp/database.json --jsonArray

## Correr
cd PictuRAS
npm i
npm start