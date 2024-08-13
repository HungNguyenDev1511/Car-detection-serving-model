
# 🚕 **Car detection pipeline**
Many companies are currently applying AI technology for vehicle recognition in buildings to better manage traffic. Our vehicle recognition application uses Modelmesh Kserve, TensorFlow Job distributed training, Kafka, and CI/CD technologies to effectively detect vehicle


# 🚀 **Challenge**
This project faced several challenges including ensuring data consistency and scalability during ingestion, managing resources and synchronization in distributed training, automating CI/CD pipelines, converting and deploying models efficiently, ensuring data privacy and security, optimizing performance, and handling the complexities of debugging and troubleshooting in a distributed system.

# 📕 Table Of Contents
- 🌟 [System Architecture](#System-architecture)
- 📁 [Repository Structure](#repository-structure)
- 🔍 [How to Guide](#how-to-guide)

## 🌟 System Architecture
![Pipeline Serving](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/diagram_pipe.gif)


## 📁 Repository Structure
```
📦 
├─ .env
├─ Jenkinsfile
├─ README.md
├─ api 
│  ├─ README_serve.md
│  ├─ triton_client.py
│  └─ upload_model_to_minio.py
├─ constants.py
├─ deployments // Serve the model and deploy the pod for training
│  ├─ mwt.yaml
│  ├─ triton-isvc.yaml
│  └─ triton-servingruntime.yaml
├─ distributed_training // logic for distributed training 
│  ├─ Dockerfile
│  ├─ README_distributed.md
│  ├─ build.sh
│  ├─ mwt.py
│  ├─ nets
│  │  └─ nn.py
│  ├─ test
│  │  └─ test.yaml
│  ├─ utils
│  │  ├─ config.py
│  │  ├─ dataset.py
│  │  └─ image_utils.py
│  └─ weights
│     └─ model.h5
├─ docker-compose.yml
├─ images
├─ mlflow
│  └─ Dockerfile
├─ model_repo // model for serve
│  └─ yolov8n_car
│     ├─ 1
│     │  └─ model.onnx
│     └─ config.pbtxt
├─ notebooks
│  └─ debug.ipynb
├─ requirements.txt
└─ streaming // ingest data for training
   ├─ Dockerfile
   ├─ README_streaming.md
   ├─ docker-compose.yml
   ├─ kafka_connector
   │  └─ connect-timescaledb-sink.json 
   ├─ produce.py
   └─ run.sh
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
