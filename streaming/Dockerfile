FROM python:3.8-slim

# Copy app handler code

# Install dependencies
RUN pip3 install kafka-python==2.0.2
RUN pip3 install avro==1.11.1
RUN pip3 install pandas==1.5.1
RUN pip3 install pyarrow==10.0.1
RUN pip3 install python-schema-registry-client==2.4.1
RUN pip3 install pymongo==4.5.0

# Copy app handler code
COPY produce.py produce.py
# COPY kafka_producer/generate_schemas.py generate_schemas.py
# COPY run.sh .
# # Uncomment this to generate a random schema
# RUN chmod +x /run.sh && ./run.sh generate_schemas

CMD [ "python", "-u", "produce.py", "--mode", "setup", "--bootstrap_servers", "broker:29092"]