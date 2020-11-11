from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'learning_logs'

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('upload/', views.upload, name='upload'),
    path('edit_topic/<int:topic_id>/', views.edit_topic, name="edit_topic"),
    path('delete/<int:topic_id>/', views.delete_topic, name="delete_topic"),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('search/', views.search, name="search"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
