    # How-to Guide
![Pipeline Serving](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/e86947c5-5e25-4b0b-917d-2b78275dad5f)

That is a Project about Serving one model using Modelmesh Kserve and using technique multiple training you can follow all components to see all pipelines The idea of this pipeline will be described below:
- Step 1: Ingest Data from the end user and send directly to PostgreSQL. I use Kafka to send data to PostgreSQL, ready for training in Step 2
- Step 2: In this step, I use all data in PostgreSQL for the training job and use Tensorflow Job and K8s to create multiple Vmware for training, the result will be the weight file after training and you can use this for Serving Step. The Idea in this step is, that the data is countinuously ingested into the database and you can use a CICD tool like Jenkins or something like that to conduct continuously the continuous job
- Step 3: In this step, I use the model file in the training step to serve, should be converted to onnx model platform and I can serve to Modelmesh