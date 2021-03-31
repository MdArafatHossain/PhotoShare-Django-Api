from django.urls import path, include
from .import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

   path('api', views.ApiList.as_view()),
   path('api/posts',
       views.PostList.as_view(),
       name = 'post-list' ),
   path('api/profiles', 
      views.ProfileList.as_view(), 
      name = 'profile-list'),
   path('api/posts/<int:pk>', 
      views.PostDetail.as_view(), 
      name = 'post-detail'),
   path('api/profiles/<int:pk>', 
      views.ProfileDetail.as_view(), 
      name = 'profile-detail'),
   path('api/posts/<int:post_id>/comments', 
      views.CommentList.as_view(), 
      name = 'comment-list'),
])
