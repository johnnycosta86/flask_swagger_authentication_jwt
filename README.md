# flask_swagger_authentication_jwt
This is an example of Rest endpoint using python Flask with JWT authentication via SWAGGER


-- Create docker image

docker build -t crypto_api:latest .

-- Run docker image

docker run -d -p 8080:8080 crypto-api

-- List all docker containers running

docker container ls

-- Run bash inside docker container 

docker container exec -it container_id_crypto_api bash