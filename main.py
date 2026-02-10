#!/home/ubuntu/projects/ami-generator/.venv/bin/python3

from boto3 import client
from datetime import datetime
import structlog


def main():
    logger = structlog.get_logger()
    instance_id = "i-0630fc9dc8b1eaa29"
    ec2 = client("ec2")
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    ami_name = f"backup-kube-{timestamp}"

    try:
        response = ec2.create_image(
            InstanceId=instance_id,
            Name=ami_name,
            NoReboot=True,
            DryRun=False,
            TagSpecifications=[
                {
                    "ResourceType": "image",
                    "Tags": [
                        {"Key": "Name", "Value": ami_name},
                        {"Key": "CreatedBy", "Value": "ami-generator"},
                    ],
                }
            ],
        )
        logger.info(f"created AMI: {response['ImageId']} ({ami_name})")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
