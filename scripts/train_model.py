"""Script to start a training job in SageMaker.

This script assumes:

1. You are logged in to SageMaker using the `aws sso login` command
2. You refreshed your identity by issuing the command:
    `aws sts get-caller-identity`
"""
import argparse
import time
import boto3


def main():
    """Train a model on SageMaker."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_s3_uri', required=True, help='S3 URI for input data')
    parser.add_argument('--ecr_container_url', required=True, help='ECR container URL')
    parser.add_argument('--output_bucket', required=True, help='S3 bucket for output data')
    parser.add_argument('--sagemaker_role', required=True, help='SageMaker role ARN')
    args = parser.parse_args()

    input_s3_uri = args.input_s3_uri
    ecr_container_url = args.ecr_container_url
    output_bucket = args.output_bucket
    sagemaker_role = args.sagemaker_role

    session = boto3.Session()
    sagemaker_client = session.client('sagemaker')

    name = 'fraud-' + time.strftime('%Y-%m-%d-%H-%M-%S')

    instance_type = 'ml.m4.xlarge'
    instance_count = 1
    memory_volume = 8

    _ = sagemaker_client.create_training_job(
        TrainingJobName=name,
        AlgorithmSpecification={
            'TrainingImage': ecr_container_url,
            'TrainingInputMode': 'File'
        },
        RoleArn=sagemaker_role,
        InputDataConfig=[{
            'ChannelName': 'train',
            'DataSource': {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": input_s3_uri,
                    "S3DataDistributionType": "FullyReplicated"
                }
            },
            'ContentType': 'text/csv',
            'CompressionType': 'None'
        }],
        OutputDataConfig={"S3OutputPath": output_bucket},
        ResourceConfig={
            "InstanceType": instance_type,
            "InstanceCount": instance_count,
            "VolumeSizeInGB": memory_volume
        },
        StoppingCondition={'MaxRuntimeInSeconds': 43200}
    )


if __name__ == '__main__':
    main()