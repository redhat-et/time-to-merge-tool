[![TTM Inference](https://github.com/redhat-et/time-to-merge-tool/actions/workflows/inference.yaml/badge.svg)](https://github.com/redhat-et/time-to-merge-tool/blob/main/.github/workflows/inference.yaml)

# Github Action Tool for Time to Merge Model

This repository contains a tool to train the Github time to merge model. This model can be trained on any repository and be used to predict the time to merge of new pull requests. To learn more about this model, please see [here](https://github.com/aicoe-aiops/ocp-ci-analysis/tree/master/notebooks/time-to-merge-prediction).


To use the Github Action tool for your own repository and train the model, you can follow these steps:



### Pre-requisites:

1. **S3 bucket credentials**: You will need an S3 bucket to store the data and the model generated as a apart of the training process. You can pass S3 bucket credentials in 2 ways. You can either set them up as Github Action Secrets or pass them as a payload from your http request.

2. **Personal Acess Token**: You need a personal access token to trigger the workflow and download github data. You can generate that by going [here](https://github.com/settings/tokens/new?description=my-gh-access-token&scopes=workflow,repo)


## Step 1


Once you have the pre-requisites in place, add your S3 credentials to your repository action secrets if they are private and you dont want to pass them on through the http request.

To do that, go to repository "Settings" -> "Security" -> "Secrets" -> "Actions" -> "New Repository Secret" and add secrets for `S3_BUCKET`, `S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `GITHUB_TOKEN`, `REPO`, `ORG`

<img width="200" alt="image" src="https://user-images.githubusercontent.com/32435206/195929605-4518559e-7ffd-4b6d-a47f-e06fd1cdb4ac.png">

<img width="500" alt="image" src="https://user-images.githubusercontent.com/32435206/195929854-840a5784-a23a-4412-b23e-1b83c0160e75.png">

## Step 2

We have created a Github Action Workflow which carries out the model training process for the Github Time to Merge model. There are two steps and ways to use this github action :

1. **Training Mode** :

For a every new repository, this is a pre-requisite. We need to first train the model on the previously made pull requests. To run the action in training mode we will need to specify the `MODE` as `1`. You will need to add `train-ttm.yaml` file to `.github/worklows/` like [this](https://github.com/aicoe-aiops/ocp-ci-analysis/blob/master/.github/workflows/train-ttm.yaml). 

This mode will initiate the model training process by following the steps of data collection, feature engineering, model training on the PR data available and finally running the inference i.e. predicting the time to merge for the latest PR on the repository. (NOTE : This workflow will fail if there are no PRs on the repository) So, you can initiate a new trigger by going to actions for your repository like [here](https://github.com/aicoe-aiops/ocp-ci-analysis/actions/workflows/train-ttm.yaml):

![image](https://user-images.githubusercontent.com/26301643/206544812-b6ffbe44-7bd3-4c7d-ab75-55b29d24f8f4.png)

Go select - `Run Time to Merge Model Training` and go to `Run workflow` on upper right and run it like such :

![image](https://user-images.githubusercontent.com/26301643/206545092-1476bc49-18cc-4cac-a7c0-c122c2034179.png)

This will initiate the model training and inference action. 


2. **Infernce Mode** : 

Similar to the `train-ttm.yaml` file, you can add another file called `predict-ttm.yaml` file to `.github/worklows/` like [this](https://github.com/aicoe-aiops/ocp-ci-analysis/blob/master/.github/workflows/predict-ttm.yaml). This file has `MODE` as `0` which would enable just inference on the new incoming Pull Request and add a comment to the pull request specifying the approximate time it will take to be merged.

![image](https://user-images.githubusercontent.com/26301643/206541965-c85eb5f8-012e-454c-9f0d-467db0c8be07.png)


## Step 3

You can run this workflow by triggering it manually

To trigger manually, first set all the environment variables needed to run the workflow as Action secrets to the repo.
These include `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET`, `S3_ENDPOINT_URL`, `CEPH_BUCKET_PREFIX`, `REPO` and `ORG`.

Now, go to the "Actions" section of your forked repository and click on workflow "Run in container" and click on "Run workflow"

<img width="500" alt="image" src="https://user-images.githubusercontent.com/32435206/195928717-079b0c85-c953-43a9-b6e4-cf6efbc7dff5.png">

## Step 4

To view your running workflow from the Github UI, go to "Actions" and click on the workflow run

<img width="700" alt="image" src="https://user-images.githubusercontent.com/32435206/196230588-d8485c8c-2f97-46a9-ba07-b86e1b7c6782.png">

## Architecture

![ttm github workflow (1)](https://user-images.githubusercontent.com/32435206/196721278-b668b411-d1b6-4af3-8d73-3cb0dd8d58ab.png)

### Installs

There are 2 approaches that we follow for installing dependencies.

1. [run-in-container.](.github/workflows/run-in-container.yaml): Install dependencies from base container image ocp-ci-analysis. This is the default option that is selected when run from the run-ttm.sh script. 
2. [install-from-config](.github/workflows/install-from-config.yaml): Install dependencies from requirements.txt. To run this option, you can run a manual workflow-dispatch and trigger this manually from the GitHub UI.
