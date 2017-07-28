import boto.ec2

AWS_REGION = 'us-east-1'

conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id='AKQ', aws_secret_access_key='2Z0Yzqy/')

aws_zones = conn.get_all_zones()
for aws_zone in aws_zones:
    print aws_zone
