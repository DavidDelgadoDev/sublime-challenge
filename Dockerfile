# Pull base image
FROM python:3.10

# Set environment variables
ENV DockerHOME=/home/app/sublime-challenge
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_PORT=5432
ENV DATABASE_HOST=pg-db
ENV DATABASE_PASSWORD='password'
ENV DATABASE_USER=postgres
ENV DATABASE_NAME=postgres

RUN mkdir -p $DockerHOME  

# Set work directory
WORKDIR $DockerHOME  

# Install dependencies
RUN pip install --upgrade pip
COPY . $DockerHOME  

RUN pip install -r requirements.txt
RUN pip install gunicorn


EXPOSE 8000  

# Run the application 
CMD ["gunicorn", "sublime.wsgi:application", "--bind", "0.0.0.0:8000"]