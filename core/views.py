from django.shortcuts import render, redirect, get_object_or_404
from .models import Campanha, Usuario
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CampanhaForm, UsuarioCadastroForm, EditarPerfilForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def home(request):
    return render(request, 'index.html')

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UsuarioCadastroForm()
        
        
def ong_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verifica se o usuário está logado e se é uma ONG
        if request.user.is_authenticated and request.user.tipo_perfil == 'ONG':
            return view_func(request, *args, **kwargs)
        
        # Se for um Doador, redireciona para o dashboard comum ou nega o acesso
        return redirect('dashboard')  # Ou: raise PermissionDenied
    return _wrapped_view
        
    return render(request, 'cadastro.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
    else:
            form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'private/dashboard.html')

@login_required
def ListarCampanhas(request):
    campanha = Campanha.objects.all()
    context = {
        "campanhas": campanha,
    }
    
    return render(request, 'private/regist_campanha.html', context)

@login_required
@ong_required
def CadastrarCampanha(request):
    form = CampanhaForm(request.POST or None)
    if form.is_valid():
        # Intercepta o salvamento automatico
        campanha = form.save(commit=False)
        campanha.fk_iddoador = request.user
        
        campanha.save()
        return redirect('registro-campanha')
    context = {
        'form':form
    }
    return render(request, 'private/cadastrar_campanha.html', context)

@login_required
def EditarCampanha(request, id):
    campanha = campanha.objects.get(pk=id)
    
    if campanha.fk_iddoador != request.user:
        return redirect('registro-campanhas')
    
    form = CampanhaForm(request.POST or None, instance=campanha)
    
    if form.is_valid():
        form.save()
        return redirect('registro-campanhas')
    context = {
        'form': form
    }
    return render(request, 'private/cadastrar_campanha.html', context)

@login_required
def RemoverCampanha(request, id):
    campanha = Campanha.objects.get(pk=id)
    
    if campanha.fk_iddoador != request.user:
        return redirect('registro-campanha')
    
    campanha.delete()
    return redirect('registro-campanha')
    
@login_required
def ListarDoadores(request):
    usuario = Usuario.objects.all()
    context = {
        "usuario": usuario,
    }
    
    return render(request, 'private/doadores.html', context)

@login_required
def PerfilDoador(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    context = {
        'usuario': usuario,
    }
    return render(request, 'private/perfil.html', context)

@login_required
def MeuPerfil(request):
    return render(request, 'private/meu_perfil.html')

@login_required
def EditarPerfil(request):
    if request.method == 'POST':    
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('meu-perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'private/editar_perfil.html', context)

def DetalheCampanha(request, id):
    campanha = get_object_or_404(Campanha, pk=id)
    context = {
        "campanha": campanha,
    }
    return render(request, 'private/detalhes_campanha.html', context)