import boto3


def push_model_to_s3(path):
    client = boto3.client('s3')
    print("pushing to s3...")
    brain_name = path.split("/")[-1]
    print(brain_name)
    client.upload_file(path,
                       "newborn-training-models", brain_name)
