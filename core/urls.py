from django.urls import path
from core.views import *

urlpatterns = [
    path('', home, name="home"),
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login, name='login'),
    
    path('dashboard/', dashboard, name='dashboard'),
    
    path('dashboard/registro-campanhas/', ListarCampanhas, name="registro-campanhas"),
    path('dashboard/registro-campanhas/<int:id>', DetalheCampanha, name='detalhe-campanha'),
    path('dashboard/cadastrar-campanha/', CadastrarCampanha, name="cadastrar-campanha"),
    path('dashboard/editar-companha/<int:id>', EditarCampanha, name="editar-campanha"),
    path('dashboard/remover-campanha/<int:id>', RemoverCampanha, name="remover-campanha"),
    path('dashboard/registro-campanhas/<int:idcampanha>/atualizacao/adicionar/', adicionar_atualizacao, name='adicionar-atualizacao'),
    path('atualizacao/<int:id_atualizacao>/editar/', editar_atualizacao, name='editar-atualizacao'),
    path('atualizacao/<int:id_atualizacao>/remover/', remover_atualizacao, name='remover-atualizacao'),
    
    path('dashboard/ongs/', ListarOngs, name="ongs"),
    path('dashboard/ongs/<int:id>/', PerfilOng, name='perfil-ong'),
    
    path('dashboard/doadores/', ListarDoadores, name="doadores"),
    path('dashboard/doador/<int:id>/', PerfilDoador, name='perfil-doador'),
    
    path('logout/', logout, name='logout'),
    
    path('dashboard/meu-perfil/', MeuPerfil, name="meu-perfil"),
    path('dashboard/meu-perfil/editar/', EditarPerfil, name="editar-perfil")
]