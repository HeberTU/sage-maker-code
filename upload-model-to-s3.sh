#!/usr/bin/env bash

# The first argument to this script is the S3 bucket name and the second is the model name
bucket=$1
model_name=$2

if [ "$bucket" == "" ] || [ "$model_name" == "" ]; then
    echo "Usage: $0 <s3-bucket-name> <model-name>"
    exit 1
fi

model_directory="assets/api/"

# Check if the model directory exists
if [ ! -d "$model_directory" ]; then
    echo "Model directory $model_directory does not exist."
    exit 2
fi

# Check if the S3 bucket exists
if ! aws s3 ls "s3://$bucket" > /dev/null 2>&1; then
    echo "Bucket named $bucket does not exist. Creating bucket..."
    if ! aws s3 mb "s3://$bucket"; then
        echo "Failed to create bucket. Ensure that the bucket name is globally unique."
        exit 3
    fi
    echo "Bucket $bucket created successfully."
fi

# Compress the model
tar -czvf model.tar.gz -C "$model_directory/" .

# Upload the compressed model file to S3
echo "Uploading model.tar.gz to s3://$bucket/$model_name/"
aws s3 cp model.tar.gz "s3://$bucket/$model_name/model.tar.gz"

if [ $? -eq 0 ]; then
    echo "Upload complete."
else
    echo "Upload failed."
    exit 4
fi
