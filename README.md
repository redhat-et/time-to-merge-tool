[![Run in container](https://github.com/oindrillac/ttmtool/actions/workflows/run-in-container.yaml/badge.svg)](https://github.com/oindrillac/ttmtool/actions/workflows/run-in-container.yaml)

# Github Action Tool for Time to Merge Model

This repository contains a tool to train the Github time to merge model. This model can be trained on any repository and be used to predict the time to merge of new pull requests. To learn more about this model, please see [here](https://github.com/aicoe-aiops/ocp-ci-analysis/tree/master/notebooks/time-to-merge-prediction).

We have created a Github Action Workflow which carries out the model training process for the Github Time to Merge model.

To use the Github Action tool and train your model, you can follow these steps:

## Step 1

Fork this repository to your account.

<img width="500" alt="image" src="https://user-images.githubusercontent.com/32435206/195927731-484b8640-cee5-45e3-8940-49d80463d945.png">

## Step 2

### Requirements
1. **S3 bucket credentials**: You will need an S3 bucket to store the data and the model generated as a apart of the training process. You can pass S3 bucket credentials in 2 ways. You can either set them up as Github Action Secrets or pass them as a payload from your http request.

2. **Personal Acess Token**: You need a personal access token to trigger the workflow and download github data. You can generate that by going [here](https://github.com/settings/tokens/new?description=my-gh-access-token&scopes=workflow,repo)

**Optional**

You can add your S3 credentials to your repository action secrets if they are private and you dont want to pass them on through the http request.

To do that, go to repository "Settings" -> "Security" -> "Secrets" -> "Actions" -> "New Repository Secret" and add secrets for `S3_BUCKET`, `S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

<img width="200" alt="image" src="https://user-images.githubusercontent.com/32435206/195929605-4518559e-7ffd-4b6d-a47f-e06fd1cdb4ac.png">

<img width="500" alt="image" src="https://user-images.githubusercontent.com/32435206/195929854-840a5784-a23a-4412-b23e-1b83c0160e75.png">

## Step 3
There are currently 2 ways to run the workflow:


1. **POST Request to Github API Endpoint**

From your terminal, clone your repository and run `bash run-ttm.sh`.

* Enter your github username
* Enter the repository you want to train the model on eg: `community`
* Enter the organization the repo belongs to eg: `operate-first`
* Enter the personal access token generated in the previous step eg: `ghp_xyzxyzxyz`

If you are passing your S3 credentials here
* Enter your bucket name
* Enter your endpoint url
* Enter your Access Key
* Enter your Secret Key

![image](https://user-images.githubusercontent.com/26301643/196466088-10e8f725-0e5c-494e-b146-a1fd5ce6c31e.png)

2. **Manual Trigger**

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
