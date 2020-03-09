from rest_framework import status
from rest_framework import mixins, viewsets, permissions, filters, pagination, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from users.models import Account, FavoriteTruck
from .serializers import AccountSerializer, FavoriteTruckSerializer


class FavoritesViewSet(ModelViewSet):
    serializer_class = FavoriteTruckSerializer
    queryset = FavoriteTruck.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__id',)


class CustomUserAPIView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.all()
        username = self.request.query_params.get('username')
        email = self.request.query_params.get('email')

        first_name = self.request.query_params.get('first_name', None)
        last_name = self.request.query_params.get('last_name', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        elif email:
            queryset = queryset.filter(email=email)
        elif first_name:
            queryset = queryset.filter(first_name=first_name)
        elif last_name:
            queryset = queryset.filter(last_name=last_name)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = AccountSerializer

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

        tokenObj = Token.objects.filter(key=token).first()

        if tokenObj:
            return Response("Valid token", status=status.HTTP_200_OK)

        return Response("Invalid token", status=status.HTTP_403_FORBIDDEN)


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username', '=email')
    filter_fields = ('first_name', 'last_name')
    pagination_class = pagination.LimitOffsetPagination

    

