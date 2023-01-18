[![TTM Inference](https://github.com/redhat-et/time-to-merge-tool/actions/workflows/inference.yaml/badge.svg)](https://github.com/redhat-et/time-to-merge-tool/blob/main/.github/workflows/inference.yaml)

# Github Action for Time to Merge Model

**Want an estimate on how long it will take to get your PR merged?**

The data science team within Red Hat's Emerging Technologies group wanted to know if we could leverage Github Actions to help us do some predictive analytics and measure the velocity of our projects. To that end we developed the "Time to Merge" (TTM) tool .    

This repository contains the TTM GitHub Action needed to train a custom model for individual projects and provide predictions in the form of PR comments. This model can be trained on any repository and can be used to predict the time to merge of new pull requests. To learn more about this approach, please see [here](https://github.com/aicoe-aiops/ocp-ci-analysis/tree/master/notebooks/time-to-merge-prediction).

*NOTE: Currently the GitHub action is set up in a way to succeed and comment time to merge estimates on pull requests only when pull requests are opened from a feature branch of the same repository.*

To use the Github Action for your own repository and train a model, follow these steps:

### Pre-requisites:

1. **S3 bucket**: You will need an S3 bucket to store the data and the model generated as a part of the training process. You can pass the S3 bucket credentials in 2 ways. You can either set them up as Github Action Secrets or pass them as a payload from your http request.

2. **Personal Acess Token**: You also need a personal access token to trigger the workflow and download data from GitHub. You can generate that by going [here](https://github.com/settings/tokens/new?description=my-gh-access-token&scopes=workflow,repo)

## Step 1

Once you have the pre-requisites in place, add your S3 credentials to your repository action secrets (this is the recommended approach) if they are private and you dont want to pass them on through the http request .

To do that, go to your repository "Settings" -> "Security" -> "Secrets" -> "Actions" -> "New Repository Secret" and add secrets for `S3_BUCKET`, `S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, your personal access token as your `GITHUB_TOKEN`, the prefix/folder where you want to store the data on the S3 bucket as the `CEPH_BUCKET_PREFIX`, and the GitHub repository that you want to train the model on and the organization it belongs to as `REPO` and `ORG`.

<img width="200" alt="image" src="https://user-images.githubusercontent.com/32435206/195929605-4518559e-7ffd-4b6d-a47f-e06fd1cdb4ac.png">

<img width="500" alt="image" src="https://user-images.githubusercontent.com/32435206/195929854-840a5784-a23a-4412-b23e-1b83c0160e75.png">

## Step 2

To use this Github Action for both training and inference on new PR's, you will need to add 2 workflow files to your repository.

One action controls the training workflow, and is triggered on-demand and as needed. The other action controls the inference workflow, and is triggered on each new PR submission. 


1. **Training Mode** :

For every new repository, you need to first train the model on the historical pull requests. 
To do that, you will need to add a `train-ttm.yaml` file to the `.github/worklows/` folder on your repository that looks like [this](https://github.com/aicoe-aiops/ocp-ci-analysis/blob/master/.github/workflows/train-ttm.yaml). To run the action in training mode, make sure you specify the `MODE` as `1`.

This mode will initiate the model training process which includes data collection, feature engineering and model training on the historical pull requests and finally runs the inference i.e. predicting the time to merge for the last pull request on the repository. 

(*NOTE : This workflow will fail if there are no PRs on the repository. For this model to train correctly, you would need atleast 11 closed PRs on the repository being trained. For good model performance, we recommend training the model on repositories with atleast a few 100 PRs.*)

You can also initiate a manual trigger by going to actions for your repository like [here](https://github.com/aicoe-aiops/ocp-ci-analysis/actions/workflows/train-ttm.yaml):

![image](https://user-images.githubusercontent.com/26301643/206544812-b6ffbe44-7bd3-4c7d-ab75-55b29d24f8f4.png)

Go select - `Run Time to Merge Model Training` and go to `Run workflow` on upper right and run it like such :

![image](https://user-images.githubusercontent.com/26301643/206548995-5e82cf06-1892-462d-9114-e81065b1f13e.png))

This will initiate the model training and inference action. 


2. **Inference Mode** : 

Similar to the `train-ttm.yaml` file, you need to add another file called `predict-ttm.yaml` to the `.github/worklows/` folder in your repository that looks like [this](https://github.com/aicoe-aiops/ocp-ci-analysis/blob/master/.github/workflows/predict-ttm.yaml). This file has set `MODE` to `0` which will enable inference on all new incoming pull requests and add a comment on the pull request specifying the approximate time it will take to be merged.

![image](https://user-images.githubusercontent.com/26301643/206541965-c85eb5f8-012e-454c-9f0d-467db0c8be07.png)

(*NOTE: For the inference workflow to succesfully comment a time range prediction, you need atleast one open PR on the repsoitory*)

## Step 3

To view your running workflow from the Github UI, go to "Actions" and click on the workflow run :

![image](https://user-images.githubusercontent.com/26301643/206549380-369e6680-5e4e-4994-ae8a-59fd149db426.png)

Click on `pipeline` to see logs and errors :

![image](https://user-images.githubusercontent.com/26301643/206549621-0184880a-769e-48dc-928f-44c721464999.png)

## Architecture

![ttm github workflow (1)](https://user-images.githubusercontent.com/26301643/206780355-7d4e877c-c9ed-448d-8331-ad31e865b85f.png)

## Alternate Approach

You can also use this tool on your repository with an alternate approach without adding the workflow file to your repository. Here are the steps that you can follow:

1. Fork this [repository](https://github.com/redhat-et/time-to-merge-tool) and to your fork add the secrets as mentioned [here](https://github.com/redhat-et/time-to-merge-tool#step-1). Make sure to mention the `REPO` and `ORG` for the repository you want to run TTM on.

2. Go to `Actions` for your fork and select the `run in container` workflow to train the model. 

<img width="1045" alt="Screen Shot 2022-12-09 at 2 51 41 PM" src="https://user-images.githubusercontent.com/26301643/206785568-5bf2890c-d6dd-4875-9a70-025a8e24a8dd.png">

3. You can also interact with this tool by POST request to Github API endpoint. From your terminal, clone your repository and run `bash run-ttm.sh` . This will run the training workflow and train the TTM model on the repo and org of your choice.

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

