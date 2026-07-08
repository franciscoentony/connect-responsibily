# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Campanha(models.Model):
    idcampanha = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to='campanhas/fotos/', blank=True, null=True, verbose_name="Foto de Perfil")
    titulo = models.CharField(max_length=100, null=False, default='')
    subtitulo = models.TextField(null=False, default='')
    descricao = models.TextField(null=False, default='')
    data_campanha = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    fk_iddoador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fk_idlocal = models.ForeignKey('LocalEntrega', on_delete=models.CASCADE, db_column='fk_idlocal')

    class Meta:
        managed = True
        db_table = 'Campanha'

class ImagemCampanha(models.Model):
    idimagem = models.AutoField(primary_key=True)
    fk_idcampanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='imagens', db_column='fk_idcampanha')
    imagem = models.ImageField(upload_to='campanhas/galeria/')

    class Meta:
        managed = True
        db_table = 'ImagemCampanha'

class Usuario(AbstractUser):
    OPCOES_PLANO = [
        ('PADRAO', 'Padrão'),
        ('GOLD', 'Gold'),
        ('PREMIUM', 'Premium'),
    ]
    
    TIPO_PERFIL = [
        ('DOADOR', 'Doador'),
        ('ONG', 'ONG'),
    ]

    nome = models.CharField(max_length=150, verbose_name="Nome Completo")
    foto = models.ImageField(upload_to='doadores/perfis/', blank=True, null=True, verbose_name="Foto de Perfil")
    tipo_perfil = models.CharField(max_length=10, choices=TIPO_PERFIL, default='DOADOR')
    tipo_plano = models.CharField(max_length=20, choices=OPCOES_PLANO, default='PADRAO', verbose_name="Tipo de Plano")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado (Sigla)")
    quantidade_campanhas = models.PositiveIntegerField(default=0, verbose_name="Quantidade de Doações")
    valor_impacto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Impacto Total (R$)")
    esta_ativo = models.BooleanField(default=True, verbose_name="Doador Ativo?")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        managed = True
        ordering = ['-valor_impacto']

    def __str__(self):
        return f"{self.nome} ({self.tipo_plano})"
    

class Item(models.Model):
    iditem = models.AutoField(primary_key=True)
    quantidade = models.IntegerField(blank=True, null=True)
    condicao = models.CharField(max_length=30, blank=True, null=True)
    fk_idcampanha= models.ForeignKey(Campanha, models.DO_NOTHING, db_column='fk_idcampanha', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Item'


class LocalEntrega(models.Model):
    idlocal = models.AutoField(primary_key=True)
    nome_local = models.CharField(max_length=100, blank=True, null=True)
    endereco = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Local_Entrega'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
