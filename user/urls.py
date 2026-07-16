from django.urls import path
from .views import AdminMockView, ControllUser, ControllUserPutDelete, PrivateMockView, PublicMockView, UserCreateView,TokenView,UserView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView,TokenBlacklistView

urlpatterns = [
    # здесь смешанные url админ плюс пользователь
    path('User', UserView.as_view(), name='user_controll'),
    path('', UserCreateView.as_view(), name='registration'),
    path('token/', TokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    #ЭТО ЧАСТЬ для админа что бы менять и просматривать пользователей
    path('getuser/', ControllUser.as_view(), name='get_user'),
    path('putdeleteuser/<int:pk>/', ControllUserPutDelete.as_view(), name='put_delete_user'),

    #это надеюсь то что нужно было 
    path('public/', PublicMockView.as_view(), name='public-mock'),
    path('private/', PrivateMockView.as_view(), name='private-mock'),
    path('admin/', AdminMockView.as_view(), name='admin-mock'),

]
