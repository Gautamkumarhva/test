FROM python:3.11
WORKDIR /app

# Install the application dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY . .
EXPOSE 5000

# Set the environment variable for Flask
#ENV FLASK_APP=app.py

# Run the Flask application
#source: https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]