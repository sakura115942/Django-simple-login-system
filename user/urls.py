from django.urls import path
from .views import RegisterView, LoginView, logout, UserDetailView, UserListView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('<pk>/', UserDetailView.as_view(), name='user_detail'),
]
