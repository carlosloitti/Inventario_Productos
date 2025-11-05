from django.shortcuts import render
from .models import Usuario
from .serializers import UsuarioSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Usuario
from rest_framework import generics
from django.views import View

# Listar Usuarios
class UsuarioListAPIView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({
                'error': 'Datos inválidos',
                'detalles': serializer.errors
            }, status=400)
        try:
            self.perform_create(serializer)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            return JsonResponse({
                'error': 'Error interno del servidor',
                'detalles': str(e)
            }, status=500)
        


class UsuarioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return JsonResponse(serializer.data, status=200)
        except Exception as e:
            return JsonResponse({
                'error': 'Usuario no encontrado',
                'detalles': str(e)
            }, status=404)
        
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                return JsonResponse({
                    'error': 'Datos inválidos',
                    'detalles': serializer.errors
                }, status=400)
            self.perform_update(serializer)
            return JsonResponse(serializer.data, status=200)
        except Usuario.DoesNotExist:
            return JsonResponse({
                'error': 'Usuario no encontrado'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'error': 'Error interno del servidor',
                'detalles': str(e)
            }, status=500)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return JsonResponse({'detalle': 'Usuario eliminado exitosamente'}, status=204)
        except Usuario.DoesNotExist:
            return JsonResponse({
                'error': 'Usuario no encontrado'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'error': 'Error interno del servidor',
                'detalles': str(e)
            }, status=500)


# Eliminar Usuario
class UsuarioDeleteAPIView(generics.DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Create your views here.
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'

class DemoView(ListView):
    model = Usuario
    template_name = 'usuarios/demo.html'
    context_object_name = 'usuarios' 

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario-list-html')
    context_object_name = 'usuario' 

    def form_valid(self, form):
        """Método moderno para lógica personalizada al eliminar."""
        usuario = self.get_object()
        print("-------------------------------------------------------")
        print(f"DELETE request received - Eliminando usuario: {usuario.nombre} {usuario.apellido} (ID: {usuario.id})")
        messages.success(self.request, f'El usuario {usuario.nombre} {usuario.apellido} ha sido eliminado exitosamente.')
        return super().form_valid(form)
    
    def delete(self, request, *args, **kwargs):
        usuario = self.get_object()
        print("-------------------------------------------------------")
        print(f'DELETE request received - Eliminando usuario: {usuario.nombre} {usuario.apellido} (ID: {usuario.id})')
        messages.success(request, f'El usuario {usuario.nombre} {usuario.apellido} ha sido eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
    
@method_decorator(csrf_exempt, name='dispatch')
class UsuarioAjaxView(generics.GenericAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        """Crear un nuevo usuario vía POST"""
        if request.method != 'POST':
            return JsonResponse({'error': 'Método no permitido'}, status=405)

        data = {
            'nombre': request.POST.get('nombre'),
            'apellido': request.POST.get('apellido'),
            'cedula': request.POST.get('cedula'),
            'email': request.POST.get('email')
        }

        # Validar datos incompletos
        if not all(data.values()):
            return JsonResponse({'error': 'Datos incompletos'}, status=400)

        # Validar duplicados (ejemplo para cédula)
        if Usuario.objects.filter(cedula=data['cedula']).exists():
            return JsonResponse({'error': 'Usuario con esta cédula ya existe'}, status=400)

        # Crear usuario
        try:
            usuario = Usuario.objects.create(**data)
            return JsonResponse({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'cedula': usuario.cedula,
                'email': usuario.email
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, pk, *args, **kwargs):
        """Actualizar un usuario vía AJAX"""
        try:
            usuario = get_object_or_404(Usuario, pk=pk)
            data = json.loads(request.body)

            usuario.nombre = data.get('nombre', usuario.nombre)
            usuario.apellido = data.get('apellido', usuario.apellido)
            usuario.cedula = data.get('cedula', usuario.cedula)
            usuario.email = data.get('email', usuario.email)
            usuario.save()

            return JsonResponse({
                #'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'cedula': usuario.cedula,
                'email': usuario.email
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UsuarioCreateView(View):
    def post(self, request, *args, **kwargs):
        """Crear un nuevo usuario"""
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            cedula = data.get('cedula')
            email = data.get('email')

            # Validar datos
            if not all([nombre, apellido, cedula, email]):
                return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

            # Verificar duplicados
            if Usuario.objects.filter(cedula=cedula).exists():
                return JsonResponse({'error': 'El usuario con esta cédula ya existe'}, status=400)

            # Validar que la cédula sea un número
            if not cedula.isdigit():
                return JsonResponse({'error': 'La cédula debe ser un número válido'}, status=400)

            # Validar formato de email
            if '@' not in email or '.' not in email:
                return JsonResponse({'error': 'El email debe tener un formato válido'}, status=400)

            # Crear usuario
            usuario = Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                email=email
            )

            return JsonResponse({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'cedula': usuario.cedula,
                'email': usuario.email
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
