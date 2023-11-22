from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Tarefa
from .forms import Tarefaform
from django.contrib import messages
from django.db.models import Q

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