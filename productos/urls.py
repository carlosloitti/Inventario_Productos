from django.urls import path, include
from . views import (
    ProductoDeleteAPIView, ProductoDeleteAPIView, ProductoListAPIView,
    ProductoListView, ProductoDeleteView, DemoView, ProductoAjaxView
)

#from . import views

urlpatterns = [
    path('api/productos/', ProductoListAPIView.as_view(), name='producto-list-api'),
    path('api/productos/<int:pk>/delete/', ProductoDeleteAPIView.as_view(), name='producto-delete-api'),   

    path('ajax/productos/', ProductoAjaxView.as_view(), name='producto-ajax'),
    path('ajax/productos/<int:pk>/', ProductoAjaxView.as_view(), name='producto-ajax-detail'),

    path('productos/', ProductoListView.as_view(), name='producto-list-html'),
    path('productos/<int:pk>/delete/', ProductoDeleteView.as_view(), name='producto-delete-html'),
    path('demo/', DemoView.as_view(), name='demo'),
    path('', ProductoListView.as_view(), name='home'),


]