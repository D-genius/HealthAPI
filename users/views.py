from rest_framework import generics, permissions
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from django.contrib.auth import update_session_auth_hash
from .serializers import UserSerializer, PasswordSerializer
from .models import CustomUser


class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['read']

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = PasswordSerializer
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['write']

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.data.get('old_password')):
            return Response({"old_password": ["Wrong password."]}, status=400)

        user.set_password(serializer.data.get('new_password'))
        user.save()
        update_session_auth_hash(request, user)
        return Response("Password updated successfully")
# User = get_user_model()

# class UserRegistration(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]