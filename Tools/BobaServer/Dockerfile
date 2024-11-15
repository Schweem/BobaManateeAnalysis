FROM python:3.9-slim-buster

# YOUR ENV var for mongo URI here, you cant use mine 

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files into the container
COPY requirements.txt requirements.txt
COPY bobabackend.py bobabackend.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose the port for flask
EXPOSE 5000

# Run the API
CMD ["python", "bobabackend.py"]
