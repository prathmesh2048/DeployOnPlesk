from django.conf import settings
from . import request
from . import exception
from . import message
import random
import string


# Generate Random String
def generateCode(length):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Handle local requests
def packetStream(url, params, type="post"):
    url = settings.PS_URL + url
    headers = {
        "Authorization": "Bearer " + settings.PS_TOKEN,
        "Content-Type": "application/json",
    }

    if type == "get":
        response = request.get(url, headers).json()
    else:
        response = request.post(url, headers, params).json()

    if response["status"] != 200:
        raise exception.ParseError(response["message"])

    return response


# View Account Info
def accountInfo():
    response = packetStream("/my_info", {}, "get")
    return response["data"]["balance"] / 100


# Create subuser
def createUser():
    username = generateCode(7).lower()
    params = {"username": username}
    return packetStream("/sub_users/create", params)


# View user
def viewUser(username):
    params = {"username": username}
    return packetStream("/sub_users/view_single", params)


# View usage history
def viewUsage(username):
    params = {"username": username}
    return packetStream("/sub_users/view_txs", params)


# Reset auth key
def resetAuthKey(user):
    params = {"username": user.ps_username}

    response = packetStream("/sub_users/reset_auth_key", params)

    user.ps_authkey = response["data"]["proxy_authkey"]
    user.save()

    return response


# Add balance to user
def addBalance(username, amount):
    params = {"username": username, "amount_usd_cents": amount * 100}
    return packetStream("/sub_users/give_balance", params)


# Subtract balance from user account
def subtractBalance(username, amount):
    params = {"username": username, "amount_usd_cents": amount * 100}
    return packetStream("/sub_users/take_balance", params)
