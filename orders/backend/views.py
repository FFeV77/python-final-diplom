from backend.models import Shop, User
from backend.serialyzers import (CreateUserSerialyzer, ShopLoadSerializer,
                                 ShopSerializer, UpdateUserSerializer)
from backend.utils import file_shop_load, link_shop_load
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerialyzer


class GetUserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user


class ShopView(RetrieveAPIView):
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer


class ShopLoadView(APIView):
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ShopLoadSerializer

    def post(self, request):
        if request.data.get('file'):
            resp = file_shop_load(request.data['file'], request)
        elif request.data.get('link'):
            resp = link_shop_load(request.data['link'], request)
        else:
            resp = {'error': 'data not set'}
        return Response(resp)
