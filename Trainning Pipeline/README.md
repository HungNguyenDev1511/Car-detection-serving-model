# How-to Guide
First, you should download the Data set for the training job from here: 
- https://drive.google.com/drive/folders/12ncEAoWT_kwuPT8YRdFysqgS54XJwre7?usp=drive_link
- the Structure of folder will be like this:
- 
![Trainning job ](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/StructureTrainning.png)


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
# Run Docker Compose instead of Kubernetes to run the service MLFLOW (option)
 if want to POC in low resources you can use docker instead
 ```shell
 docker compose -f docker-compose.yml up --d --build
 ```

# Something needs to be noted here
- If you  don't have multiple GPUs, please use another Strategy for example below
-
![Strategy Scope](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/Strategy.png)
- You can custom the script and run the training job following your custom if result fails by command: 
 ```shell
    kubectl get TFjob
 ```
 kindly check the log of the pod error and fix it
-
![Result Train ](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/result_train_pod.png) 

- In the logic of the training script, you must define the model and load the dataset in strategy scope like this:
-
![Strategy Scope](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/strategy_scope.png)

- You can exec to the pod or container (if use docker instead) you can see the process of training job
-
![Train Process](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/train_process.png)
- The Version of the model will be stored in MLFLOW like the following result below:
-
![Result](https://github.com/HungNguyenDev1511/Car-detection-serving-model/blob/refactor/Mlflow%20_modelregistry.png)


# Add Mlflow for model registry now (Optional section)

Finally, add Jenkins to CICD when updating more data the system automatically train
- Write docker-compose to run the service Jenkins
- Write Jenkins Script to train and deploy automatically
- Install Ngrok: curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
- Test ngrok install success: ngrok
- Open browser localhost:8081 to open Jenkins -> Manage Jenkins -> Plugins and Type : Docker Pipeline and Docker and choose install without start 
- Now open Terminal Linux and type: Ngrok http 8081 (that expose the request to Jenkins) and copy Forwarding url (something like https://9d76-42-113.ngrok-free.app)
- Open your github repository: In this case is Capstone-Model-Serving-pipeline -> go to Settings of repository -> Webhook -> Add Webhook and paste the Forwarding url in step above to Payload Url and concat "/github-webhook/", Content Type: choose Applycation/json. In the part "Which events would you like to trigger this webhook" choose Push and Pull. Finally, wait the status of webhook to the green mark so that is ok
- Back to Jenkins -> choose Dashboard -> New Item and you type your name of the project and choose Multibrach Pipeline and OK
- Add name Project -> Branch Source and Add Source you choose Github 
- In Github Credential -> Choose the Project Name you create above -> and Type the User Name of your Github Account store the Repository (Model-mesh-serving-pipeline blabla ) and in The Password -> Back to your Github Repository -> Developer settings -> Personal access tokens then choose Token classic -> Generate New token classic and choose all option for demo no error and copy the token generated to Jenkins Password and Add
- Copy The Repository we are working to the Repository HTTPS URL 
- Check all information, if all you see ok, then Save 
- Choose the Credential and then choose the Scope of our prọect and Add the project credential create a new Credential -> in Username you can type anything you want
- For the Password: Go to DockerHub (where you store all your docker Images) -> go to Account Setting -> Security -> generate new token and then copy to the Credential of Jenkins the Id you type dockerhub  
- Choose Manage Jenkins -> System and go to Github part -> In Github API usage rate limiting strategy -> Never check rate limit (NOT RECOMMENDED) and Save 
- Finally, go to the Repo in Jenkins -> Configure and Github Credential you choose the Github Credential you created in step above then Save 
- Scan Repository Now to check all connections is ok or not, if not restart Jenkins again 


# References

For more information, please take a look at examples [here](https://github.com/kubeflow/training-operator/tree/master/examples) and [here](https://github.com/kubeflow/examples/tree/master/github_issue_summarization).

Some other useful examples:
- https://henning.kropponline.de/2017/03/19/distributing-tensorflow/
- https://www.cs.cornell.edu/courses/cs4787/2019sp/notes/lecture22.pdf
- https://web.eecs.umich.edu/~mosharaf/Readings/Parameter-Server.pdf
- https://s3.us.cloud-object-storage.appdomain.cloud/developer/default/series/os-kubeflow-2020/static/kubeflow06.pdf
- https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/parameter-servers
- http://www.juyang.co/distributed-model-training-ii-parameter-server-and-allreduce/
