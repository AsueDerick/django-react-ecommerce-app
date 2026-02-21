from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Product
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from .serializers import MyTokenObtainPairSerializer, ProductSerializer, UserSerializer, UserSerializerWithToken

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    
    if User.objects.filter(username=data['email']).exists():
        return Response({"detail": "User already exists"}, status=400)
    
    user = User.objects.create(
        first_name = data["name"],
        username = data['email'],
        email = data['email'],
        password = make_password(data['password'])
    )
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def getUsersProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def UpdateUsersProfile(request):
    user = request.user
    data = request.data

    # Update fields
    user.first_name = data.get("username", user.first_name)  # or "name"
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    if data.get("password"):
        user.password = make_password(data["password"])

    user.save()

    # Return updated user with token
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])  
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([])
def getProduct(request, pk):
    products = Product.objects.get(_id=pk)
    serializer = ProductSerializer(products, many=False)
    return Response(serializer.data)

