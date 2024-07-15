    # How-to Guide
![abc](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/e86947c5-5e25-4b0b-917d-2b78275dad5f)

## Prerequisites

### Install kustomize
[Kustomize](https://kubectl.docs.kubernetes.io/) is another tool to install applications on k8s beside Helm. Let's install it first.

```shell
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/
```

### Install modelmesh-serving

Pay attention that `minikf` uses Kubernetes version 1.16, which is not suitable for the latest release of the modelmesh-serving repository, which is `0.11.1`.

Clone the repository. I did this step already for you so you don't have to redo this. I just want to show you what I did.
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
![modelmesh-serving](./images/modelmesh-serving-installation.png)

## Quickstart

Port-forward `minio` service so you can access it locally
```shell
kubectl port-forward svc/minio -p 9000:9000 -n modelmesh-serving
```

Assume that your `minio` pod is `minio-5f894ffd9-v27zp`, use the following commands to obtain `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` for signing in `minio` and uploading your objects.

```shell
kubectl get po minio-676b8dcf45-nw2zw -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_ACCESS_KEY") | .value'

kubectl get po minio-676b8dcf45-nw2zw -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_SECRET_KEY") | .value'
```

You can see that in my case, `MINIO_ACCESS_KEY` is `AKIAIOSFODNN7EXAMPLE`, and `MINIO_SECRET_KEY` is `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`.
![minio-credentials](./images/minio-credentials.png).
Open browser to access localhost:9000 - that is the endpoint of MINIO

In this project we work with triton so we need to upload the models and config by file config.pbtxt in folder model_repo\yolov8n_car and upload the folder yolov8nx_car in to onnx on MINIO. The structure of folder in onnx folder on MINIO you should do like this 

Run the following command to have a start model
```shellk get p
kubectl apply -f deployments/triton-isvc.yaml
kubectl apply -f intrusion-detection-runtime/triton-servingruntime.yaml
```

To see whether our service is ready, run the following command
```shell
kubectl get isvc
```
, it should take several minutes for our service to be `READY`. If not, please check logs of the container `mm` in the pod corresponding to `mlserver` as follows

```shell
kubectl logs modelmesh-serving-mlserver-0.x-68d7dcb75d-5m5lg -c mm
```

To make a prediction, do the following steps:

1. Port-forward `modelmesh-serving` service
    ```shell
    kubectl port-forward --address 0.0.0.0 service/modelmesh-serving 8008 -n modelmesh-serving
    ```
2. Test your newly created modelmesh-serving service
    ```shell
    python utils/quickstart/client.py
    ```

    **Note:** Don't forget to replace your cookie ;)
