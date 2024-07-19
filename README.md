    # How-to Guide
![abc](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/e86947c5-5e25-4b0b-917d-2b78275dad5f)

that is Project about Serving one model using Modelmesh Kserve and use technique multiple train you can follow all component to see all pipeline
The idea of this pipeline will be describe below:
Step 1: Ingest Data from end user send direct to PostgreSql. I use Kafka to send data to PostgreSql, ready for trainning in Step 2
Step 2: In this step i use all data in PostgreSql for Trainning job, use Tensorflow Job to and K8s for create multiple Vmware to trainning, the result will be the weight file after trainning and you can use this to Serving Step. The Idea in this step is, the data countinuously ingest to database and you can use CICD tool like Jenkins or something like that to conduct continuously the trainning job
Step 3: In this step i use the model file in trainning step to serving, in this step should be convert to onnx model platform and i can serving to Modelmesh