from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PerfilUsuario

def registro_view(request):
    if request.method == 'POST':
        # Captura de datos del formulario (Campos A-F)
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        edad = request.POST.get('edad')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validación simple de email (Flujo alterno 5a)
        if "@" not in email:
            messages.error(request, "El E-mail no es válido para registrarse.") [cite: 140]
            return render(request, 'core/registro.html')

        try:
            # 1. Crear el usuario base de Django (RF-01)
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = nombre
            user.last_name = apellido
            user.save()

            # 2. Crear el perfil extendido con los datos del TP (RF-02)
            PerfilUsuario.objects.create(user=user, tipo='Tutor') 
            
            return redirect('login')
        except Exception as e:
            messages.error(request, "El nombre de usuario ya existe.")
            
    return render(request, 'core/registro.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        # 1. Captura de datos (Campos A y B del prototipo) [cite: 94]
        usuario_a = request.POST.get('username')
        password_b = request.POST.get('password')

        # 2. El sistema valida el ingreso de los datos [cite: 16, 96]
        user = authenticate(request, username=usuario_a, password=password_b)

        if user is not None:
            # 3. El sistema permite al usuario su ingreso (Postcondición) [cite: 90, 97]
            auth_login(request, user)
            return redirect('menu_principal')
        else:
            # 4. Flujo alterno: mensaje de error (Página 9) [cite: 101]
            messages.error(request, "Usuario y/o contraseña errónea")
            return render(request, 'core/login.html')
            
    return render(request, 'core/login.html')



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login') # Al cerrar sesión, vuelve al inicio

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Nino

@login_required
def alta_nino_view(request):
    if request.method == 'POST':
        # Captura de datos del formulario (Prototipo Pág. 12)
        apellido_a = request.POST.get('apellido')
        nombre_b = request.POST.get('nombre')
        domicilio_c = request.POST.get('domicilio')
        telefono_d = request.POST.get('telefono')
        fecha_e = request.POST.get('fecha_nacimiento')

        try:
            # Creamos el registro en SQL Server vinculado al tutor actual
            nuevo_nino = Nino(
                apellido=apellido_a,
                nombre=nombre_b,
                domicilio=domicilio_c,
                dni=telefono_d,  # Usamos el campo para identificarlo
                fecha_nacimiento=fecha_e,
                tutor=request.user
            )
            nuevo_nino.save()
            
            # Postcondición: Mensaje de éxito
            messages.success(request, "La alta del niño se produjo exitosamente")
            return redirect('menu_principal')
            
        except Exception as e:
            messages.error(request, "Hubo un error al registrar: " + str(e))
            
    return render(request, 'core/alta_nino.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Nino

def modificar_nino_view(request):
    ninos = None
    nino_seleccionado = None
    query = request.GET.get('buscar') # Campo A (Barra de búsqueda)

    # Si el usuario escribió algo en la barra de búsqueda
    if query:
        ninos = Nino.objects.filter(nombre__icontains=query) | Nino.objects.filter(apellido__icontains=query)

    # Si el usuario seleccionó un niño de la lista para editar (por ID)
    id_editar = request.GET.get('id_editar')
    if id_editar:
        nino_seleccionado = get_object_or_404(Nino, id=id_editar)

    # Lógica para GUARDAR los cambios (Botón Aceptar B1)
    if request.method == 'POST':
        id_nino = request.POST.get('id_nino')
        nino = get_object_or_404(Nino, id=id_nino)
        
        nino.apellido = request.POST.get('apellido')
        nino.nombre = request.POST.get('nombre')
        nino.domicilio = request.POST.get('domicilio')
        nino.dni = request.POST.get('dni')
        nino.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        nino.save()
        
        return redirect('menu_principal')

    return render(request, 'core/modificar_nino.html', {
        'ninos': ninos,
        'nino_seleccionado': nino_seleccionado,
        'query': query
    })

@login_required
def eliminar_nino_view(request):
    ninos = None
    nino_a_eliminar = None
    query = request.GET.get('buscar')

    # Buscador similar al de Modificar
    if query:
        ninos = Nino.objects.filter(nombre__icontains=query) | Nino.objects.filter(apellido__icontains=query)

    # Selección del niño a borrar
    id_borrar = request.GET.get('id_borrar')
    if id_borrar:
        nino_a_eliminar = get_object_or_404(Nino, id=id_borrar)

    # Acción de ELIMINAR (Botón Aceptar B1)
    if request.method == 'POST':
        id_nino = request.POST.get('id_nino')
        nino = get_object_or_404(Nino, id=id_nino)
        nino.delete() # El sistema borra el registro en SQL Server
        messages.warning(request, "El registro ha sido eliminado correctamente.")
        return redirect('menu_principal')

    return render(request, 'core/eliminar_nino.html', {
        'ninos': ninos,
        'nino_a_eliminar': nino_a_eliminar,
        'query': query
    })


from django.shortcuts import render, get_object_or_404
from .models import Cuento, Pictograma

def narracion_view(request):
    # Traemos el primer cuento de la base de datos
    cuento = Cuento.objects.first() 
    
    # Traemos todos los pictogramas vinculados a ese cuento específico
    pictogramas = Pictograma.objects.filter(cuento=cuento)
    
    # Pasamos ambos al HTML
    return render(request, 'core/narracion.html', {
        'cuento': cuento,
        'pictogramas': pictogramas
    })



def menu_principal_view(request):
    return render(request, 'core/menu.html')

from django.shortcuts import redirect
from django.utils import timezone
from .models import Reporte, Nino

def finalizar_lectura_view(request):
    # 1. Intentamos buscar al último niño que este tutor dio de alta
    nino = Nino.objects.filter(tutor=request.user).last()
    
    # 2. Si por alguna razón la relación tutor-niño falló, buscamos el primer niño que exista
    # Esto es solo para asegurar que veas datos en tu prototipo ahora mismo
    if not nino:
        nino = Nino.objects.first()

    # 3. Solo si existe un niño en la base de datos, guardamos el reporte
    if nino:
        Reporte.objects.create(
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            nino=nino
        )
        print(f"DEBUG: Reporte guardado para {nino.nombre}") # Verás esto en tu terminal negra
    else:
        print("DEBUG: No se encontró ningún niño en la base de datos para guardar el reporte")

    return redirect('reportes')


def reportes_view(request):
    # Traemos todos los reportes para confirmar que aparecen
    lista_reportes = Reporte.objects.all().order_by('-fecha', '-hora')
    return render(request, 'core/reportes.html', {'reportes': lista_reportes})


def lista_cuentos_view(request):
    cuentos = Cuento.objects.all()
    return render(request, 'core/lista_cuentos.html', {'cuentos': cuentos})

from django.shortcuts import render, get_object_or_404
from .models import Cuento, Pictograma

def narracion_view(request, cuento_id):
    cuento = get_object_or_404(Cuento, id=cuento_id)
    pictogramas = Pictograma.objects.filter(cuento=cuento)
    
    # Guardamos el ID del cuento en la sesión
    request.session['ultimo_cuento_id'] = cuento_id
    
    return render(request, 'core/narracion.html', {
        'cuento': cuento,
        'pictogramas': pictogramas
    })

from django.shortcuts import redirect, render
from django.utils import timezone
from .models import Reporte, Nino, Pictograma
import json # Para manejar los datos JSON que envía el front

def finalizar_lectura_view(request):
    nino = Nino.objects.filter(tutor=request.user).first() or Nino.objects.first()
    
    # Recibimos la lista de pictogramas activados desde el frontend
    pictogramas_activados_nombres = request.POST.get('pictogramas_activados', '[]')
    pictogramas_activados_nombres = json.loads(pictogramas_activados_nombres)
    
    if nino:
        nuevo_reporte = Reporte(
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
            nino=nino
        )
        nuevo_reporte.save() 
        print(f"ÉXITO: Se grabó la lectura de {nino.nombre} en SQL Server")
    else:
        print("DEBUG: No se encontró ningún niño en la base de datos para guardar el reporte")

    # Guardamos la lista de nombres de pictogramas en la sesión para la página de resumen
    request.session['pictogramas_resumen'] = pictogramas_activados_nombres
    
    # Redirigimos a la nueva página de resumen
    return redirect('resumen_lectura')

from PIL import Image
import os
import uuid
from django.conf import settings

def resumen_lectura_view(request):
    nombres_pictogramas = request.session.get('pictogramas_resumen', [])
    cuento_id = request.session.get('ultimo_cuento_id')
    
    # 1. Buscar los objetos en la DB
    pictogramas_encontrados = []
    for nombre in nombres_pictogramas:
        pic = Pictograma.objects.filter(descripcion=nombre, cuento_id=cuento_id).first()
        if pic:
            pictogramas_encontrados.append(pic)

    imagen_generada_url = None

    if pictogramas_encontrados:
        # Configuración de rutas
        base_static = settings.STATICFILES_DIRS[0]
        ruta_img = os.path.join(base_static, 'img')
        ruta_generated = os.path.join(base_static, 'generated_images')
        
        if not os.path.exists(ruta_generated):
            os.makedirs(ruta_generated)

        # 2. CARGAR EL FONDO REALISTA
        # Usamos el mismo fondo del escenario para que sea coherente
        fondo_path = os.path.join(ruta_img, 'fondo_bosque.png')
        if os.path.exists(fondo_path):
            escena_final = Image.open(fondo_path).convert("RGBA")
            # Redimensionamos a un tamaño estándar para el reporte
            escena_final = escena_final.resize((1024, 768)) 
        else:
            # Si no hay fondo, creamos uno verde suave
            escena_final = Image.new('RGBA', (1024, 768), (34, 139, 34, 255))

        # 3. DICCIONARIO DE POSICIONES (Igual que en el JS para que coincida)
        # Multiplicamos los porcentajes por el tamaño de la imagen (1024x768)
        posiciones_reales = {
            # Formato: "palabra": (X, Y, Ancho)
            "casa":       (580, 100, 350), # Al fondo a la derecha
            "abuela":     (720, 300, 110), # Cerca de la casa
            "cazador":    (150, 320, 170), # Entre los árboles a la izquierda
            "lobo":       (30, 420, 230),  # Acechando abajo a la izquierda
            "caperucita": (400, 400, 160), # Centro de la escena
            "flores":     (480, 580, 90),  # En el suelo
            "canasta":    (350, 550, 75),  # Al lado de Caperucita
            "manzanas":   (700, 600, 85)   # En el suelo a la derecha
        }

        # 4. PEGAR LOS PERSONAJES
        for p in pictogramas_encontrados:
            desc = p.descripcion.lower()
            ruta_p = os.path.join(ruta_img, p.tipo_imagen)
            
            if os.path.exists(ruta_p) and desc in posiciones_reales:
                personaje = Image.open(ruta_p).convert("RGBA")
                
                # Obtener config: x, y, ancho
                x, y, ancho = posiciones_reales[desc]
                
                # Calcular alto proporcional
                ratio = ancho / float(personaje.size[0])
                alto = int(float(personaje.size[1]) * float(ratio))
                personaje = personaje.resize((ancho, alto), Image.Resampling.LANCZOS)
                
                # Pegar en la escena usando el canal alfa (transparencia)
                escena_final.paste(personaje, (x, y), personaje)

        # 5. GUARDAR RESULTADO
        nombre_archivo = f"recuerdo_{uuid.uuid4().hex}.png"
        ruta_final = os.path.join(ruta_generated, nombre_archivo)
        escena_final.save(ruta_final)
        
        imagen_generada_url = f"{settings.STATIC_URL}generated_images/{nombre_archivo}"

    # Limpiar sesión para la próxima lectura
    request.session['pictogramas_resumen'] = []
    
    return render(request, 'core/resumen_lectura.html', {
        'imagen_compuesta_url': imagen_generada_url,
        'conteo': len(pictogramas_encontrados)
    })