## Base de dados
docker rm mongoEW
docker run -d -p 27017:27017 --name mongoEW mongo
docker cp db.json mongoEW:/tmp
docker exec mongoEW mongoimport -d contratos -c contratos /tmp/contratos.json --jsonArray

## Correr
cd PictuRAS
npm i
npm start