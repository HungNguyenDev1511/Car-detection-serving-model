FROM python:3.9

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt && \
    rm requirements.txt

COPY --chown=${USER} ./model.py /opt/
ENV PYTHONPATH=/opt/
WORKDIR /opt/

# # environment variables to be compatible with ModelMesh Serving
# #  these can also be set in the ServingRuntime, but this is recommended for
# #  consistency when building and testing
# ENV MLSERVER_MODELS_DIR=/models/_mlserver_models/ \
#     MLSERVER_GRPC_PORT=8001 \
#     MLSERVER_HTTP_PORT=8002 \
#     MLSERVER_METRICS_PORT=8082 \
#     MLSERVER_LOAD_MODELS_AT_STARTUP=false \
#     MLSERVER_DEBUG=true \
#     MLSERVER_MODEL_PARALLEL_WORKERS=0 \
#     MLSERVER_MODEL_NAME=dummy-model

# RUN mkdir -p /models/_triton_models \ 
#     chmod 777 /models/_triton_models \ 
#     exec tritonserver
#           "--model-repository=/models/_triton_models"
#           "--model-control-mode=explicit"
#           "--strict-model-config=false"
#           "--strict-readiness=false"
#           "--allow-http=true"
#           "--allow-sagemaker=false"
#           '\

RUN mkdir -p /models/_triton_models
RUN chmod 777 /models/_triton_models

ARG model-repository=/models/_triton_models \
    model-control-mode=explicit \ 
    strict-model-config=false \ 
    trict-readiness=false \ 
    allow-http=true \
    allow-sagemaker=false


# # With this setting, the implementation field is not required in the model
# # settings which eases integration by allowing the built-in adapter to generate
# # a basic model settings file
# ENV MLSERVER_MODEL_IMPLEMENTATION=model.CustomMLModel

CMD tritonserver $model-repository