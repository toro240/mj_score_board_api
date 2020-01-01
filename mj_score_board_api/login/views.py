from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from botocore.exceptions import ClientError
from django.conf import settings
import json
import boto3

from logging import getLogger
logger = getLogger(__name__)

@ensure_csrf_cookie
# Create your views here.
def auth(request):
    if request.method == 'GET':
        return JsonResponse({})

    try:
        aws_client = boto3.client('cognito-idp',
            region_name = "ap-northeast-1",
            aws_access_key_id = settings.AWS_COGNITO_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_COGNITO_SECRET_ACCESS_KEY_ID,
        )

        aws_result = aws_client.admin_initiate_auth(
            UserPoolId = settings.AWS_COGNITO_USER_POOL_ID,
            ClientId = settings.AWS_COGNITO_CLIENT_ID,
            AuthFlow = "ADMIN_NO_SRP_AUTH",
            AuthParameters = {
                "USERNAME": request.POST["user_name"],
                "PASSWORD": request.POST["password"],
            }
        )
        return JsonResponse(aws_result)
    except ClientError as ce:
        ret = {
            "status":500,
            "data": {
                "message": "",
            },
        }
        if ce.response['Error']['Code'] == 'NotAuthorizedException':
            ret["status"] = 401
            ret["data"]["message"] = "ユーザー名・パスワードが間違っています。"
        else:
            logger.error(ce)
            ret["status"] = 500
            ret["data"]["message"] = "エラーが発生しました。"
        return JsonResponse(ret)
    except Exception as e:
        logger.error(e)
        ret = {
            "status":500,
            "data":"システムエラーが発生しました。",
        }
        return JsonResponse(ret)
