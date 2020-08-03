import boto3
import os

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_ID, KEY_PAIR


def create_ec2_instance():
    ec2 = boto3.client('ec2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID, region_name="us-east-1")
    ec2_client = boto3.client('ec2-instance-connect', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID, region_name="us-east-1")
    public_key = ec2.create_key_pair(KeyName=KEY_PAIR)['KeyMaterial']
    generate_pub_file(public_key)
    # images = ec2.describe_images(Owners=['self'])
    resp = ec2.run_instances(ImageId='ami-08f3d892de259504d', MinCount=1, MaxCount=1, KeyName=KEY_PAIR)
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
    ec2_instance_id = resp['Instances'][0]['InstanceId']
    assert check_that_ec2_instance_is_up(ec2, ec2_instance_id)
    #ec2_client.send_ssh_public_key(InstanceId=ec2_instance_id, SSHPublicKey=public_key, InstanceOSUser="ec2-user", AvailabilityZone="us-east-1a")


def generate_pub_file(public_key_data):
    filename = "/home/fadi/Desktop/boto3Automation/boto3_automation/public_key_test.pem"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(public_key_data)


def check_that_ec2_instance_is_up(ec2, ec2_instance_id):
    ec2_instances_list = ec2.describe_instances()['Reservations']
    for ec2_instance in ec2_instances_list:
        ec2_instance_objects = ec2_instance['Instances']
        for ec2_object in ec2_instance_objects:
            if ec2_object['InstanceId'] == ec2_instance_id:
                return True
    return False


def main():
    print("boto3 automation task!")


if __name__ == "__main__":
    main()

create_ec2_instance()
