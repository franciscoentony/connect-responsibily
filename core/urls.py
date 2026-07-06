from django.urls import path
from core.views import *

urlpatterns = [
    path('', home, name="home"),
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login, name='login'),
    
    path('dashboard/', dashboard, name='dashboard'),
    
    path('dashboard/registro-campanhas/', ListarCampanhas, name="registro-campanhas"),
    path('dashboard/registro-campanhas/<int:id>', DetalheCampanha, name='detalhe-campanha'),
    path('dashboard/cadastrar-campanha/', CadastrarCampanha, name="cadastrar-companha"),
    path('dashboard/editar-companha/<int:id>', EditarCampanha, name="editar-campanha"),
    path('dashboard/remover-campanha/<int:id>', RemoverCampanha, name="remover-campanha"),
    
    path('dashboard/doadores/', ListarDoadores, name="doadores"),
    path('dashboard/doador/<int:id>/', PerfilDoador, name='perfil-doador'),
    path('logout/', logout, name='logout'),
    
    path('dashboard/meu-perfil/', MeuPerfil, name="meu-perfil"),
    path('dashboard/meu-perfil/editar/', EditarPerfil, name="editar-perfil")
]