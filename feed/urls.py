from django.urls import path, include
#added include  in line 1

from feed import views


urlpatterns = [
    path ('', include('api.urls')), #added
    path('', views.HomeView.as_view(), name='index'),
    path('new', views.new_post, name='new_post'),
    path('<int:_id>', views.post_details, name='post_details')
]
