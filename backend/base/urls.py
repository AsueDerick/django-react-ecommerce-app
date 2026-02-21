from django.urls import path
from . import views

urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile/', views.getUsersProfile, name='user_profile'),
    path('users/update/', views.UpdateUsersProfile, name='update_profile'),
    path('users/register/', views.registerUser, name='register'),
    path('users/', views.getUsers, name='users'),
    path('products/', views.getProducts, name="products"),
    path('products/<str:pk>/', views.getProduct, name="product"),
    
]