from typing import OrderedDict
from rest_framework.generics import CreateAPIView, ListAPIView
from helper import helper
from .serializers import AdminLoginSerializer, authenticate


# Admin Login
# post
# /v1/auth/admin-login
class AdminLogin(CreateAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request):
        helper.check_parameters(request, ["username", "password"])
        # helper.verify_recaptcha(request)

        user = self.get_serializer(data=request.data)
        user.is_valid(raise_exception=True)
        user = user.validated_data

        return helper.createResponse(
            helper.message.LOGIN_SUCCESS,
            {
                "username": user.username,
                "email": user.email,
                "token": helper.get_token(user),
            },
        )


# Verify Access
# get
# /v1/auth/access
class CheckAccess(ListAPIView):
    permission_classes = [helper.permission.IsAuthenticated]

    def list(self, request):
        return helper.createResponse(helper.message.ACCESS_TRUE, {
            "success": True,
            "is_active": request.user.is_active
        })


# Update Password
# post
# /v1/auth/update-password
class UpdatePassword(CreateAPIView):
    permission_classes = [helper.permission.IsAuthenticated]
    serializer_class = AdminLoginSerializer

    def post(self, request):
        helper.check_parameters(request, ["old_password", "new_password"])
        helper.isEmpty(request.data["old_password"], "old_password")

        # check password length
        if len(request.data["new_password"]) < 8:
            raise helper.exception.ParseError(helper.message.PASSWORD_LENGTH)

        user = authenticate(
            **{
                "username": request.user.username,
                "password": request.data["old_password"],
            }
        )

        if user != None:
            user.set_password(request.data["new_password"])
            user.save()
            return helper.createResponse(helper.message.CHANGE_PASSWORD_SUCCESS)
        else:
            return helper.createResponse(helper.message.PASSWORD_MISMATCH, status_code=400)
