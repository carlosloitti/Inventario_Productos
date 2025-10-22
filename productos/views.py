from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework import generics
from rest_framework import viewsets

# Listar Productos
class ProductoListAPIView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Eliminar Producto
class ProductoDeleteAPIView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Create your views here.
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

class DemoView(ListView):
    model = Producto
    template_name = 'productos/demo.html'
    context_object_name = 'productos' 

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy ('producto-list-html')
    context_object_name = 'producto' 

    def form_valid(self, form):
        """Método moderno para lógico personalizado al eliminacion."""
        producto = self.get_object()
        print("-------------------------------------------------------")
        print(f"DELETE request received - Eliminando producto: {producto.nombre}    (ID: {producto.id})")
        messages.success(self.request, f'El producto {producto.nombre} ha sido eliminado exitosamente.')
        return super().form_valid(form)
    
    def delete(self, request, *args, **kwargs):
        producto = self.get_object()
        print("-------------------------------------------------------")
        print(f'DELETE request received - Eliminando producto: {producto.nombre}    (ID: {producto.id})')
        messages.success(request, f'El producto {producto.nombre} ha sido eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
    
@method_decorator(csrf_exempt, name='dispatch')
class ProductoAjaxView(generics.GenericAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def post(self, request, *args, **kwargs):
        """( Crear un nuevo producto via AJAX)"""
        print("-------------------------------------------------------")
        print("POST request received")
        print(request.body)
        try:
            data = {
                'nombre': request.POST.get('nombre'),
                #'apellido': request.POST.get('apellido'),
                'descripcion': request.POST.get('descripcion', ''),
                'precio': request.POST.get('precio')
            }

            producto = Producto.objects.create(**data)
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                #'apellido': producto.apellido,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                #'creado': producto.creado.strftime('%Y-%m-%d %H:%M:%S') 
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put (self, request, pk, *args, **kwargs):
        """ Actualizar un producto via AJAX"""
        try:
            producto = get_object_or_404(Producto, pk=pk)
            data = json.loads(request.body)

            producto.nombre = data.get('nombre', producto.nombre)
            #producto.apellido = data.get('apellido', producto.apellido)
            producto.descripcion = data.get('descripcion', producto.descripcion)
            producto.precio = data.get('precio', producto.precio)
            producto.save()

            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                #'apellido': producto.apellido,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                'creado': producto.creado.strftime('%Y-%m-%d %H:%M:%S') 
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)