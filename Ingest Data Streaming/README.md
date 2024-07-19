The main idea of this step is you use the streaming tool to create many data you want. There are some tool you can use in local for POC which are RabbitMQ, Kafka... and in this Project i used Kafka Flink and send data to PostgreSQL to use. The main idea to develop in this step is you should define the kafka-producer service and use it to send data continuously to PostgresSQL. In Kafka Producer, you can define the message format, the data you want to binding the message and the topic you want to share the message. You can reference this guide to develop: https://docs.confluent.io/cloud/current/connectors/cc-postgresql-sink.html#step-6-check-the-results-in-postgresql

- First you can start the docker compose file (You can skip this step when you run it success in step 1)
- Then, you can access to https://localhost:9021 (9021 is the port of control center kafka)
- Click on the topic tab - for example you can follow like image below
-
![Topic Tab]()