from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from botocore.exceptions import ClientError
import json
import login.cognito
from .models import User
from django.db import transaction

from logging import getLogger
logger = getLogger(__name__)

# Create your views here.
@ensure_csrf_cookie
def auth(request):
    if request.method == 'GET':
        return JsonResponse({})
    ret = {
        "status":500,
        "data": {
            "message": "",
            "aws_result": {}
        },
    }
    try:
        cognito = login.cognito.AWS_Cognito()
        aws_result = cognito.auth(request.POST["user_name"], request.POST["password"])

        ret["status"] = aws_result["ResponseMetadata"]["HTTPStatusCode"]
        ret["data"]["aws_result"] = aws_result
        return JsonResponse(ret)
    except ClientError as ce:
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
        ret["status"] = 500
        ret["data"]["message"] = "システムエラーが発生しました。"
        return JsonResponse(ret)

@ensure_csrf_cookie
def new(request):
    if request.method == 'GET':
        return JsonResponse({})
    ret = {
        "status":500,
        "data": {
            "message": "",
            "aws_result": {}
        },
    }

    if User.objects.is_valid_email(email=request.POST["mail_address"]):
        ret["status"] = 401
        ret["data"]["message"] = "既に使用されているメールアドレスです。"
        return JsonResponse(ret)

    transaction.set_autocommit(False)
    try:
        user = User.objects.create(email=request.POST["mail_address"])
        cognito = login.cognito.AWS_Cognito()
        aws_result = cognito.new(request.POST["user_name"], request.POST["password"], user.mail_address, str(user.id))
        ret["status"] = aws_result["ResponseMetadata"]["HTTPStatusCode"]
        ret["data"]["aws_result"] = aws_result
    except ClientError as ce:
        transaction.rollback()
        if ce.response['Error']['Code'] == 'UsernameExistsException':
            ret["status"] = 401
            ret["data"]["message"] = "既に使用されているユーザー名です。"
        else:
            logger.error(ce)
            ret["status"] = 500
            ret["data"]["message"] = "エラーが発生しました。"
    except Exception as e:
        transaction.rollback()
        logger.error(e)
        ret["status"] = 500
        ret["data"]["message"] = "システムエラーが発生しました。"
    else:
        transaction.commit()
    finally:
        transaction.set_autocommit(True)

    return JsonResponse(ret)
