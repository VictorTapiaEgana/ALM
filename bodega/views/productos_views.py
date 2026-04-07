from django.shortcuts import render


def crear_producto(request):
    
    if request.method == 'GET':

        context = {
            'title': 'Crear Producto'
        }

        return render(request, 'productos/crear_producto.html', context)

    elif request.method == 'POST':        
        pass