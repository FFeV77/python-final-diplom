from backend.models import Shop, User
from backend.serialyzers import ShopSerializer, UpdateUserSerializer, CreateUserSerialyzer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated


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
