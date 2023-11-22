from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

def min_length_validator(value):
    if len(value) < 20:
        raise ValidationError('A descrição deve ter pelo menos 20 caracteres.')

class Tarefa(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(validators=[min_length_validator])
    autor = models.CharField(max_length=100)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo