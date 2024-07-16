"""Script to deploy a model from SageMaker registry.

This script assumes you have:

1. Model version registered and approved in the registry
2. You are logged in to SageMaker using the `aws sso login` command
3. You refreshed your identity by issuing the command:
    `aws sts get-caller-identity`
"""
import argparse

from fraud import utils


def main(
    region_name: str,
    model_name: str,
    model_version_arn: str,
    execution_role_arn: str,
) -> None:
    """Deploy a model in SageMaker."""
    utils.deploy_model_version(
        region_name=region_name,
        model_name=model_name,
        model_version_arn=model_version_arn,
        execution_role_arn=execution_role_arn,
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
        "--model-name",
        type=str,
        help="This name will be used to deploy the model.",
    )
    parser.add_argument(
        "--model-version-arn",
        type=str,
        help="Name of the model.",
    )
    parser.add_argument(
        "--execution-role-arn",
        type=str,
        help="Name of the model.",
    )

    args = parser.parse_args()
    if vars(args) == {}:
        parser.print_help()
        exit(1)

    main(
        region_name=args.region_name,
        model_name=args.model_name,
        model_version_arn=args.model_version_arn,
        execution_role_arn=args.execution_role_arn,
    )
