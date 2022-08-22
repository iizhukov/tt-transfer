from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views


urlpatterns = [
    path('edit/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('edit/user-data/', views.EditUserView.as_view(), name="edit_user_data"),
    path('avatar/', views.UserAvatarView.as_view(), name="avatar"),
    path('documents/', views.UserDocumentsView.as_view(), name="documents"),

    path('get-user-data/', views.GetUserDataView.as_view(), name="get_user_data"),
    path('user-list/', views.UserListView.as_view(), name="user_list"),

    path('company/', views.CompanyView.as_view(), name="company"),
    path('company/<int:id>', views.CompanyView.as_view(), name="company"),
]
