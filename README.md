In this repo we test out TTM toolification process

We have created a Github Action Workflow which carries out the model training process for the Github Time to Merge model.

There are currently 2 ways to run the workflow:

1. Manual Trigger
2. POST Request to Github API Endpoint

```
curl --request POST \
  --url 'https://api.github.com/repos/oindrillac/test-tool-ttm/dispatches' \  
  --header 'authorization: Bearer <insert-personal-access-token-workflow-checked>' \
  --data '{"event_type": "workflow-run"}'
  
```


To view running events from the terminal

```
curl --request GET \ 
  --url 'https://api.github.com/repos/oindrillac/test-tool-ttm/actions/runs' \
  --header 'authorization: Bearer <insert-personal-access-token-workflow-checked>' \
  --data '{"event_type": "workflow-run"}'
```
