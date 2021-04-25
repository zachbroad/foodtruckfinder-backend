from django.http import Http404
from rest_framework import generics, pagination, permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from trucks.models import TruckFavorite
from users.models import User, Feedback
from .serializers import UserSerializer, FavoriteTruckSerializer, FeedbackSerializer



class AccountRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        profile = UserSerializer(user, many=False)
        return Response({
            'token': token.key,
            'username': user.username,
            'user_id': user.pk,
            'email': user.email,
            'admin': user.is_superuser,
            'staff': user.is_staff,
            'profile': profile.data
        })


class ValidateToken(APIView):
    permission_classes = [AllowAny]

    # def get(self, request):
    #     return Response()

    def post(self, request, *args, **kwargs):
        token = self.request.data['token']
        token_obj = Token.objects.filter(key=token).first()

        if token_obj:
            return Response("Valid token", status=status.HTTP_200_OK)

        return Response("Invalid token", status=status.HTTP_403_FORBIDDEN)


class AccountViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    filterset_fields = ['username', 'email', 'first_name', 'last_name']
    pagination_class = pagination.LimitOffsetPagination


class FeedbackViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()


class ProfileViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

