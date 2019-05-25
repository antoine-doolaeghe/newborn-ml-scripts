import boto3
# Create an SNS client
sns = boto3.client('sns')


def send_sns_message(topic_arn, message):
    sns.publish(
        TopicArn=topic_arn,
        Message=message
    )
