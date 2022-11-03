import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

# get the org/repo from env vars
ORG = os.getenv("GITHUB_ORG")
REPO = os.getenv("GITHUB_REPO")
CEPH_BUCKET_PREFIX = os.getenv("CEPH_BUCKET_PREFIX")

print(f"{ORG}/{REPO}")
print(
    f"Downloaded file is being stored at {CEPH_BUCKET_PREFIX}/srcopsmetrics/bot_knowledge/{ORG}/{REPO}/PullRequest.json"
)

# run collection on the org/repo specified
command ='python -m srcopsmetrics.cli --create-knowledge --repository '+ORG+'/'+REPO+' --entities PullRequest'

os.system(command)
