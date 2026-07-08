from django.shortcuts import render, redirect, get_object_or_404
from .models import Campanha, Usuario, ImagemCampanha, AtualizacaoCampanha
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CampanhaForm, UsuarioCadastroForm, EditarPerfilForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps
import json

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
    return render(request, 'cadastro.html')
        
        
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
    campanhas_ativas = Campanha.objects.filter(fk_iddoador=request.user)
    campanhas_ativas_count = campanhas_ativas.count()
    
    total_doadores = Usuario.objects.filter(tipo_perfil='DOADOR').count()
    total_doacoes = "0,00"
    
    meses_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul']
    meses_valores = [12000, 19000, 15000, 25000, 22000, 30000, 50000]
    
    categorias_labels = ['Alimentos', 'Saúde', 'Educação', 'Outros']
    categorias_valores = [40, 25, 20, 15]
    
    context = {
        'campanhas_ativas': campanhas_ativas,
        'total_doacoes': total_doacoes,
        'total_doadores': total_doadores,
        'campanhas_ativas_count': campanhas_ativas_count,
        'chart_meses_labels': json.dumps(meses_labels),
        'chart_meses_valores': json.dumps(meses_valores),
        'chart_categorias_labels': json.dumps(categorias_labels),
        'chart_categorias_valores': json.dumps(categorias_valores),
    }
    
    return render(request, 'private/dashboard.html', context)

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
    form = CampanhaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        campanha = form.save(commit=False)
        campanha.fk_iddoador = request.user
        campanha.save()
        
        imagens_galeria = request.FILES.getlist('imagens_galeria')
        for imagem in imagens_galeria:
            ImagemCampanha.objects.create(
                fk_idcampanha=campanha,
                imagem=imagem
            )
            
        return redirect('registro-campanhas')
    context = {
        'form': form
    }
    return render(request, 'private/cadastrar_campanha.html', context)

@login_required
def EditarCampanha(request, id):
    campanha = Campanha.objects.get(pk=id)
    
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
        return redirect('dashboard')
    
    campanha.delete()
    return redirect('dashboard')
    
@login_required
def ListarDoadores(request):
    doadores = Usuario.objects.filter(tipo_perfil='DOADOR')
    context = {
        "doadores": doadores,
    }
    
    return render(request, 'private/doadores.html', context)

@login_required
def ListarOngs(request):
    ongs = Usuario.objects.filter(tipo_perfil='ONG')
    context = {
        "ongs": ongs,
    }
    
    return render(request, 'private/ongs.html', context)

@login_required
def PerfilDoador(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    context = {
        'usuario': usuario,
    }
    return render(request, 'private/perfil.html', context)

@login_required
def PerfilOng(request, id):
    ong = get_object_or_404(Usuario, pk=id)
    context = {
        'ong': ong,
    }
    return render(request, 'private/perfil_ong.html', context)

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

@login_required
def adicionar_atualizacao(request, idcampanha):
    campanha = get_object_or_404(Campanha, pk=idcampanha)
    if campanha.fk_iddoador == request.user and request.method == 'POST':
        texto = request.POST.get('texto')
        imagem = request.FILES.get('imagem')
        if texto:
            AtualizacaoCampanha.objects.create(
                campanha=campanha,
                texto=texto,
                imagem=imagem
            )
    return redirect('detalhe-campanha', id=campanha.idcampanha)

@login_required
def editar_atualizacao(request, id_atualizacao):
    atualizacao = get_object_or_404(AtualizacaoCampanha, pk=id_atualizacao)
    if atualizacao.campanha.fk_iddoador == request.user and request.method == 'POST':
        texto = request.POST.get('texto')
        imagem = request.FILES.get('imagem')
        if texto:
            atualizacao.texto = texto
            if imagem:
                atualizacao.imagem = imagem
            atualizacao.save()
    return redirect('detalhe-campanha', id=atualizacao.campanha.idcampanha)

@login_required
def remover_atualizacao(request, id_atualizacao):
    atualizacao = get_object_or_404(AtualizacaoCampanha, pk=id_atualizacao)
    idcampanha = atualizacao.campanha.idcampanha
    if atualizacao.campanha.fk_iddoador == request.user:
        atualizacao.delete()
    return redirect('detalhe-campanha', id=idcampanha)