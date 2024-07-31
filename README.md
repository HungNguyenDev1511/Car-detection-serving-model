
![Pipeline Serving](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/e86947c5-5e25-4b0b-917d-2b78275dad5f)

# :taxi: **Car detection pipeline**
Many companies are currently applying AI technology for vehicle recognition in buildings to better manage traffic. Our vehicle recognition application uses Modelmesh Kserve, TensorFlow Job distributed training, Kafka, and CI/CD technologies to effectively detect vehicle


# 🚀 **Challenge**
This project faced several challenges including ensuring data consistency and scalability during ingestion, managing resources and synchronization in distributed training, automating CI/CD pipelines, converting and deploying models efficiently, ensuring data privacy and security, optimizing performance, and handling the complexities of debugging and troubleshooting in a distributed system.

# 📕 Table Of Contents
- 🌟 [System Architecture](#system-architecture)
- 📁 [Repository Structure](#repository-structure)
- 🔍 [How to Guide](#how-to-guide)

# 🌟 System Architecture


# 📁 Repository Structure
# 🔍 How to Guide


That is a Project about Serving one model using Modelmesh Kserve and using technique multiple training you can follow all components to see all pipelines The idea of this pipeline will be described below:
- Step 1: Ingest Data from the end user and send directly to PostgreSQL. I use Kafka to send data to PostgreSQL, ready for training in Step 2
- Step 2: In this step, I use all data in PostgreSQL for the training job and use Tensorflow Job and K8s to create multiple Vmware for training, the result will be the weight file after training and you can use this for Serving Step. The Idea in this step is, that the data is countinuously ingested into the database and you can use a CICD tool like Jenkins or something like that to conduct continuously the continuous job
- Step 3: In this step, I use the model file in the training step to serve, should be converted to onnx model platform and I can serve to Modelmesh