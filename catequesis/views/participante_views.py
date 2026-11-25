from django.shortcuts import render, get_object_or_404
from catequesis.models.participante import Participante


def participante_list(request):
    participantes = Participante.objects.all()
    return render(request, 'catequesis/participantes/lista.html',
                  {'participantes': participantes})


def participante_detail(request, pk):
    participante = get_object_or_404(Participante, pk=pk)
    return render(request, 'catequesis/participantes/detalle.html',
                  {'participante': participante})