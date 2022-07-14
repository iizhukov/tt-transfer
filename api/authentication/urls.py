from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views


urlpatterns = [
    path('get-user-data/', views.GetUserDataView.as_view(), name="get_user_data"),
    path('user-list/', views.UserListView.as_view(), name="user_list"),
    path('is-auth/', views.IsAuthView.as_view(), name="is_auth"),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('create-user/', views.CreateUserView.as_view(), name='create_user'),
    path('logout/', views.UserLogoutView.as_view(), name="logout"),

    path('token/', views.CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),

    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
