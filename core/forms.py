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
        fields = ['titulo', 'subtitulo','descricao', 'data_campanha', 'status', 'fk_idlocal']
        
        widgets = {
            'subtitulo': forms.Textarea(attrs={
                'rows': 2, 
                'placeholder': 'Escreva aqui o subtitulo da campanha...',
                'class': 'textarea-input',
                'style': 'height: auto;'
            }),
            # Transforma o input padrão em uma caixa de texto maior (Textarea)
            'descricao': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Escreva aqui os detalhes da campanha...',
                'class': 'textarea-input',  # Adicione suas classes CSS aqui, se houver
                'style': 'height: auto;'
            }),

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