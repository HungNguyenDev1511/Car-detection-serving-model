FROM tensorflow/tensorflow:2.12.0

# Update the package list
RUN apt-get update

# Install necessary packages
RUN apt install -y libgl1-mesa-glx

# Install Python dependencies
RUN pip install opencv-python-headless==4.5.3.56
RUN pip install mlflow==2.14.1
RUN pip install tqdm

# Copy the application code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Run mwt.py with the --train argument
CMD ["python", "mwt.py", "--train"]
