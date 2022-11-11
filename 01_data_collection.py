import os
import pandas as pd
from github import Github
from dotenv import find_dotenv, load_dotenv

import process_pr
import ceph_comm


load_dotenv(find_dotenv(), override=True)

# get the org/repo from env vars
ORG = os.getenv("GITHUB_ORG")
REPO = os.getenv("GITHUB_REPO")
CEPH_BUCKET_PREFIX = os.getenv("CEPH_BUCKET_PREFIX")
TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

## S3 bucket credentials
s3_endpoint_url = os.getenv("S3_ENDPOINT_URL")
s3_access_key = os.getenv("S3_ACCESS_KEY")
s3_secret_key = os.getenv("S3_SECRET_KEY")
s3_bucket = os.getenv("S3_BUCKET")

s3_input_data_path = os.getenv("CEPH_BUCKET_PREFIX")
RAW_DATA_PATH = os.path.join(s3_input_data_path, ORG, REPO)

cc = ceph_comm.CephCommunication(s3_endpoint_url, s3_access_key, s3_secret_key, s3_bucket)

gh = Github(login_or_token=TOKEN, timeout=50)
prs = gh.get_repo(ORG+'/'+REPO).get_pulls(state='closed')
pr_ids = [pr.number for pr in prs]

closed_prs_df = pd.DataFrame(pr_ids, columns=["closed_pr_ids"])
CLOSED_PR_IDS_FILENAME = os.path.join(ORG + REPO + "CLOSED_PR_IDS.parquet")
CLOSED_PRS_KEY = os.path.join(s3_input_data_path, ORG, REPO, "closed_prs")
cc.upload_to_ceph(closed_prs_df, CLOSED_PRS_KEY, CLOSED_PR_IDS_FILENAME)

for pr_id in pr_ids:
    d = process_pr.get_mi_parsed_pr(ORG+'/'+REPO, pr_id, TOKEN)
    pr_df = pd.DataFrame.from_dict(d, orient="index")
    pr_df = pr_df.transpose()

    PR_FILENAME = os.path.join("PRs/"+ str(pr_id) + ".json")
    print("collected PR", RAW_DATA_PATH+"/"+PR_FILENAME)
    
    cc.upload_to_ceph_as_json(pr_df, RAW_DATA_PATH, PR_FILENAME)