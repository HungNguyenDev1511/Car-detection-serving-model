
# 🚕 **Car detection pipeline**
Many companies are currently applying AI technology for vehicle recognition in buildings to better manage traffic. Our vehicle recognition application uses Modelmesh Kserve, TensorFlow Job distributed training, Kafka, and CI/CD technologies to effectively detect vehicle


# 🚀 **Challenge**
This project faced several challenges including ensuring data consistency and scalability during ingestion, managing resources and synchronization in distributed training, automating CI/CD pipelines, converting and deploying models efficiently, ensuring data privacy and security, optimizing performance, and handling the complexities of debugging and troubleshooting in a distributed system.

# 📕 Table Of Contents
- 🌟 [System Architecture](#system-architecture)
- 📁 [Repository Structure](#repository-structure)
- 🔍 [How to Guide](#how-to-guide)

# 🌟 System Architecture
![Pipeline Serving](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/e86947c5-5e25-4b0b-917d-2b78275dad5f)


# 📁 Repository Structure
📦 Car-detection-serving-model
├─ Inference Model Modelmesh 
│  ├─ README.md
│  ├─ car-detection-runtime
│  │  └─ triton-servingruntime.yaml
│  ├─ deployments
│  │  └─ triton-isvc.yaml
│  ├─ model_repo
│  │  └─ yolov8n_car
│  │     ├─ 1
│  │     │  └─ model.onnx
│  │     └─ config.pbtxt
│  ├─ requirements.txt
│  ├─ triton.yaml
│  └─ utils
│     ├─ triton_client.py
│     └─ upload_model.py
├─ Ingest Data Streaming
│  ├─ Dockerfile
│  ├─ README.md
│  ├─ docker-compose.yml
│  ├─ kafka_connector
│  │  └─ connect-timescaledb-sink.json 
│  ├─ produce_json.py
│  └─ run.sh
├─ README.md
├─ Training Pipeline
│  ├─ Jenkinsfile
│  ├─ README.md
│  ├─ docker-compose.yml
│  ├─ mlflow
│  │  └─ Dockerfile
│  └─ train
│     ├─ Dockerfile
│     ├─ build.sh
│     ├─ debug.ipynb
│     ├─ mwt.py
│     ├─ mwt.yaml
│     ├─ nets
│     │  └─ nn.py
│     ├─ utils
│     │  ├─ config.py
│     │  ├─ dataset.py
│     │  └─ util.py
│     └─ weights
│        ├─ model.h5
│        └─ model_s.h5
└─ image
   ├─ Messenger.png
   ├─ Mlflow _modelregistry.png
   ├─ PipelineAllcode.png
   ├─ Strategy.png
   ├─ StructureTrainning.png
   ├─ Structure_Data.png
   ├─ Topic_tab.png
   ├─ add_credential.png
   ├─ add_credential_dockerhub.png
   ├─ add_token_dockerhub.png
   ├─ bus.jpg
   ├─ check_request_github_jenkins.png
   ├─ connector.png
   ├─ generate_token_docker_hub.png
   ├─ get_token_github.png
   ├─ github_tokens.png
   ├─ instal_docker_jenkins.png
   ├─ install_docker_success.png
   ├─ isvc.png
   ├─ jenkins_container.png
   ├─ jenkins_portal.png
   ├─ jenkins_ui.png
   ├─ ngrok.png
   ├─ ngrok_forwarding.png
   ├─ password_jenkins.png
   ├─ result.png
   ├─ result_connect_jenkins_github.png
   ├─ result_push_dockerhub.png
   ├─ result_train_pod.png
   ├─ strategy_scope.png
   ├─ train_process.png
   ├─ ui_build_jenkins.png
   ├─ validate_connect_repo.png
   └─ webhook_github.png


# 🔍 How to Guide


That is a Project about Serving one model using Modelmesh Kserve and using technique multiple training you can follow all components to see all pipelines The idea of this pipeline will be described below:
- Step 1: Ingest Data from the end user and send directly to PostgreSQL. I use Kafka to send data to PostgreSQL, ready for training in Step 2
- Step 2: In this step, I use all data in PostgreSQL for the training job and use Tensorflow Job and K8s to create multiple Vmware for training, the result will be the weight file after training and you can use this for Serving Step. The Idea in this step is, that the data is countinuously ingested into the database and you can use a CICD tool like Jenkins or something like that to conduct continuously the continuous job
- Step 3: In this step, I use the model file in the training step to serve, should be converted to onnx model platform and I can serve to Modelmesh