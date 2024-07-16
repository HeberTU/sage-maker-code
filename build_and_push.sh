#!/usr/bin/env bash

# The argument to this script is the image name. This will be used as the image on the local
# machine and combined with the account and region to form the repository name for ECR.
image=$1

if [ "$image" == "" ]; then
    echo "Usage: $0 <image-name>"
    exit 1
fi

chmod +x docker-entrypoint.sh

# Get the account number associated with the current IAM credentials
account=$(aws sts get-caller-identity --profile $AWS_PROFILE --query Account --output text)

if [ $? -ne 0 ]; then
    echo "Error retrieving AWS account number."
    exit 255
fi

# Get the region defined in the current configuration (default to us-west-2 if none defined)
# us-west-1 == ireland
region=$(aws configure get region)
region=${region:-us-west-1}

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"

# If the repository doesn't exist in ECR, create it.
if ! aws ecr describe-repositories --profile $AWS_PROFILE   --repository-names "${image}" > /dev/null 2>&1; then
    aws ecr create-repository --repository-name "${image}" > /dev/null
fi

# Get the login command from ECR for AWS CLI v2 and execute it directly
aws ecr get-login-password --region ${region} --profile $AWS_PROFILE | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com

# Build the docker image locally with the image name and then push it to ECR
# with the full name.
docker build -t ${image} .
docker tag ${image} ${fullname}

docker push ${fullname}
