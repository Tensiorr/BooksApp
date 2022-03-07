from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'books', views.BookListView)
app_name = 'books'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add', views.AddView.as_view(), name='add'),
    path('edit/<uuid:pk>', views.EditView.as_view(), name='edit'),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
