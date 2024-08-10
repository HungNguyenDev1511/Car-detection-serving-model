# Table of Contents
1. [Introduction](#introduction)
2. [Dataset Setup](#dataset-setup)
   - [Downloading the Dataset](#downloading-the-dataset)
   - [Folder Structure](#folder-structure)
3. [Kafka and Flink Setup](#kafka-and-flink-setup)
   - [Starting Docker Compose](#starting-docker-compose)
   - [Accessing Kafka Control Center](#accessing-kafka-control-center)
4. [Viewing Kafka Topics](#viewing-kafka-topics)
   - [Accessing the Topics Tab](#accessing-the-topics-tab)
   - [Viewing Topic Messages](#viewing-topic-messages)
5. [Adding Kafka Connector](#adding-kafka-connector)
6. [Verifying Data in PostgreSQL](#verifying-data-in-postgresql)
7. [Note](#note)

---

# Introduction
The main idea of this step is to use a streaming tool to generate the data you need. For a proof of concept (POC), you can use tools like RabbitMQ or Kafka locally. In this project, I used Kafka with Flink to send data to PostgreSQL. The key task in this step is to define the Kafka producer service and use it to continuously send data to PostgreSQL. In the Kafka producer, you can specify the message format, bind the data to the message, and choose the topic for sharing the message. You can refer to this guide for development: [Confluent PostgreSQL Sink](https://docs.confluent.io/cloud/current/connectors/cc-postgresql-sink.html#step-6-check-the-results-in-postgresql).

# Dataset Setup

## Downloading the Dataset
- First, download the dataset for streaming from the following link: [Dataset Link](https://drive.google.com/drive/folders/12ncEAoWT_kwuPT8YRdFysqgS54XJwre7?usp=drive_link)

## Folder Structure
- The structure of the folder will be like this:

<div align="center">
  <img src="https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/structure_data.png" alt="Structure Data Folder">
</div>

# Kafka Flink Setup

## Starting Docker Compose
- You can start the Docker Compose file (You can skip this step if you successfully completed it in step 1).

## Accessing Kafka Control Center
- Then, you can access `https://localhost:9021` (9021 is the port for the Kafka Control Center).

# Viewing Kafka Topics

## Accessing the Topics Tab
- Click on the `Topics` tab—for example, you can follow the steps shown in the image below:

![Topic Tab](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/topic_tab.png)

## Viewing Topic Messages
- Click on the topic name (in this case, `image 0`) to view the messages:

![Message](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/messenger.png)

# Adding Kafka Connector
- You need to add the connector to Kafka so that the messages can be sent to PostgreSQL. I've provided an example configuration in the `connect-timescaledb-sink.json` file.

![Connector](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/connector.png)

# Verifying Data in PostgreSQL
Finally, you can verify it by opening PostgreSQL and querying the data with SQL for training.

# Note
- Remember to validate that the connector is properly configured before proceeding to the data verification step.
