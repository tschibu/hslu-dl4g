#!/bin/bash

# copy everything to tschinux but not files/folders starting with a dot (e.g .git)
deploy_user_host=ubuntu@ec2-52-59-191-250.eu-central-1.compute.amazonaws.com


# relative to home directory unless preceded by a slash,
# WARNING: watch out not to delete the whole thing when using:
#   deploy.sh complete
deployment_folder="dl4g"

d="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "x${1:-}" == "xcomplete" ]; then
    echo "Deleting previous deployment:"
    ssh -i $HOME/.ssh/DL4G.pem "$deploy_user_host" "test -n "\$HOME" && rm -rv '$deployment_folder'"
fi
rsync -avz --exclude-from="$d"/.gitignore --exclude .git --exclude jass-data -e "ssh -i $HOME/.ssh/DL4G.pem" "$d/" "$deploy_user_host:$deployment_folder/"
echo "INFO: finished."
