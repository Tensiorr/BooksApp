from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add', views.AddView.as_view(), name='add'),
    path('<uuid:pk>/', views.DetailView.as_view(), name='detail'),
    path('edit/<uuid:pk>', views.EditView.as_view(), name='edit'),
]