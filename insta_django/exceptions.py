from rest_framework.exceptions import APIException


class NotAllowedMimetypeException(APIException):
    status_code = 400
    default_detail = "Not allowed media format"


class NotAllowedMoreThan10TagsException(APIException):
    status_code = 400
    default_detail = "Not allowed more than 10 tags by post"
