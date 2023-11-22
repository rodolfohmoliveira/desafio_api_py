from django import forms

from .models import Tarefa

class Tarefaform(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao']