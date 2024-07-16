"""Script to create an SageMaker Model.

This script assumes you have:

1. Trained the fraud-detection model
2. Uploaded the model artifacts to S3
3. Build the Docker Image for serving
4. Pushed the Docker image to AWS ECR.
5. You are logged in to SageMaker using the `aws sso login` command
6. You refreshed your identity by issuing the command:
    `aws sts get-caller-identity`
"""
import argparse
from datetime import datetime

from fraud import utils


def main(
    region_name: str,
    model_group_name: str,
    ecr_uri_image: str,
    model_artifacts_s3_uri: str,
) -> None:
    """Create a model in SageMaker."""
    utils.register_model_version(
        region_name=region_name,
        model_group_name=model_group_name,
        model_description=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ecr_uri_image=ecr_uri_image,
        model_artifacts_s3_uri=model_artifacts_s3_uri,
        supported_content_types=["application/json"],
        supported_response_types=["application/json"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a SageMaker model that can be deployed."
    )
    parser.add_argument(
        "--region-name",
        type=str,
        help=" The AWS region name.",
        choices=[
            "eu-west-1",
            "eu-west-2",
            "eu-west-3",
        ],
    )
    parser.add_argument(
        "--model-group-name",
        type=str,
        help="Name of the model.",
    )
    parser.add_argument(
        "--ecr-uri-image",
        type=str,
        help="Unique resource identifier (URI) for the Docker image.",
    )
    parser.add_argument(
        "--model-artifacts-s3-uri",
        type=str,
        help="Model artifact Remote path in S3.",
    )

    args = parser.parse_args()
    if vars(args) == {}:
        parser.print_help()
        exit(1)

    main(
        region_name=args.region_name,
        model_group_name=args.model_group_name,
        ecr_uri_image=args.ecr_uri_image,
        model_artifacts_s3_uri=args.model_artifacts_s3_uri,
    )
