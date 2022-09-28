read -p 'Github username:' varname

read -p 'Repository name for TTM prediction:' varrepo

echo
echo "Thanks for setting up your github and sharing the repository you want to perform time-to-merge prediction for."
echo "Now, let's fork the AI4CI repository"

curl -u $varname https://api.github.com/repos/aicoe-aiops/ocp-ci-analysis/forks -d ''
