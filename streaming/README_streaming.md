The main idea of this step is to use a streaming tool to generate the data you need. For a proof of concept (POC), you can use tools like RabbitMQ or Kafka locally. In this project, I used Kafka with Flink to send data to PostgreSQL. The key task in this step is to define the Kafka producer service and use it to continuously send data to PostgreSQL. In the Kafka producer, you can specify the message format, bind the data to the message, and choose the topic for sharing the message. You can refer to this guide for development: https://docs.confluent.io/cloud/current/connectors/cc-postgresql-sink.html#step-6-check-the-results-in-postgresql.

- First, download the dataset for streaming from the following link: https://drive.google.com/drive/folders/12ncEAoWT_kwuPT8YRdFysqgS54XJwre7?usp=drive_link
- the Structure of folder will be like this 

<div align="center">
  <img src="https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/structure_data.png" alt="Structure Data Folder">
</div>
 
- You can start the docker-compose file (You can skip this step when you run it successfully in step 1)
- Then, you can access https://localhost:9021 (9021 is the port for the Kafka Control Center)
- Click on the 'Topics' tab—for example, you can follow the steps shown in the image below
![Topic Tab](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/topic_tab.png)
- Click on the topic name (in this case, image 0) to view the messages
![Messege](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/messenger.png)
# Note
- You need to add the connector to Kafka so that the messages can be sent to PostgreSQL. I've provided an example configuration in the connect-timescaledb-sink.json file
![Connector] (https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/connector.png)

Finally, you can verify it by opening PostgreSQL and querying the data with SQL for training