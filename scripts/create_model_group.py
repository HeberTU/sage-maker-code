"""Script to create an SageMaker Model Group.

This script assumes:

1. You are logged in to SageMaker using the `aws sso login` command
2. You refreshed your identity by issuing the command:
    `aws sts get-caller-identity`
"""
import argparse
from typing import Optional

from fraud import utils


def main(
    region_name: str,
    model_group_name: str,
    model_group_description: Optional[str] = None,
) -> None:
    """Create a model in SageMaker."""
    utils.create_model_group(
        region_name=region_name,
        model_group_name=model_group_name,
        model_group_description=model_group_description,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a SageMaker model group."
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
        help="Name of the model group.",
    )
    parser.add_argument(
        "--model-group-description",
        type=str,
        help="Description of the model group.",
        default=None,
    )

    args = parser.parse_args()
    if vars(args) == {}:
        parser.print_help()
        exit(1)

    main(
        region_name=args.region_name,
        model_group_name=args.model_group_name,
        model_group_description=args.model_group_description,
    )
