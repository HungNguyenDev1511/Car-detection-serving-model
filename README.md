
# 🚕 **Car detection pipeline**
Many companies are currently applying AI technology for vehicle recognition in buildings to better manage traffic. Our vehicle recognition application uses Modelmesh Kserve, TensorFlow Job distributed training, Kafka, and CI/CD technologies to effectively detect vehicle


# 🚀 **Challenge**
This project faced several challenges including ensuring data consistency and scalability during ingestion, managing resources and synchronization in distributed training, automating CI/CD pipelines, converting and deploying models efficiently, ensuring data privacy and security, optimizing performance, and handling the complexities of debugging and troubleshooting in a distributed system.

# 📕 Table Of Contents
- 🌟 [System Architecture](#System-architecture)
- 📁 [Repository Structure](#repository-structure)
- 🔍 [How to Guide](#how-to-guide)

## 🌟 System Architecture
![Pipeline Serving](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/diagram.gif)


## 📁 Repository Structure
 ```
📦 
├─ Jenkinsfile
├─ README.md
├─ api
│  ├─ README.md
│  ├─ car-detection-runtime
│  │  └─ triton-servingruntime.yaml
│  ├─ deployments
│  │  └─ triton-isvc.yaml
│  ├─ model_repo
│  │  └─ yolov8n_car
│  │     ├─ 1
│  │     │  └─ model.onnx
│  │     └─ config.pbtxt
│  ├─ models
│  │  └─ model.h5
│  ├─ requirements.txt
│  └─ utils
│     ├─ .env
│     ├─ classes.py
│     ├─ triton_client.py
│     └─ upload_model.py
├─ docker-compose.yml
├─ kubeflow_pipeline
│  ├─ README.md
│  ├─ mlflow
│  │  └─ Dockerfile
│  └─ train
│     ├─ Dockerfile
│     ├─ build.sh
│     ├─ debug.ipynb
│     ├─ mwt.py
│     ├─ mwt.yaml
│     ├─ nets
│     │  └─ nn.py
│     ├─ utils
│     │  ├─ config.py
│     │  ├─ dataset.py
│     │  └─ util.py
│     └─ weights
│        ├─ model.h5
│        └─ model_s.h5
└─ streaming
   ├─ Dockerfile
   ├─ README.md
   ├─ docker-compose.yml
   ├─ kafka_connector
   │  └─ connect-timescaledb-sink.json 
   ├─ produce_json.py
   └─ run.sh
```

## 🔍 How to Guide

- Step 1: Ingest Data 
``` shell
 cd streaming
 ```
 Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/tree/refactor/Ingest%20Data%20Streaming) for thís step
- Step 2: Trainning 
``` shell
 cd kubeflow_pipeline
 ```
 Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/tree/refactor/Training%20Pipeline) for thís step
- Step 3: Serving
``` shell
 cd api
 ```
Read [Readme.md](https://github.com/HungNguyenDev1511/Car-detection-serving-model/tree/refactor/Inference%20Model%20Modelmesh%20) for thís step
