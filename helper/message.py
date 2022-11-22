def OTP_MESSAGE(otp):
    return "Verify your OTP: " + str(otp)


def MODULE_NOT_FOUND(module):
    return "No " + module + " found."


def MODULE_STORE_SUCCESS(module):
    return module + " has been added successfully !"


def MODULE_LIST(module):
    return module + " list."


def MODULE_STATUS_CHANGE(module, status):
    return module + " has been " + status + " successfully!"


def MODULE_EXISTS(module):
    return "The " + module + " already exists"


def MODULE_INVALID(module):
    return "Invalid " + module


def INVALID_INPUT(param):
    return param + " has invalid value."


NOT_ACCEPTABLE_REQUEST = "Request Not Acceptable"


EMAIL_NOT_VERIFIED = "You have not verified your email yet. We've sent otp on your registered email. Please verify before login."
EMAIL_OTP_2FA = "You have enabled Two-Factor Authentication. We've sent otp on your registered email. Please verify before login."

LOGIN_SUCCESS = "Login Successful! redirecting..."
USER_EMAIL_EXISTS = "Email already exists."
USER_NAME_EXISTS = "Username already exists."
SIGNUP_USER_SUCCESS = "You have signed up successfully. Please verify your email by entering the otp sent on your email."
PASSWORD_LENGTH = "Password must be between 8 to 50 chars."
VERIFY_OTP_MISMATCH = "You have entered wrong OTP or Invalid User"
MOBILE_OTP_SENT_SUCCESS = (
    "We've sent OTP on your email. Please verify your email address."
)
RESET_PASSWORD_SUCCESS = "Password reset request has been processed successfully."
CHANGE_PASSWORD_SUCCESS = "Your password has been changed successfully."
PASSWORD_MISMATCH = "Incorrect old password."

NOT_VALID_PARAMS = "Request has not valid parameters"
INVALID_RECAPTCHA = "Invalid reCaptcha!"
ACCESS_TRUE = "Access available on this token."

SERVER_ERROR = "Server Error."


# Billing Message
BILLING_ADDRESS_ALREADY_PRESENT = "Billing address is already present."
BILLING_ADDRESS_NOT_PRESENT = "Billing address is not present."


# proxy messages
PLAN_EXPIRED_OR_NOT_FOUND = "Account doesn't having any active plan."
PLAN_EXHAUSTED = "You have used 100% of your plan"
PROXY_GENERATOR_DATA = "Proxy Generator Data."


# WEBHOOK MESSAGES
ORDER_ALREADY_FULLFILLED = "Order is already fullfilled!"
ORDER_NOT_PAID = "Order is not paid."

# MAIL MESSAGE
OTP_SUBJECT = "Verify your email account - hostarena.gg"
CONFIRM_SUBSCRIPTION_SUBJECT = ""

# Newsletter Messages
SUBSCRIPTION_EMAIL_EXISTS = "Subscription is already present with this email."
CHECK_SUBSCRIPTION_MAIL = "Email added to the bucket. Please check you email inbox for confirmation."


# PAYMENT MESSAGES
PAYMENT_FAILD = "Payment failed."
CHECKOUT_SUCCESSFUL = "Payment checkout successful."
