# Introduction 
This project contains a demonstration of a fake fraud-detection model, designed to exemplify how to deploy a machine-learning model using a custom Docker Image on Amazon's SageMaker.

# Getting Started

## Installation process

### Poetry

Poetry is used for dependency management and packaging in Python.

- **Windows**: Follow these [instructions](https://confluence.zurich.com/display/DATASL/Install+and+configure+Poetry+in+Windows) to install and configure Poetry on Windows machines.
- **Unix-based**: For Unix-based systems, refer to the official [Poetry installation guide](https://python-poetry.org/docs/).

### AWS CLI

#### Install AWS CLI

The AWS CLI is used to interact with AWS services.

- Follow the instructions in the official [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) to install the AWS CLI.

#### Configure SSO

To configure Single Sign-On (SSO) for AWS CLI:

- Refer to the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html) for detailed instructions.

#### Login

Set your AWS profile and login via SSO:

```zsh
export AWS_PROFILE=<your-aws-profile>
aws sso login
```
For instance:
```zsh
export AWS_PROFILE=191678926016_AWSPowerUserAccess
aws sso login
```

Retrieve your AWS identity to confirm successful login:
```zsh
aws sts get-caller-identity
```

### Environmental Variables

To test locally, you must create a '.env' file in the project's root directory to store all the environmental variables. To do so, you can use the following template:
```zsh
ENV=PROD
```

### Dependencies
1. Create python environment with all dependencies:
    ```zsh
    poetry install
    ```
   
2. Activate python environment:
    ```zsh
    source .venv/bin/activate
    ```
   
3. Install pre-commit hooks:
    ```zsh
    pre-commit install
    ```
   
## Train model

To train the model, run:

```zsh
python train
```

## Serve model local

Build the docker container locally:

```zsh
docker build --tag fraud:latest . 
```

After training the model you can serve it using the following command:

```zsh
docker run -it --rm -p 8080:8080 -v $(pwd)/assets/api:/opt/ml/model/ --name fraud-server fraud:latest serve
```

After initializing the server you can make a health check using:

```zsh
curl -v http://localhost:8080/ping
```

You should get something like:

```zsh
*   Trying [::1]:8080...
* Connected to localhost (::1) port 8080
> GET /ping HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.4.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: nginx/1.22.1
< Date: Thu, 04 Jul 2024 05:22:58 GMT
< Content-Type: application/json
< Content-Length: 1
< Connection: keep-alive
< 
```

## Upload model to S3

Make the script to upload the model artifacts to S3 executable: 

```zsh
chmod +x upload-model-to-s3.sh  
```

Use the provided script to upload the model to an S3 bucket:

```zsh
./upload-model-to-s3.sh <s3-bucket-name> fraud-detection
```
Replace <s3-bucket-name> with your S3 bucket name.

## Build and push Docker image

Make the script to build and push the Docker Image to ECR executable: 

```zsh
chmod +x build_and_push.sh  
```

Use the provided script to build and push the Docker Image to ECR:

```zsh
./build_and_push.sh fraud-detection
```

## Deploy the model in Sagemaker

### Create the model in SageMaker

To create a model deployable model inside Sagemaker you will need to:

1. Train and upload your model to S3 first and obtain its S3 unique resource identifier (URI).
2. Build and push your Docker image to ECR and obtain its URI.
3. Have a valid Execution role ARN.

```zsh
python create_model_in_sagemaker \
--region-name <your region name, e.g. eu-west-1> \
--ecr-uri-image <Your docker Image URI> \
--model-artifacts-s3-uri <Your model S3 URI> \
--execution-role-arn <Your Execution role> \
--model-name <a model name>
```

This scrip will log the model ARN in you command line.


### Create the Endpoint in SageMaker

## Additional Notes

* Make sure to have the necessary AWS IAM permissions configured for SSO, S3 access, and SageMaker operations.
* Update the .env file with any additional required environment variables specific to your setup.
* The upload-model-to-s3.sh script assumes AWS CLI is configured and has the necessary permissions to access the specified S3 bucket.
