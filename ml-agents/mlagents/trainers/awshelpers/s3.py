import boto3


def push_model_to_s3(brain_name):
    client = boto3.client('s3')
    client.upload_file("models/ppo-0/"+brain_name+".nn",
                       "newbornbucket999999", brain_name+".nn")
