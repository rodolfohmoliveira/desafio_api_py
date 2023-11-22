import os
import sys
import django

#  Adicione o caminho do diretório principal do projeto ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_rest.settings")
django.setup()

from atividades.models import ProjetoInfo

projeto_info = ProjetoInfo.objects.create(nome="APi de Atividades", descricao="Etapa de desafio")

readme_content = f"# {projeto_info.nome}\n\n{projeto_info.descricao}"

with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)

print(projeto_info)