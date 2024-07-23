# How-to Guide

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
kubectl port-forward svc/minio 9000:9000 -n modelmesh-serving
```

Assume that your `minio` pod is `minio-5f894ffd9-v27zp`, use the following commands to obtain `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` for signing in `minio` and uploading your objects.

```shell
kubectl get po minio-676b8dcf45-nw2zw -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_ACCESS_KEY") | .value'

kubectl get po minio-676b8dcf45-nw2zw -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_SECRET_KEY") | .value'
```

You can see that in my case, `MINIO_ACCESS_KEY` is `AKIAIOSFODNN7EXAMPLE`, and `MINIO_SECRET_KEY` is `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`.
![minio-credentials](./images/minio-credentials.png).

Acess to localhost:9000 to access MINIO upload model to MINIO bucket structure of storage our ONNX model and config pbtxt will like this. Remember use the model we training in previous step to serving. The format should be onnx format so please convert the weight file to onnx before upload to bucket.
![Screenshot from 2024-05-11 17-01-13](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/adc4b65c-a51c-4e64-9a1a-377f680810ed)
![Screenshot from 2024-05-11 17-01-19](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/8461cdc0-1fcd-491e-9b24-8d8d9b5bfc58)


Run the following command to have a deploy onnx model
```shellk get p
kubectl apply -f high-density-model-serving/deployments/triton-isvc.yaml
kubectl apply -f high-density-model-serving/intrusion-detection-runtime/triton-servingruntime.yaml
```

To see whether our service is ready, run the following command
```shell
kubectl get isvc
```
You can see that is false
![Screenshot from 2024-05-11 17-03-59](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/690161fc-1f85-4932-8d59-9d0e12498bed)

, it should take several minutes for our service to be `READY`. If not, please check logs of the container `mm` in the pod corresponding to `triton` as follows

kubectl get pods and try to see error 
![Screenshot from 2024-05-11 17-05-19](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/2f3abcac-7e4f-45b0-9c21-11efc94bf886)

if our service change tobe `READY`. All may OK

![Result](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/result-.png)
![Result Inference Service](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/isvc.png)


```shell
kubectl describe pod modelmesh-serving-triton-2.x-6c4978d6db-5k59z
![Screenshot from 2024-05-11 17-05-55](https://github.com/HungNguyenDev1511/Capstone-Project-Model-Serving/assets/69066161/05ce3bc4-5982-4b25-b9ef-29b54dd564cd)

```
just resolve one by one error first

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
