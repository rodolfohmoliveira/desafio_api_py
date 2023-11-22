from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from .models import Tarefa
from .forms import Tarefaform
from django.contrib import messages
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import TarefaSerializer

@swagger_auto_schema(
    method='get',
    responses={200: 'OK', 403: 'Acesso não autorizado'},
    operation_description='Obter a lista de itens',
    manual_parameters=[
        openapi.Parameter('page_size', in_=openapi.IN_QUERY, description='Tamanho da página', type=openapi.TYPE_INTEGER),
        openapi.Parameter('page', in_=openapi.IN_QUERY, description='Número da página', type=openapi.TYPE_INTEGER),
    ],
)
@api_view(['GET'])
def list_items(request):
    """
    Obtém a lista de itens.
    """
    # Recupera os parâmetros da consulta
    page_size = request.GET.get('page_size', 10)
    page_number = request.GET.get('page', 1)

    # Lógica para obter a lista de itens (exemplo com Tarefa model)
    tarefas_list = Tarefa.objects.all().order_by('-created_at').filter(user=request.user)

    # Configura o paginador
    paginator = Paginator(tarefas_list, page_size)
    
    try:
        # Obtém a página solicitada
        tarefas = paginator.page(page_number)
    except EmptyPage:
        # Se a página estiver fora do intervalo, retorna uma resposta vazia ou uma mensagem adequada
        data = {'message': 'A página solicitada não existe.'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    # Serializa os dados (dependendo de como você tem configurado seus serializers)
    serializer = TarefaSerializer(tarefas, many=True)

    # Retorna os dados serializados
    return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def atvlist(request):
    
    search = request.GET.get('search')
    
    if search:
        tarefas = Tarefa.objects.filter(
            Q(titulo__icontains=search, user=request.user) |
            Q(autor__icontains=search,  user=request.user) |
            Q(descricao__icontains=search,  user=request.user))
    else:
    
        tarefas_list = Tarefa.objects.all().order_by('-created_at').filter( user=request.user)
    
        paginator = Paginator(tarefas_list, 5)
    
        page = request.GET.get('page')
    
        tarefas = paginator.get_page(page)
    
    return render(request, 'atividades/list.html', {'tarefas': tarefas})

@login_required
def tarefaView(request, id):
    tarefa = get_object_or_404(Tarefa, pk=id)
    return render(request, 'atividades/detail.html', {'tarefa': tarefa})


@login_required
def novatarefa(request):
    if request.method == 'POST':
        form = Tarefaform(request.POST)

        if form.is_valid():
            tarefa = form.save(commit=False)  # Não salve ainda, apenas crie a instância
            tarefa.user = request.user
            tarefa.save()  # Agora salve a instância
            return redirect('/')
    else:
        form = Tarefaform()
    return render(request, 'atividades/novatarefa.html', {'form': form})

@login_required
def edittarefa(request, id):
    tarefa = get_object_or_404(Tarefa, pk=id)
    form = Tarefaform(instance=tarefa)

    if request.method == 'POST':
        form = Tarefaform(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'atividades/edittarefa.html', {'form': form, 'tarefa': tarefa})

@login_required
def deleteTarefa(request, id):
    tarefa = get_object_or_404(Tarefa, pk=id)
    tarefa.delete()
    
    messages.info(request, 'Tarefa deletada com sucesso.')
    
    return redirect('/')