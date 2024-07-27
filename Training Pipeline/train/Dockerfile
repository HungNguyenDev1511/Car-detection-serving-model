FROM tensorflow/tensorflow:2.12.0

#ROM nvcr.io/nvidia/tensorflow:20.12-tf2-py3
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN pip install opencv-python-headless==4.5.3.56
RUN pip install mlflow==2.14.1
RUN pip install tqdm


COPY . /app

WORKDIR /app

# Run mwt.py with the --train argument
CMD ["python", "mwt.py", "--train"]
