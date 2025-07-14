# Build the Docker image with the calculated date and specified version
$tag = "home-kokoro-api"

Write-Output "Generating requirements.txt: $tag"
pip freeze > requirements.txt
Start-Sleep -Milliseconds 100

Write-Output "Deleting Docker image with tag: $tag"
docker rmi -f $tag .
Start-Sleep -Milliseconds 100

Write-Output "Building Docker image with tag: $tag"
docker build -t $tag .
Start-Sleep -Milliseconds 100

Write-Output "Running Docker image with tag: $tag"
docker run -d --name $tag -p 3090:3090 docker.io/library/$tag
Start-Sleep -Milliseconds 100
Write-Output "Script completed successfully with image tag: $tag"