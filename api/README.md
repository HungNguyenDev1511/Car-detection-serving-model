# Deployment Pipeline Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
   - [Install kustomize](#install-kustomize)
   - [Install modelmesh-serving](#install-modelmesh-serving)
2. [Deployment Pipeline Overview](deployment-pipeline-overview)
3. [Getting Started](#getting-started)
4. [Making Prediction](#making-prediction)

---

## Prerequisites

Before getting started, ensure that your environment meets the following prerequisites:

- GKE Version: Use GKE version 1.29

### Install kustomize

[Kustomize](https://kubectl.docs.kubernetes.io/) is an alternative tool to Helm for installing applications on Kubernetes. Install it by running the following commands:

```shell
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/
```

### Install modelmesh-serving

Clone the modelmesh-serving repository:

```shell
RELEASE=release-0.9
git clone -b $RELEASE --depth 1 --single-branch https://github.com/kserve/modelmesh-serving.git
cd modelmesh-serving
```

Create a new namespace and install modelmesh-serving:

```shell
kubectl create namespace modelmesh-serving
./scripts/install.sh --namespace modelmesh-serving --quickstart

```

After a few minutes, you should see the following output:

![modelmesh-serving](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/modelmesh-serving-installation.png)

## Deployment Pipeline Overview

The following diagram provides an overview of the deployment pipeline, detailing each step from model optimization to deployment and scaling.

[deploymentOverview](images/deployment_pipeline.png)

### Key Components:

1. Model Optimization (ONNX):
    - Optimizes the model for serving, converting it into ONNX format.

2. Model Testing:

    - Runs tests to ensure that the optimized model meets the necessary performance and accuracy criteria.

3. Runtime Containerization:

    - Packages the model into a containerized runtime environment.

4. Ingest Serving-Model to S3:

    - The containerized model is uploaded to an S3-compatible storage, such as MinIO.
5. Deployment and Scaling:

    - The model is deployed and scaled using Kubernetes (K8s), managed through `kubectl`.

6. Model Serving API:

    - The deployed model is accessible via an API, allowing users to make predictions.

## Getting Started

### Port-forward the `MinIO` Service

To access MinIO locally, use the following command:

```shell
kubectl port-forward svc/minio 9000:9000 -n modelmesh-serving
```

### Access MinIO Credentials

Obtain the `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` required to sign in and upload your models to MinIO:

```shell
kubectl get po minio-676b8dcf45-nw2zw -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_ACCESS_KEY") | .value'

kubectl get po minio-676b8dcf45-nw2zw -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_SECRET_KEY") | .value'
```

You can see that in my case, `MINIO_ACCESS_KEY` is `AKIAIOSFODNN7EXAMPLE`, and `MINIO_SECRET_KEY` is `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`.

![minio-credentials](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/minio-credentials.png).

Access localhost:9000 to open MINIO and upload the model to the MINIO bucket. The structure for storing our ONNX model and the config.pbtxt file should look like this. Remember to use the model we trained in the previous step for serving. The format should be ONNX, so please convert the weight file to ONNX before uploading it to the bucket

![Screenshot from 2024-05-11 17-01-13](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/adc4b65c-a51c-4e64-9a1a-377f680810ed)

![Screenshot from 2024-05-11 17-01-19](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/8461cdc0-1fcd-491e-9b24-8d8d9b5bfc58)


### Upload Model to MinIO:

You can manually upload the model or use the following script:
``` shell
python api/upload_model_to_minio.py
```

### Deploy the ONNX Model:

Deploy the model using the following commands:

```shell
kubectl get p
kubectl apply -f deployments/triton-isvc.yaml
kubectl apply -f deployments/triton-servingruntime.yaml
```

### Verify the Service Readiness:

Check if the service is ready:

```shell
kubectl get isvc
```

You can see that is `false`:

![Error](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/false_modelmesh_deploy.png)

It should take several minutes for our service to become READY. 

If it doesn’t, please check the logs of the `mm` container in the pod corresponding to triton using the following command to check logs:

```shell
kubectl describe pod modelmesh-serving-triton-2.x-6c4978d6db-5k59z
```

![Error Log Pod Describe](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/error_log_pod.png)


Once the service is ready, you should see the following result:

![Result](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/result.png)
![Result Inference Service](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/isvc.png)


## Making Prediction:

To make a prediction, follow these steps:

1. Port-forward `modelmesh-serving` service
    ```shell
    kubectl port-forward --address 0.0.0.0 service/modelmesh-serving 8008 -n modelmesh-serving
    ```
2. Test your newly created modelmesh-serving service
    ```shell
    python api/triton_client.py
    ```
