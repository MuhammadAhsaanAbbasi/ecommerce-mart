import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore
from fastapi import HTTPException

from ..setting import AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY, DOMAIN_NAME 

client = boto3.client(
    "ses",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

# Function to check if an email is verified
def is_email_verified(email_address: str) -> bool:
    response = client.list_verified_email_addresses()
    return email_address in response['VerifiedEmailAddresses']

def verify_email_func(email_address: str):
    response = client.verify_email_address(
        EmailAddress=[email_address]
    )
    return {
        "message": "Verification Email sent!",
        "response": response
    }

# Function to send email via AWS SES
async def send_email_via_ses(user_email: str, body: str, subject: str):
    recipient = user_email.lower().strip()
    charset = 'UTF-8'
    sender = DOMAIN_NAME
    try:
        response = client.send_email(
            Destination={'ToAddresses': [recipient]},
            Message={
                'Body': {'Html': {'Charset': charset, 'Data': body}},
                'Subject': {'Charset': charset, 'Data': subject},
            },
            Source=sender,
        )
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'MessageRejected':
            raise HTTPException(status_code=400, detail=f"Email address is not verified: {recipient}")
        if error_code == 'InvalidParameterValue':
            raise HTTPException(status_code=400, detail=f"Invalid email address format: {recipient}")
        raise HTTPException(status_code=500, detail=str(e)) from e
    return response