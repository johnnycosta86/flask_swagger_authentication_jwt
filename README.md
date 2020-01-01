# flask_swagger_authentication_jwt
This is an example of Rest endpoint using python Flask with JWT authentication via SWAGGER


-- Create docker image

docker build -t flask_swagger_authentication_jwt:latest .

-- Run docker image

docker run -d -p 8080:8080 flask_swagger_authentication_jwt

-- List all docker containers running

docker container ls

-- Run bash inside docker container 

docker container exec -it container_id_flask_swagger_authentication_jwt bash
