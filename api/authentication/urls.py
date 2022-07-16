from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views


urlpatterns = [
    path('reset-password/get-code/', views.ResetPasswordGetCodeView.as_view(), name='reset_password__get_code'),
    path('reset-password/check-code/', views.ResetPasswordCheckCodeView.as_view(), name='reset_password__check_code'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),

    path('edit/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('edit/user-data/', views.EditUserView.as_view(), name="edit_user_data"),
    path('avatar/', views.UserAvatarView.as_view(), name="avatar"),

    path('is-auth/', views.IsAuthView.as_view(), name="is_auth"),
    path('get-user-data/', views.GetUserDataView.as_view(), name="get_user_data"),
    path('user-list/', views.UserListView.as_view(), name="user_list"),

    path('create-user/', views.CreateUserView.as_view(), name='create_user'),
    path('token/', views.CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.UserLogoutView.as_view(), name="logout"),

    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
