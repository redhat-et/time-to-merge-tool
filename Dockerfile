# Container image that runs your code
FROM quay.io/aicoe/ocp-ci-analysis

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY . /

RUN chmod +x /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
