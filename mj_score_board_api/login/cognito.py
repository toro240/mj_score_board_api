from django.conf import settings
import boto3

class AWS_Cognito():
    def __init__(self):
        self.aws_client = boto3.client('cognito-idp',
            region_name = "ap-northeast-1",
            aws_access_key_id = settings.AWS_COGNITO_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_COGNITO_SECRET_ACCESS_KEY_ID,
        )

    def auth(self, user_name, password):
        return self.aws_client.admin_initiate_auth(
            UserPoolId = settings.AWS_COGNITO_USER_POOL_ID,
            ClientId = settings.AWS_COGNITO_CLIENT_ID,
            AuthFlow = "ADMIN_NO_SRP_AUTH",
            AuthParameters = {
                "USERNAME": user_name,
                "PASSWORD": password,
            }
        )

    def new(self, user_name, password, mail_address, user_id):
        return self.aws_client.sign_up(
            ClientId = settings.AWS_COGNITO_CLIENT_ID,
            Username = user_name,
            Password = password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': mail_address
                },
                {
                    'Name': 'custom:user_id',
                    'Value': user_id
                },
            ],
        )
