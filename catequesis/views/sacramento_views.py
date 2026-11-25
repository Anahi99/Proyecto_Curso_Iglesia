from django.shortcuts import render, get_object_or_404
from catequesis.models.sacramento import Sacramento


def sacramento_list(request):
    sacramentos = Sacramento.objects.all()
    return render(request, 'catequesis/sacramentos/lista.html',
                  {'sacramentos': sacramentos})


def sacramento_detail(request, pk):
    sacramento = get_object_or_404(Sacramento, pk=pk)
    return render(request, 'catequesis/sacramentos/detalle.html',
                  {'sacramento': sacramento})