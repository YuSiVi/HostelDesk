from django.urls import path
from complaints import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit, name='submit'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/<int:pk>/remark/', views.add_remark, name='add_remark'),
    path('complaint/<int:pk>/upvote/', views.upvote_complaint, name='upvote_complaint'),
    path('complaint/<int:pk>/rate/', views.rate_complaint, name='rate_complaint'),
    path('edit/<int:pk>/', views.edit_complaint, name='edit_complaint'),
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
    path('delete/<int:pk>/', views.delete_complaint, name='delete_complaint'),
]
