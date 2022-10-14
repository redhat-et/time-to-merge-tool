[![Run in container](https://github.com/oindrillac/ttmtool/actions/workflows/run-in-container.yaml/badge.svg)](https://github.com/oindrillac/ttmtool/actions/workflows/run-in-container.yaml)

# Github Action Tool for Time to Merge Model

In this repo we test out TTM toolification process

We have created a Github Action Workflow which carries out the model training process for the Github Time to Merge model.

There are currently 2 ways to run the workflow:

1. Manual Trigger
2. POST Request to Github API Endpoint

```
curl \
  -X POST \
  -H 'authorization: Bearer <insert-personal-access-token-workflow-checked>' \
  https://api.github.com/repos/oindrillac/ttmtool/dispatches \
  -d '{"event_type": "workflow-run", "client_payload":{"REPO":"community", "ORG":"operate-first"}}' 
```


To view running events from the terminal

```
curl --request GET \ 
  --url 'https://api.github.com/repos/oindrillac/ttmtool/actions/runs' \
  --header 'authorization: Bearer <insert-personal-access-token-workflow-checked>' \
  --data '{"event_type": "workflow-run"}'
```
