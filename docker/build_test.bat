@echo off
setlocal

set "name=template_python"
rem Change the current working directory to the directory of the batch script
cd /d %~dp0
cd ..

docker build -t rpakishore/%name% :latest . -f .\Dockerfile

:: Run a Docker container in detached mode with specified volumes and port mapping
docker run ^
    -d --name %name% ^                          :: Assigns the name to the container
    -v ..\.streamlit:/root/.streamlit ^         :: Mounts .streamlit directory from host to container
    -v ..\streamlit:/app ^                      :: Mounts streamlit directory from host to container
    -v ..\logs:/app/.venv/lib/python3.12/logs ^ :: Mounts logs directory from host to container
    -p 9000:8501 ^                              :: Maps port 9000 on the host to port 8501 in the container
    rpakishore/%name%                           :: Specifies the Docker image name

endlocal

start "" "http://localhost:9000"