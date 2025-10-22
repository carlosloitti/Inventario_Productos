from django.urls import path, include
from .views import (
    UsuarioDeleteAPIView, UsuarioListAPIView,
    UsuarioListView, UsuarioDeleteView, DemoView, UsuarioAjaxView,
    UsuarioCreateView
)

urlpatterns = [
    path('api/usuarios/', UsuarioListAPIView.as_view(), name='usuario-list-api'),
    path('api/usuarios/<int:pk>/delete/', UsuarioDeleteAPIView.as_view(), name='usuario-delete-api'),

    path('ajax/usuarios/', UsuarioAjaxView.as_view(), name='usuario-ajax'),
    path('ajax/usuarios/<int:pk>/', UsuarioAjaxView.as_view(), name='usuario-ajax-detail'),

    path('usuarios/', UsuarioListView.as_view(), name='usuario-list-html'),
    path('usuarios/<int:pk>/delete/', UsuarioDeleteView.as_view(), name='usuario-delete-html'),
    path('demo/', DemoView.as_view(), name='demo-usuarios'),
    path('', UsuarioListView.as_view(), name='home'),

    path('usuarios/crear/', UsuarioCreateView.as_view(), name='usuario-crear'),
]