from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


class CustomAuthentication(TokenAuthentication):

    def authenticate(self, request):
        tokenString = request.META.get("HTTP_AUTHORIZATION")
        if not tokenString:
            raise exceptions.NotAuthenticated()
        token = tokenString.split()
        if tokenString and len(token) == 2 and not str(token[1]).lower() == "UNDEFINED":
            if not tokenString.startswith("Token "):
                msg = "Header must contain Token"
                raise exceptions.AuthenticationFailed(msg)
        else:
            msg = "Invalid token header. No credentials provided."
            raise exceptions.AuthenticationFailed(msg)
        try:
            response = super().authenticate(request)
            if response:
                return (response, None)
            else:
                msg = "Invalid token."
                raise exceptions.AuthenticationFailed(msg)
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))
