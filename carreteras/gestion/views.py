from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Carretera, Tramo, Poblacion, Categoria

def dashboard(request):
    if request.method == 'POST':
        try:
            # LÓGICA PARA AGREGAR CARRETERA
            if 'btn_carretera' in request.POST:
                nom = request.POST.get('nombre_carretera')
                cat_id = request.POST.get('categoria')
                # El método save() de Carretera tiene el límite de 3 locales, 2 nac, etc.
                nueva_c = Carretera(nombre=nom, categoria_id=cat_id)
                nueva_c.full_clean() # Ejecuta la validación de límites
                nueva_c.save()
                messages.success(request, f"Carretera '{nom}' registrada.")

            # LÓGICA PARA AGREGAR TRAMO
            elif 'btn_tramo' in request.POST:
                nuevo_t = Tramo(
                    carretera_id=request.POST.get('carretera'),
                    km_inicio=request.POST.get('km_inicio'),
                    km_fin=request.POST.get('km_fin'),
                    pueblo_inicio_id=request.POST.get('pueblo_inicio'),
                    pueblo_fin_id=request.POST.get('pueblo_fin'),
                    tipo_final=request.POST.get('tipo_final'),
                    confluye_con_id=request.POST.get('confluye_con') or None
                )
                nuevo_t.save()
                messages.success(request, "Transacción de Tramo Exitosa.")
                
        except Exception as e:
            messages.error(request, f"Error de Integridad: {e}")
        return redirect('dashboard')

    context = {
        'tramos': Tramo.objects.all().order_by('carretera', 'km_inicio'),
        'carreteras': Carretera.objects.all(),
        'pueblos': Poblacion.objects.all(),
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'pages/index.html', context)