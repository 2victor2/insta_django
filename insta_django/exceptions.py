from rest_framework.exceptions import APIException


class NotAllowedMimetypeException(APIException):
    status_code = 400
    default_detail = "Not allowed media format"
