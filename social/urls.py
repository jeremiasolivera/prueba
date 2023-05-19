from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.details, name="rooms"),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('profile/<str:pk>/', views.userProfile, name="userProfile"),


] 

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)