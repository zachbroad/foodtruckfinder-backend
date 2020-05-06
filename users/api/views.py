from django.http import Http404
from rest_framework import generics, pagination, permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import Account, FavoriteTruck, Feedback
from .serializers import AccountSerializer, FavoriteTruckSerializer, FeedbackSerializer


class FavoritesViewSet(ModelViewSet, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FavoriteTruckSerializer
    model = FavoriteTruck
    queryset = FavoriteTruck.objects.all()

    filterset_fields = ['user', 'truck']

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        # "SHOULD" always return 1 object
        return self.model.objects.get(truck__id=self.request.query_params.get('truck'),
                                      user__id=self.request.query_params.get('user'))

    def get_queryset(self):
        queryset = FavoriteTruck.objects.all()
        user_id = self.request.query_params.get('user__id')
        truck_id = self.request.query_params.get('truck___id')

        if user_id is not None and truck_id is not None:
            queryset = queryset.filter(user__id=user_id, truck__id=truck_id)
        elif user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        elif truck_id is not None:
            queryset = queryset.filter(truck__id=truck_id)

        return queryset


class AccountRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Account.objects.all()


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        profile = AccountSerializer(user, many=False)
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
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    filterset_fields = ['username', 'email', 'first_name', 'last_name']
    pagination_class = pagination.LimitOffsetPagination


class FeedbackViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        acc = AccountSerializer(request.user, many=False)
        return Response(data=acc.data)
