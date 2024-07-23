The main idea of this step is you use the streaming tool to create many data you want. There are some tools you can use locally for POC which are RabbitMQ, Kafka... and in this Project, I used Kafka Flink and sent data to PostgreSQL to use. The main idea to develop in this step is you should define the kafka-producer service and use it to send data continuously to PostgreSQL. In Kafka Producer, you can define the message format, the data you want to bind the message, and the topic you want to share the message. You can reference this guide to develop: https://docs.confluent.io/cloud/current/connectors/cc-postgresql-sink.html#step-6-check-the-results-in-postgresql

- First, you should download the Data set for the training job from here: 
- https://drive.google.com/drive/folders/12ncEAoWT_kwuPT8YRdFysqgS54XJwre7?usp=drive_link
- the Structure of folder will be like this:
- S
![Structure Data Folder ](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/Structure_Data.png)
 
- You can start the docker-compose file (You can skip this step when you run it successfully in step 1)
- Then, you can access https://localhost:9021 (9021 is the port of control center Kafka)
- Click on the topic tab - for example, you can follow like image below
-
![Topic Tab](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/Topic_tab.png)
- Click on the topic name (in this case image 0) you can see the message
-
![Messege](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/Messenger.png)
# Note
- You need to add the connector to Kafka so the message can be sent to Postgres. I add the example config in the connect-timescaledb-sink.json file
![Connector] (https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/connector.png)

Finally, you can check it by opening PostgresSQl and calling the data from SQL to train