"""AWS utility functions."""
from dataclasses import dataclass
from time import (
    gmtime,
    strftime,
)
from typing import (
    Dict,
    List,
    Optional,
)

import boto3
from botocore.exceptions import ClientError

from fraud.utils.logging import get_logger

logger = get_logger()


@dataclass
class AWSConfig:
    """Data class for AWS configuration."""

    UserId: str
    Account: str
    Arn: str
    ResponseMetadata: Dict[str, str]


def get_aws_credentials() -> AWSConfig:
    """Get the AWS credentials.

    Returns:
        AWSConfig: AWS temporal credentials.
    """
    sts_client = boto3.client("sts")
    return AWSConfig(**sts_client.get_caller_identity())


def get_sagemaker_client(region_name: str) -> boto3.Session:
    """Get an instance of a sagemaker client session.

    Args:
        region_name: str
            The AWS region name

    Returns:
        boto3.Session:
            Sagemaker client session
    """
    client = boto3.client("sagemaker", region_name=region_name)
    return client


def create_sagemaker_model(
    region_name: str,
    ecr_uri_image: str,
    model_artifacts_s3_uri: str,
    execution_role_arn: str,
    model_name: str,
) -> str:
    """Create a SageMaker model.

    Args:
        region_name: str
            The AWS region name
        ecr_uri_image: str
            Unique resource identifier (URI) for the Docker image.
        model_artifacts_s3_uri: str
            S3 URI where the model artifacts are stored (string).
        execution_role_arn: str
            The ARN of the execution role. The execution role is an IAM
            (Identity and Access Management) role that grants permissions to an
             AWS service to access other AWS resources.
        model_name: str
            Name of the SageMaker model.

    Returns:
        str:
            Model AWS ARN.
    """
    try:
        logger.info("Creating SageMaker model.")

        client = get_sagemaker_client(region_name=region_name)

        response = client.create_model(
            ModelName=model_name,
            PrimaryContainer={
                "Image": ecr_uri_image,
                "ModelDataUrl": model_artifacts_s3_uri,
            },
            ExecutionRoleArn=execution_role_arn,
        )
        model_arn = response["ModelArn"]
        logger.info(f"Model created successfully: {model_arn}")

    except ClientError as e:
        logger.error(f"An error occurred: {e}")

    except ValueError as e:
        logger.error(f"Missing Credentials: {e}")

    return model_arn


def create_model_group(
    region_name: str,
    model_group_name: str,
    model_group_description: Optional[str] = None,
) -> str:
    """Create a model group in SageMaker.

    Args:
        region_name: str
            The AWS region name.
        model_group_name: str
            Name of the model group.
        model_group_description: str
            Description of the model group.

    Returns:
        str:
            Model group ARN.
    """
    logger.info("Creating SageMaker model group.")

    client = get_sagemaker_client(region_name=region_name)

    model_package_group_input_dict = {
        "ModelPackageGroupName": model_group_name,
        "ModelPackageGroupDescription": model_group_description,
    }
    try:
        response = client.create_model_package_group(
            **model_package_group_input_dict
        )

        model_group_arn = response["ModelPackageGroupArn"]
        logger.info(f"Model group created successfully: {model_group_arn}")

    except ClientError as e:
        logger.error(f"An error occurred: {e}")

    except ValueError as e:
        logger.error(f"Missing Credentials: {e}")

    return model_group_arn


def register_model_version(
    region_name: str,
    model_group_name: str,
    model_description: str,
    ecr_uri_image: str,
    model_artifacts_s3_uri: str,
    supported_content_types: List[str],
    supported_response_types: List[str],
) -> str:
    """Register a model version inside a model group.

    Args:
         region_name: str
            The AWS region name.
        model_group_name: str
            Name of the model group.
        model_description: str
            Description of the model version.
        ecr_uri_image: str
            Unique resource identifier (URI) for the Docker image.
        model_artifacts_s3_uri: str
            S3 URI where the model artifacts are stored (string).
        supported_content_types: List[str]
            List containing the supported input types for inference.
        supported_response_types: List[str]
            List containing the supported input types for generating the model
            response (prediction).

    Returns:
        str: Model version ARN.
    """
    logger.info("Registering SageMaker model.")

    client = get_sagemaker_client(region_name=region_name)

    modelpackage_inference_specification = {
        "InferenceSpecification": {
            "Containers": [
                {
                    "Image": ecr_uri_image,
                    "ModelDataUrl": model_artifacts_s3_uri,
                }
            ],
            "SupportedContentTypes": supported_content_types,
            "SupportedResponseMIMETypes": supported_response_types,
        }
    }
    create_model_package_input_dict = {
        "ModelPackageGroupName": model_group_name,
        "ModelPackageDescription": model_description,
        "ModelApprovalStatus": "PendingManualApproval",
    }

    create_model_package_input_dict.update(
        modelpackage_inference_specification
    )
    try:
        response = client.create_model_package(
            **create_model_package_input_dict
        )

        model_package_arn = response["ModelPackageArn"]
        logger.info(f"Model created successfully: {model_package_arn}")

    except ClientError as e:
        logger.error(f"An error occurred: {e}")

    except ValueError as e:
        logger.error(f"Missing Credentials: {e}")

    return model_package_arn


def deploy_model_version(
    region_name: str,
    model_name: str,
    model_version_arn: str,
    execution_role_arn: str,
) -> str:
    """Deploy model to an endpoint.

    Args:
        region_name: str
            The AWS region name
        model_name: str
            The Name of the model that will be used.
        model_version_arn:
            Model ARN.
        execution_role_arn: str
            The ARN of the execution role. The execution role is an IAM
            (Identity and Access Management) role that grants permissions to an
             AWS service to access other AWS resources.

    Returns:
        str: Endpoint ARN.
    """
    logger.info("Deploying SageMaker model.")

    client = get_sagemaker_client(region_name=region_name)

    model_name += "-" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())

    logger.info(f"Model name: {model_name}")

    container_list = [{"ModelPackageName": model_version_arn}]

    create_model_response = client.create_model(
        ModelName=model_name,
        ExecutionRoleArn=execution_role_arn,
        Containers=container_list,
    )

    model_arn = create_model_response["ModelArn"]

    logger.info(f"Model arn: {model_arn}")

    endpoint_config_name = f"endpoint-config-{model_name}"
    logger.info(f"Endpoint config name: {endpoint_config_name}")

    create_endpoint_config_response = client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                "InstanceType": "ml.c5.xlarge",
                "InitialVariantWeight": 1,
                "InitialInstanceCount": 1,
                "ModelName": model_name,
                "VariantName": "AllTraffic",
            }
        ],
    )
    logger.info(
        "Endpoint config arn:"
        f" {create_endpoint_config_response['EndpointConfigArn']}"
    )

    endpoint_name = f"endpoint-{model_name}" + strftime(
        "%Y-%m-%d-%H-%M-%S", gmtime()
    )
    logger.info(f"Endpoint name: {endpoint_name}")

    create_endpoint_response = client.create_endpoint(
        EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
    )

    logger.info(f"Endpoint arn: {create_endpoint_response['EndpointArn']}")

    return create_endpoint_response["EndpointArn"]
