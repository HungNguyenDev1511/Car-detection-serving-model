# How-to Guide

## Build the step

Multi-worker training
    ```shell
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

# References

For more information, please take a look at examples [here](https://github.com/kubeflow/training-operator/tree/master/examples) and [here](https://github.com/kubeflow/examples/tree/master/github_issue_summarization).

Some other useful examples:
- https://henning.kropponline.de/2017/03/19/distributing-tensorflow/
- https://www.cs.cornell.edu/courses/cs4787/2019sp/notes/lecture22.pdf
- https://web.eecs.umich.edu/~mosharaf/Readings/Parameter-Server.pdf
- https://s3.us.cloud-object-storage.appdomain.cloud/developer/default/series/os-kubeflow-2020/static/kubeflow06.pdf
- https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/parameter-servers
- http://www.juyang.co/distributed-model-training-ii-parameter-server-and-allreduce/



Add mlflow for model registry now

Finally add jenkins to CICD when update more data the system automatically train
- Write docker compose to run service Jenkins
- Write Jenkins Script to train and deploy automatically
- Install Ngrok: curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
- Test ngrok install success: ngrok
- Open browser localhost:8081 to open Jenkins -> Manage Jenkins -> Plugins and Type : Docker Pipeline and Docker and choose install without start 
- Now open Terminal Linux and type: Ngrok http 8081 (that expose the request to Jenkins) and copy Forwarding url (something like https://9d76-42-113.ngrok-free.app)
- Open your github repository: In this case is Capstone-Model-Serving-pipeline -> go to Settings of repository -> Webhook -> Add Webhook and paste the Forwarding url in step above to Payload Url and concat "/github-webhook/", Content Type: choose Applycation/json. In the part "Which events would you like to trigger this webhook" choose Push and Pull. Finally, wait the status of webhook to the green mark so that is ok
- Back to Jenkins -> choose Dashboard -> New Item and you type your name of project and choose Multibrach Pipeline and OK
- Add name Project -> Branch Source and Add Source you choose Github 
- In Github Credential -> Choose the Project Name you create above -> and Type your User Name of your Github Account store the Repository (Model-mesh-serving-pipeline blabla ) and in The Password -> Back to your Github Repository -> Developer settings -> Personal access tokens then choose Token classic -> Generate New token classic and choose all option for demo no error and copy the token generated to Jenkins Password and Add
- Copy The Repository we are working to Repository HTTPS url 
- Check all information, if all you see ok, then Save 
- Choose the Credential and then choose the Scope of our prọect and Add the project credential create a new Credential -> in Username you can type anything you want
- For the Password: Go to DockerHub (where you store all your docker Images) -> go to Account Setting -> Security -> generate new token and then copy to the Credential of Jenkins the Id you type dockerhub  
- Choose Manage Jenkins -> System and go to Github part -> In Github API usage rate limiting strategy -> Never check rate limit (NOT RECOMMENDED) and Save 
- Finnally, go to the Repo in Jenkins -> Configure and Github Credential you choose Github Credential you create in step above then Save 
- Scan Repository Now to check all connect is ok or not, if not restart Jenkins again 
