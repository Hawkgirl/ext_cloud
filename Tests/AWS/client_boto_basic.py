import boto.ec2
import pprint

AWS_REGION = 'us-east-1'

conn = boto.ec2.connect_to_region(
    "us-east-1",
    aws_access_key_id='AKIAJZZOA2ZK6SOG6EJQ',
    aws_secret_access_key='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')

aws_zones = conn.get_all_zones()
for aws_zone in aws_zones:
    print aws_zone
