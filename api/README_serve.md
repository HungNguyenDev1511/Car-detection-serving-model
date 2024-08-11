# How-to Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
   - [Install kustomize](#install-kustomize)
   - [Install modelmesh-serving](#install-modelmesh-serving)
2. [Getting Started](#getting-started)

---

## Prerequisites
use GKE version 1.29
### Install kustomize
[Kustomize](https://kubectl.docs.kubernetes.io/) is another tool to install applications on k8s beside Helm. Let's install it first.

```shell
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/
```

### Install modelmesh-serving

Clone the repo as follows.
```shell
RELEASE=release-0.9
git clone -b $RELEASE --depth 1 --single-branch https://github.com/kserve/modelmesh-serving.git
cd modelmesh-serving
```

Create a new namespace and install modelmesh-serving
```shell
kubectl create namespace modelmesh-serving
./scripts/install.sh --namespace modelmesh-serving --quickstart

```

After several minutes, you should see the following output
![modelmesh-serving](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/modelmesh-serving-installation.png)

## Getting Started

Port-forward `minio` service so you can access it locally
```shell
kubectl port-forward svc/minio 9000:9000 -n modelmesh-serving
```

Assuming your minio pod is minio-5f894ffd9-v27zp, use the following commands to obtain the MINIO_ACCESS_KEY and MINIO_SECRET_KEY for signing in to minio and uploading your objects

```shell
kubectl get po minio-676b8dcf45-nw2zw -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_ACCESS_KEY") | .value'

kubectl get po minio-676b8dcf45-nw2zw -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_SECRET_KEY") | .value'
```

You can see that in my case, `MINIO_ACCESS_KEY` is `AKIAIOSFODNN7EXAMPLE`, and `MINIO_SECRET_KEY` is `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`.
![minio-credentials](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/minio-credentials.png).

Access localhost:9000 to open MINIO and upload the model to the MINIO bucket. The structure for storing our ONNX model and the config.pbtxt file should look like this. Remember to use the model we trained in the previous step for serving. The format should be ONNX, so please convert the weight file to ONNX before uploading it to the bucket
![Screenshot from 2024-05-11 17-01-13](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/adc4b65c-a51c-4e64-9a1a-377f680810ed)
![Screenshot from 2024-05-11 17-01-19](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/8461cdc0-1fcd-491e-9b24-8d8d9b5bfc58)

Run the following command to upload the folder, or you can upload it manually if preferred 
``` shell
python api/upload_model_to_minio.py
```

Run the following command to have a deploy onnx model
```shell
kubectl get p
kubectl apply -f deployments/triton-isvc.yaml
kubectl apply -f deployments/triton-servingruntime.yaml
```

To see whether our service is ready, run the following command
```shell
kubectl get isvc
```
You can see that is false
![Error](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/false_modelmesh_deploy.png)

, it should take several minutes for our service to be `READY`. If not, please check logs of the container `mm` in the pod corresponding to `triton` as follows

kubectl descrbe pods and try to see error 
```shell
kubectl describe pod modelmesh-serving-triton-2.x-6c4978d6db-5k59z
```
![Error Log Pod Describe](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/error_log_pod.png)


If our service changes to 'READY', everything may be okay.

![Result](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/result.png)
![Result Inference Service](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/isvc.png)

just resolve one by one error first

To make a prediction, do the following steps:

1. Port-forward `modelmesh-serving` service
    ```shell
    kubectl port-forward --address 0.0.0.0 service/modelmesh-serving 8008 -n modelmesh-serving
    ```
2. Test your newly created modelmesh-serving service
    ```shell
    python api/triton_client.py
    ```
