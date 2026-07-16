from django.urls import path
from .views import CreatePost,IDUpdateDeletePost
urlpatterns = [
    path('post_create/',CreatePost.as_view(),name="create_post"),
    path('post_delete_update/<int:pk>/',IDUpdateDeletePost.as_view(),name='asda')
]
