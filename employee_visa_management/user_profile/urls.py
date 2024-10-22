from .views import *
from django.urls import path

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('login/', LoginView.as_view(), name='login'),
    path('submit_user_data/', ParticularUserDataFormView.as_view(), name='submit_user_data'),
    path('user_data_get/', ParticularUserDataListView.as_view(), name='user_data_list'),
    path('update_user_data/<int:pk>/', PartcularUserDataUpdateView.as_view(), name='update_user_data'),
]