from django.urls import path
from . import views

urlpatterns = [
    path('', views.atvlist, name="lista-atividade"),
    path('tarefa/<int:id>/', views.tarefaView, name="tarefa-view"),
    path('novatarefa/', views.novatarefa, name="nova-tarefa"),
    path('edit/<int:id>/', views.edittarefa, name="edit-tarefa"),
    path('delete/<int:id>/', views.deleteTarefa, name="deleta-tarefa"),
]
