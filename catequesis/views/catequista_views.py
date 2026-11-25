from django.shortcuts import render, get_object_or_404
from catequesis.models.catequista import Catequista


def catequista_list(request):
    catequistas = Catequista.objects.all()
    return render(request, 'catequesis/catequistas/lista.html',
                  {'catequistas': catequistas})


def catequista_detail(request, pk):
    catequista = get_object_or_404(Catequista, pk=pk)
    return render(request, 'catequesis/catequistas/detalle.html',
                  {'catequista': catequista})