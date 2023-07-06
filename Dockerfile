FROM python:3.9

# Set up working directory
WORKDIR /jplag

# Install Maven and other required packages
RUN apt-get update && apt-get install -y maven wget

# Download JPlag
RUN wget https://github.com/jplag/JPlag/releases/download/v4.3.0/jplag-4.3.0-jar-with-dependencies.jar

# Install Flask and Gunicorn
RUN pip3 install flask==2.0.3 gunicorn==20.1.0

# Copy the source code
COPY app.py .
# We can remove this lines. It's only dummy code to make some tests
COPY code1.cpp .
COPY code2.cpp .

# Expose the container port
EXPOSE 5000

# Start the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
