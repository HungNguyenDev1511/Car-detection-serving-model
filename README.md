
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
│  ├─ README.md
│  └─ utils
│     ├─ triton_client.py
│     └─ upload_model_to_minio.py
├─ constants.py
├─ deployments
│  ├─ mwt.yaml
│  ├─ triton-isvc.yaml
│  └─ triton-servingruntime.yaml
├─ distributed_trainning
│  ├─ Dockerfile
│  ├─ build.sh
│  ├─ mwt.py
│  ├─ nets
│  │  └─ nn.py
│  ├─ utils
│  │  ├─ config.py
│  │  ├─ dataset.py
│  │  └─ image_utils.py
│  └─ weights
│     └─ model.h5
├─ docker-compose.yml
├─ images
├─ kubeflow_pipeline
│  └─ README.md
├─ mlflow
│  └─ Dockerfile
├─ model_repo
│  └─ yolov8n_car
│     ├─ 1
│     │  └─ model.onnx
│     └─ config.pbtxt
├─ notebooks
│  └─ debug.ipynb
├─ requirements.txt
└─ streaming
   ├─ Dockerfile
   ├─ README.md
   ├─ docker-compose.yml
   ├─ kafka_connector
   │  └─ connect-timescaledb-sink.json 
   ├─ produce.py
   └─ run.sh
```

## 🔍 How to Guide

- Step 1: Ingest Data 
``` shell
 cd streaming
 ```
 Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/README_streaming.md) for this step
- Step 2: Trainning 
``` shell
 cd distributed_trainning
 ```
 Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/README_distributed.md) for this step
- Step 3: Serving
``` shell
 cd api
 ```
Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/README_serve.md) for this step
