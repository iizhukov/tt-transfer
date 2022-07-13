from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views


urlpatterns = [
    path('create-user/', views.CreateUserView.as_view(), name='create_user'),
    path('user-list/', views.UserListView.as_view(), name="user_list"),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),

    path('token/', views.CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),

    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
