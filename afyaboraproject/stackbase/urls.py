from django.urls import path
from . import views

app_name = 'stackbase'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # CRUD funtions
    path('questions/', views.QuestionListView.as_view(), name='question-lists'),
    path('questions/new', views.QuestionCreateView.as_view(), name='question-create'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:pk>/update', views.QuestionUpdateView.as_view(), name='question-update'),
]

