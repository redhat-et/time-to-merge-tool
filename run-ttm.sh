#!/bin/bash

echo Which repository do you want to train the time to merge model this on?
read REPO
echo Which Github organization or user is this repository a part of?
read ORG
echo You will need to generate a Personal Access Token to run this tool. Enter your personal access token
read PAT
echo You will need S3 bucket credentials to store the model and datasets. You can configure your bucket credentials as Action secrets in your forked repository or provide them here. Do you want to share your bucket credentials here? y/n
read CRED
if [ $CRED = y ]
then
  echo Enter your bucket name
  read BUCKET
  echo Enter S3 endpoint url
  read S3ENDPOINT
  echo Enter Access Key
  read ACCESSKEY
  echo Enter Secret Key
  read SECRETKEY
else
  echo Please add your S3 bucket credentials as repository action secrets
fi
curl \
  -X POST \
  -H 'authorization: Bearer $PAT' \
  https://api.github.com/repos/oindrillac/ttmtool/dispatches \
  -d '{"event_type": "workflow-run", "client_payload":{"REPO":"$REPO", "ORG":"$ORG"}}'

echo Request sent. Check github action workflow for running workflow
