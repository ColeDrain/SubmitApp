from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('<int:id>/detail/', views.question_detail, name='detail'),
    path('about/', views.about, name='about'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('submit/', views.submit_form, name='submit'),
    path('question_upload/', views.question_upload, name='question_upload'),
    path('<int:id>/question_update/', views.update, name='question_update'), 
]