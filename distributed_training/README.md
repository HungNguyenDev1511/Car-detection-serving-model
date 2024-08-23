# Distributed Training Pipeline

## Overview:

This pipeline leverages a combination of Redis for online feature storage, PostgreSQL for offline storage, TensorFlow for distributed training, and MLflow for model tracking and registry. Kubeflow orchestrates the entire process, ensuring a seamless flow from data preparation to model deployment.

## Table of Contents

- [Dataset Preparation](#dataset-preparation)
- [Deploying Multi-Worker Training Jobs](#deploying-multi-worker-training-jobs)
- [Monitoring and Investigating Models](#monitoring-and-investigating-models)
- [Running MLflow with Docker Compose:](#running-mlflow-with-docker-compose)
- [Important Considerations](#important-considerations)
- [Integrating Jenkins for Continuous Integration](#integrating-jenkins-for-continuous-integration)
- [References](#references)

## Dataset Preparation:

Begin by downloading the dataset required for the training job from the following link: [Download Dataset](https://drive.google.com/drive/folders/12ncEAoWT_kwuPT8YRdFysqgS54XJwre7?usp=drive_link). The folder structure should resemble the following:

<div align="center">
  <img src="https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/structure_training.png" alt="Training Job Structure">
</div>

## Deploying Multi-Worker Training Jobs

To deploy multi-worker training jobs, apply the configuration using Kubernetes:

``` shell
kubectl apply -f deployments/mwt.yaml
```

## Monitoring and Investigating Models

To monitor the training process and inspect the models, update the `persistentVolumeClaim` in the `tests/nginx.yaml` file:

```shell
kubectl apply -f tests/nginx.yaml
```

This setup creates a pod that shares a volume with other training pods, allowing them to write and read from a common source. This shared volume facilitates easy access to logs and other critical data.

You can access the pod to check and read logs using the following command:

```shell
kubectl exec -ti nginx bash
```

## Running MLflow with Docker Compose

For a proof-of-concept (POC) or limited resource environments, you can opt to run the MLflow service using Docker:

```shell
docker compose -f docker-compose.yml up --d --build
```

## Important Considerations:

👉 If multiple GPUs are not available, consider using an alternative strategy, as illustrated below:

![Strategy Scope](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/strategy.png)

👉 Customize the script to run the training job according to your requirements. If the job fails, you can diagnose the issue by checking the pod error logs:

 ```shell
    kubectl get TFjob
 ```

 Please check the pod error log and fix it.
![Result Train ](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/result_train_pod.png) 

👉 In your training script, ensure the model definition and dataset loading are encapsulated within the strategy scope:

![Strategy Scope](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/strategy_scope.png)

👉 To monitor the training process, you can exec into the pod or container (if using Docker) to observe the training job in real-time:

![Train Process](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/train_process.png)

👉 The trained model versions will be stored and managed in MLflow:

![Result](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/mlflow%20_modelregistry.png)


## Integrating Jenkins for Continuous Integration

For automated retraining when new data is available, you can integrate Jenkins into your CI/CD pipeline.

1. Install Ngrok: 

```shell
  curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc 
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" 
  sudo tee /etc/apt/sources.list.d/ngrok.list 
  sudo apt update  
  sudo apt install ngrok
```

  
2. Test Ngrok Installation: Run `ngrok` in the terminal to verify the installation:

![CurlNgrok](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/ngrok.png)

3. Retrieve Jenkins Password: Access Jenkins by retrieving the password as shown below:

![JenkinsPassword](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/password_jenkins.png)

4. Configure Jenkins:

- Open browser `localhost:8081` to open `Jenkins` -> `Manage Jenkins` -> `Plugins and Type` : `Docker Pipeline` and `Docker` and choose `Install without start` 
  ![JenkinsPlugin](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/instal_docker_jenkins.png)
- Install necessary plugins like `Docker Pipeline` and `Docker`.
  ![DowloadPlugin](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/install_docker_success.png)

5. Expose Jenkins with Ngrok: 

  - Run `ngrok http 8081` to expose Jenkins:
  ![NgrokForwardingPort](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/ngrok_forwarding.png)

6. Set Up GitHub Webhook:

- Open your Github repository: In this case is Capstone-Model-Serving-pipeline -> go to `Settings` of repository -> `Webhook` -> `Add Webhook` and paste the Forwarding url in step above to Payload Url and concat "/github-webhook/", Content Type: choose `Applycation/json`. In the part "Which events would you like to trigger this webhook" choose `Push` and `Pull`. Finally, wait for the webhook status to show a green mark, indicating that it is working correctly

  ![WebhookGithub](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/webhook_github.png)

- Check the connection. If Jenkins is successfully connected to GitHub, it will appear like this in the GitHub UI (with a green mark on the webhook)

  ![Webhookconnect](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/result_connect_jenkins_github.png)

7. Configure Jenkins Multibranch Pipeline:

- Back to Jenkins -> choose `Dashboard` -> `New Item` then enter the name of your project and choose `Multibranch Pipeline` and `OK`

- Add name Project -> `Branch Source` and `Add Source` you choose Github 

  ![UiConnectToRepository](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/add_credential.png)

- In `Github Credential` -> Choose the Project Name you create above -> and Type the User Name of your Github Account store the Repository (Model-mesh-serving-pipeline blabla ) and in The Password -> Back to your Github Repository -> `Developer settings` -> Personal access tokens then choose `Token classic` -> Generate a New token classic and choose all options for a demo with no error copy the token generated to `Jenkins Password` and `Add`

  ![TokenGithub](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/github_tokens.png)

- Copy the repository we are working on using the repository's HTTPS URL
- Check all information, `Validate it`, and if everything looks correct, then `Save`

  ![Validate](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/validate_connect_repo.png)

- Choose the `Credential` and then choose the `Scope of our project` and `Add the project credential create a new Credential` -> in Username you type the user of DockerHub
  ![UiDockerhub](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/add_credential_dockerhub.png)


- For the Password: Go to DockerHub (where you store your Docker images) then navigate to `Account Setting` -> `Security` -> Generate new token. Copy this token and paste it into Jenkins credentials, using 'dockerhub' as the ID. 

  ![TokenDockerhub](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/generate_token_docker_hub.png)

- Choose `Manage Jenkins` -> `System and go to Github part` -> In Github API usage rate limiting strategy -> Never check rate limit (NOT RECOMMENDED) and `Save` 
- Finally, go to the repository in Jenkins -> `Configure and Github Credential` Select the Github Credential you created in step above then `Save` 
- Click `Scan Repository Now` to check if all connections are correct. If they are not, restart Jenkins and try again

- The result of the build on Jenkins will look like this
  ![JenkinsBuild](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/ui_build_jenkins.png)

- As you can see, the application version will increase
  ![Version](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/images/result_push_dockerhub.png)

# References

For more information, please take a look at examples [here](https://github.com/kubeflow/training-operator/tree/master/examples) and [here](https://github.com/kubeflow/examples/tree/master/github_issue_summarization).

Some other useful examples:
- https://henning.kropponline.de/2017/03/19/distributing-tensorflow/
- https://www.cs.cornell.edu/courses/cs4787/2019sp/notes/lecture22.pdf
- https://web.eecs.umich.edu/~mosharaf/Readings/Parameter-Server.pdf
- https://s3.us.cloud-object-storage.appdomain.cloud/developer/default/series/os-kubeflow-2020/static/kubeflow06.pdf
- https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/parameter-servers
- http://www.juyang.co/distributed-model-training-ii-parameter-server-and-allreduce/
