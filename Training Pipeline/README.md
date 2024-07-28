# How-to Guide
First, you should download the Data set for the training job from here: 
- https://drive.google.com/drive/folders/12ncEAoWT_kwuPT8YRdFysqgS54XJwre7?usp=drive_link
- The structure of the folder will be like this:
![Training Job Structure](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/StructureTrainning.png)


## Build the step

Multi-worker training
 ``` shell
 cd multi-worker-training
 bash build.sh
 kubectl apply -f mwt.yaml
 ```

## Investigate the models

Update `persistentVolumeClaim` in the file `tests/nginx.yaml` with:

 ```shell
    kubectl apply -f tests/nginx.yaml
    kubectl exec -ti nginx bash
 ```
# Run Docker Compose instead of Kubernetes to run the service MLFLOW (optional)
 if want to POC in low resources you can use docker instead
 ```shell
 docker compose -f docker-compose.yml up --d --build
 ```

# Something needs to be noted here
- If you  don't have multiple GPUs, please use another Strategy for example below

![Strategy Scope](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/Strategy.png)
- You can custom the script and run the training job following your custom if result fails by command: 
 ```shell
    kubectl get TFjob
 ```
 kindly check the log of the pod error and fix it
![Result Train ](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/result_train_pod.png) 

- In the logic of the training script, you must define the model and load the dataset in strategy scope like this:
![Strategy Scope](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/strategy_scope.png)

- You can exec to the pod or container (if use docker instead) you can see the process of training job
![Train Process](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/train_process.png)
- The Version of the model will be stored in MLFLOW like the following result below:
![Result](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/Mlflow%20_modelregistry.png)


# Add Mlflow for model registry now (Optional section)

Finally, add Jenkins to CICD when updating more data the system automatically train
- Install Ngrok: curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
- Test ngrok install success: ngrok
![CurlNgrok] (https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/ngrok.png)

- Get passowrd Jenkins like this:
![JenkinsPassword](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/password_jenkins.png)

- Open browser localhost:8081 to open Jenkins -> Manage Jenkins -> Plugins and Type : Docker Pipeline and Docker and choose install without start 
![JenkinsPlugin](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/instal_docker_jenkins.png)
- Waiting some minute
![DowloadPlugin](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/install_docker_success.png)

- Now open Terminal Linux and type: Ngrok http 8081 (that expose the request to Jenkins) and copy Forwarding url (something like https://9d76-42-113.ngrok-free.app) and if and ok you can see something like this
![NgrokForwardingPort](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/ngrok_forwarding.png)


- Open your github repository: In this case is Capstone-Model-Serving-pipeline -> go to Settings of repository -> Webhook -> Add Webhook and paste the Forwarding url in step above to Payload Url and concat "/github-webhook/", Content Type: choose Applycation/json. In the part "Which events would you like to trigger this webhook" choose Push and Pull. Finally, wait the status of webhook to the green mark so that is ok


![WebhookGithub](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/webhook_github.png)

- Check connect, if jenkins connect to github success, it will be like this in github UI (have green markdown in webhook)

![Webhookconnect](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/result_connect_jenkins_github.png)

- Back to Jenkins -> choose Dashboard -> New Item and you type your name of the project and choose Multibrach Pipeline and OK

- Add name Project -> Branch Source and Add Source you choose Github 

![UiConnectToRepository](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/add_credential.png)

- In Github Credential -> Choose the Project Name you create above -> and Type the User Name of your Github Account store the Repository (Model-mesh-serving-pipeline blabla ) and in The Password -> Back to your Github Repository -> Developer settings -> Personal access tokens then choose Token classic -> Generate New token classic and choose all option for demo no error and copy the token generated to Jenkins Password and Add

![TokenGithub](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/github_tokens.png)

- Copy The Repository we are working to the Repository HTTPS URL 
- Check all information, Validate it ,if all you see ok, then Save

![Validate](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/validate_connect_repo.png)

- Choose the Credential and then choose the Scope of our prọect and Add the project credential create a new Credential -> in Username you type the user of DockerHub
![UiDockerhub](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/add_credential_dockerhub.png)


- For the Password: Go to DockerHub (where you store all your docker Images) -> go to Account Setting -> Security -> Generate new token and then copy to the Credential of Jenkins the Id you type dockerhub  

![TokenDockerhub](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/generate_token_docker_hub.png)

- Choose Manage Jenkins -> System and go to Github part -> In Github API usage rate limiting strategy -> Never check rate limit (NOT RECOMMENDED) and Save 
- Finally, go to the Repo in Jenkins -> Configure and Github Credential you choose the Github Credential you created in step above then Save 
- Scan Repository Now to check all connections is ok or not, if not restart Jenkins again 

- The result of building on Jenkins will be like this 
![JenkinsBuild](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/ui_build_jenkins.png)

- As you can see the version of application will be increase
![Version](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/image/result_push_dockerhub.png)

# References

For more information, please take a look at examples [here](https://github.com/kubeflow/training-operator/tree/master/examples) and [here](https://github.com/kubeflow/examples/tree/master/github_issue_summarization).

Some other useful examples:
- https://henning.kropponline.de/2017/03/19/distributing-tensorflow/
- https://www.cs.cornell.edu/courses/cs4787/2019sp/notes/lecture22.pdf
- https://web.eecs.umich.edu/~mosharaf/Readings/Parameter-Server.pdf
- https://s3.us.cloud-object-storage.appdomain.cloud/developer/default/series/os-kubeflow-2020/static/kubeflow06.pdf
- https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/parameter-servers
- http://www.juyang.co/distributed-model-training-ii-parameter-server-and-allreduce/
