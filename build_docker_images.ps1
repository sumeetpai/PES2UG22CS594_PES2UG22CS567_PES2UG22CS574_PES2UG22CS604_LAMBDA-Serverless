# Build Python function base image
cd docker/python
docker build -t function-python-base .
cd ../..

# Build JavaScript function base image
cd docker/node
docker build -t function-javascript-base .
cd ../..

Write-Host "Docker images built successfully!" 