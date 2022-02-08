# ref https://github.com/tebeka/pythonwise/blob/master/docker-miniconda/Dockerfile
FROM ubuntu:18.04

# System packages
RUN apt-get update && apt-get install -y curl

# Install miniconda to /miniconda


# Setup application
#COPY imgsrv.py /
#ENTRYPOINT ["/miniconda/bin/python", "/imgsrv.py"]
#EXPOSE 8080
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "./main.py", "runserver", "0.0.0.0:8000"]