from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Campanha, Usuario

class UsuarioCadastroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email', 'cidade', 'estado', 'foto']
        
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'cidade', 'estado', 'foto']

class CampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = ['titulo', 'data_campanha', 'status', 'fk_idlocal']
        
        widgets = {
            # Transforma o input de texto simples em um calendário real (YYYY-MM-DD)
            'data_campanha': forms.DateInput(attrs={'type': 'date'}),
            
            # Cria as opções exatas que você já tem salvas no banco
            'status': forms.Select(choices=[
                ('Pendente', 'Pendente'),
                ('Entregue', 'Entregue'),
            ]),
            
            # O Django transforma automaticamente as FKs em caixas de seleção (Dropdown)
            'fk_idlocal': forms.Select(),
        }