
# 🚕 **Car detection pipeline**
Many companies are currently applying AI technology for vehicle recognition in buildings to better manage traffic. Our vehicle recognition application uses Modelmesh Kserve, TensorFlow Job distributed training, Kafka, and CI/CD technologies to effectively detect vehicle


# 🚀 **Challenge**
This project faced several challenges including ensuring data consistency and scalability during ingestion, managing resources and synchronization in distributed training, automating CI/CD pipelines, converting and deploying models efficiently, ensuring data privacy and security, optimizing performance, and handling the complexities of debugging and troubleshooting in a distributed system.

# 📕 Table Of Contents
- 🌟 [System Architecture](#System-architecture)
- 📁 [Repository Structure](#repository-structure)
- 🔍 [How to Guide](#how-to-guide)

## 🌟 System Architecture
![systemoverview](images/architecutre_overview.png)

The pipeline consists of two main components:

- **Data Pipeline**: This part of the system handles the ingestion, preprocessing, and feature extraction of car detection data. It includes steps like loading the dataset, performing preprocessing tasks, and extracting relevant features using tools like Apache Flink and Redis.
- **Training and Deployment Pipeline**: The training and deployment pipeline focuses on the model development and deployment processes. It includes steps like saving the trained model and artifacts, evaluating the model, and deploying the model using tools like MLflow, Jenkins, and Kubernetes.

Certainly! Based on the comprehensive image you've provided, here's a suggested structure for your project's README file:

# Car Detection Pipeline

This project presents a robust car detection pipeline that leverages various technologies and tools to streamline the process from data acquisition to model deployment.


## 📁 Repository Structure
```
📦
├─ .env                      # Environment variables used across the project
├─ Jenkinsfile               # Configuration for a Jenkins CI/CD pipeline
├─ README.md                 # General project documentation
├─ api                       # Contains code related to the API layer
│  ├─ README_serve.md        # Documentation for the API serving component
│  ├─ triton_client.py       # Code for interacting with the Triton Inference Server
│  └─ upload_model_to_minio.py # Script to upload the trained model to Minio storage
├─ constants.py              # Shared constants and configurations used across the project
├─ deployments               # Kubernetes deployment configurations
│  ├─ mwt.yaml               # Deployment for the Multi-Worker Training (MWT) component
│  ├─ triton-isvc.yaml       # Deployment for the Triton Inference Service
│  └─ triton-servingruntime.yaml # Deployment for the Triton Inference Server runtime
├─ distributed_training      # Code and configuration for distributed training
│  ├─ Dockerfile             # Dockerfile for the distributed training component
│  ├─ README_distributed.md  # Documentation for the distributed training component
│  ├─ build.sh               # Script to build the distributed training Docker image
│  ├─ mwt.py                 # Main logic for the Multi-Worker Training component
│  ├─ nets                   # Neural network architecture definitions
│  │  └─ nn.py               # Neural network model implementation
│  ├─ test                   # Test configuration for the distributed training
│  │  └─ test.yaml           # Test deployment configuration
│  ├─ utils                  # Utility functions for the distributed training
│  │  ├─ config.py           # Configuration handling for the distributed training
│  │  ├─ dataset.py          # Dataset-related utilities
│  │  └─ image_utils.py      # Image processing utilities
│  └─ weights                # Folder containing a pre-trained model
│     └─ model.h5            # Saved weights for the pre-trained model
├─ docker-compose.yml        # Docker Compose configuration for the entire project
├─ images                    # Folder for storing project-related images
├─ mlflow                    # Code and configuration for the MLflow component
│  └─ Dockerfile             # Dockerfile for the MLflow component
├─ model_repo                # Repository for storing the trained model
│  └─ yolov8n_car            # Folder for the YOLOv8 car detection model
│     ├─ 1                   # Version 1 of the model
│     │  └─ model.onnx       # ONNX format of the trained model
│     └─ config.pbtxt        # Triton Inference Server configuration for the model
├─ notebooks                 # Folder for Jupyter Notebooks (likely for debugging/exploration)
│  └─ debug.ipynb            # Sample Jupyter Notebook for debugging
├─ requirements.txt          # Python dependencies for the project
└─ streaming                 # Code and configuration for the data streaming component
   ├─ Dockerfile             # Dockerfile for the streaming component
   ├─ README_streaming.md    # Documentation for the streaming component
   ├─ docker-compose.yml     # Docker Compose configuration for the streaming component
   ├─ kafka_connector        # Configuration for the Kafka connector
   │  └─ connect-timescaledb-sink.json # Kafka connector configuration for TimescaleDB sink
   ├─ produce.py             # Script to produce sample data for the streaming component
   └─ run.sh                 # Script to run the streaming component
```

## 🔍 How to Guide

- Step 1: In the ingestion step, we gather data from the internet for training. Here are some advanced techniques for using Kafka in training:
1. Scalability: Kafka supports horizontal scaling, allowing you to handle increasing data volumes by adding more brokers to the Kafka cluster.
2. High Performance: Kafka can handle millions of events per second with low latency, thanks to its design of segment-based storage and efficient use of memory buffers.
3. Consistency: Kafka uses mechanisms for data replication and distribution, ensuring data consistency and recovery in case of failures.
``` shell
 cd streaming
 ```
 Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/streaming/README_streaming.md) for this step
- Step 2: Training. To train the model for serving, here are some advanced techniques for distributed training:
1. Gradient Accumulation: Reducing synchronization frequency by accumulating gradients.
2. Mixed Precision Training: Using lower precision for faster computations and less memory usage.
3. Communication Optimization: Reducing communication overhead with techniques like Ring-AllReduce.
``` shell
 cd distributed_training
 ```
 Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/distributed_training/README_distributed.md) for this step
- Step 3: Serving. Use the model trained in the previous step for inference. Here are some advanced techniques
1. Scalability: ModelMesh supports scaling of model serving infrastructure to handle varying loads and large volumes of requests.
2. Multi-Model Support: It can manage and serve multiple models simultaneously, allowing for a more flexible deployment strategy.
3. Efficient Resource Utilization: ModelMesh optimizes the use of resources by dynamically allocating them based on the demand for different models.
``` shell
 cd api
 ```
Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/api/README_serve.md) for this step
