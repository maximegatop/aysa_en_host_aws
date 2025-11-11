
from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class TipoOrden(models.Model):

    class Meta:
        verbose_name = "Tipo de Orden"
        verbose_name_plural = "Tipos de Órdenes"

    def __str__(self):
        return "{} - {}".format(self.tipo_orden, self.descripcion)

    tipo_orden = models.CharField('Tipo de orden', max_length=5)
    descripcion = models.CharField('Descripción', max_length=50)
    clase_actividad = models.CharField('Clase_actividad', max_length=5, default="0")
    descripcion_clase_actividad = models.CharField('Descripción actividad', max_length=50)
    depurable = models.SmallIntegerField('Depurable',default=0)
    dias_depuracion = models.SmallIntegerField('Días depuración',default=30)
    orden_terreno = models.SmallIntegerField('Orden de terreno',default=0)
    exportable = models.SmallIntegerField('Exportable',default=1)
    activo = models.SmallIntegerField('Activo',default = 1)


class TipoPersonal(models.Model):
    id_tipo_personal = models.CharField('Id. Tipo Personal',primary_key=True, max_length=5)
    name = models.CharField('Descripción',  max_length=128, unique=True)

    def __str__(self):
        return "{} - {}".format(self.id_tipo_personal, self.name)

    class Meta():
        verbose_name = "Tipo de Personal"
        verbose_name_plural = "Tipos de Personal"

class Contratista(models.Model):
    id_contratista = models.CharField('Id. Contratista',primary_key=True, max_length=5)
    name = models.CharField('Nombre',  max_length=128, unique=True)

    def __str__(self):
        return "{} - {}".format(self.id_contratista, self.name)

    class Meta():
        verbose_name = "Contratista"
        verbose_name_plural = "Contratistas"

class Page(models.Model):
    page = models.CharField(max_length=200)
    descr = models.CharField(max_length=200)
    app = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.descr)

    class Meta():
        verbose_name = "Página disponible"
        verbose_name_plural = "Páginas disponibles"

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=200)
    pages = models.ManyToManyField(Page, blank=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta():
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"


class WorkUnit(models.Model):
    class Meta:
        verbose_name = "Contratista"
        verbose_name_plural = "Contratistas"

    id_workunit = models.CharField('Id. Oficina Comercial',primary_key=True, max_length=5, unique=True)
    name = models.CharField('Descripción',  max_length=128, unique=True)
    coords = models.CharField('Coordenadas hashmap', max_length=20)

    def __str__(self):
        return "{} - {}".format(self.id_workunit, self.name)

    def getHashmap(self):
        return self.coords;
    
    def getfilename(self):
        self._sLogName= str(self.id_workunit) + ".txt"
        return self._sLogName


class EmserUserManager(BaseUserManager):
    def create_user(self, username, email, password,contratista):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Es necesario un nombre de usuario')
        if not email:
            raise ValueError('Es necesario un email para crear el usuario')
        if not password:
            raise ValueError('Es necesario especificar el password')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            contratista=contratista
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username=username,
                                email=email,
                                password=password, contratista=None
                               )
        user.is_admin = True
        user.save(using=self._db)
        return user


class EmserUser(AbstractBaseUser):
    username= models.CharField('Nombre de Usuario', max_length=15, unique=True)
    email = models.EmailField(
        verbose_name='Dirección de Correo Electrónico',
        max_length=255,
        unique=True
    )

    pages = models.ManyToManyField(Page, blank=True,verbose_name='Páginas')
    work_units = models.ManyToManyField(WorkUnit, blank=True,verbose_name='Oficinas')
    groups = models.ManyToManyField(Group, blank=True,verbose_name='Grupos')
    tiposPersonal = models.ManyToManyField(TipoPersonal,blank=True,verbose_name='Tipos de personal')
    tiposOrdenes =  models.ManyToManyField(TipoOrden,blank=True,verbose_name='Tipos de órdenes')
    contratista = models.ForeignKey(Contratista,blank=True,null=True,default=None)

    first_name = models.CharField('Nombre', max_length=64, blank=True, default='')
    last_name = models.CharField('Apellido', max_length=64, blank=True, default='')
    phone_number = models.CharField('Nro Teléfono', max_length=64, blank=True, default='')
    cell_number = models.CharField('Nro Celular', max_length=64, blank=True, default='')
    address = models.CharField('Dirección Postal', max_length=128, blank=True, default='')

    is_active = models.BooleanField('Activo', default=True)
    is_admin = models.BooleanField('Administrador', default=False)

    objects = EmserUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_my_pages(self):
        pages = self.pages.all()
        for g in self.groups.all():
            pages = (pages | g.pages.all()).distinct()
        return pages

    def get_my_oficinas(self):
        oficinas = self.work_units.all()

        return oficinas

    def get_my_pages_strings(self):
        ret = []
        for p in self.get_my_pages():
            ret.append=[p.page]

    def get_full_name(self):
        ret = self.username
        if self.first_name != '' and self.last_name != '':
            ret = "{}, {}".format(self.last_name, self.first_name)
        return ret

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True



    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    class Meta():
        verbose_name = "Usuario"
        verbose_name_plural = " Usuarios"

class ConfigParamsImpExp(models.Model):

    class Meta:
        verbose_name = "Parámetros Importación Exportación"
        verbose_name_plural = "Parámetros Importación Exportación"

    def __str__(self):
        return "{}".format(self.oficina)
    
    oficina =  models.OneToOneField(WorkUnit,  blank=True,null=True, on_delete=models.PROTECT)
    contratista = models.ForeignKey(Contratista, blank=True,null=True, on_delete=models.PROTECT)
    txt_import = models.SmallIntegerField(default=0)
    path_txt_import = models.CharField('directorio importación', max_length=500, blank=True,null=True)
    txt_export = models.SmallIntegerField(default=0)
    path_txt_export = models.CharField('directorio exportación', max_length=500, blank=True,null=True)
    ws_import = models.SmallIntegerField(default=0)
    url_ws_import = models.CharField('url ws importación', max_length=500, blank=True,null=True)
    ws_export = models.SmallIntegerField(default=0)
    url_ws_export = models.CharField('url ws exportación', max_length=500, blank=True,null=True)
    path_txt_backup = models.CharField('directorio backup', max_length=500, blank=True,null=True)
    ftp_import = models.SmallIntegerField(default=0)
    url_ftp_import = models.CharField('url ftp importación', max_length=500, blank=True,null=True)
    dir_ftp_import = models.CharField('dir ftp importación', max_length=500, blank=True,null=True)
    ftp_export = models.SmallIntegerField(default=0)

    url_ftp_export = models.CharField('url ftp exportación', max_length=500, blank=True,null=True)
    dir_ftp_export = models.CharField('dir ftp importación', max_length=500, blank=True,null=True)
    ftp_backup = models.SmallIntegerField(default=0)
    url_ftp_backup = models.CharField('url ftp backup', max_length=500, blank=True,null=True)
    dir_ftp_bkp_import= models.CharField('dir ftp bkp importación', max_length=500, blank=True,null=True)
    
    ftp_user = models.CharField('usuario ftp', max_length=500, blank=True,null=True)
    ftp_user_domain = models.CharField('dominio', max_length=500, blank=True,null=True)
    ftp_user_password = models.CharField('password usuario ftp', max_length=500, blank=True,null=True)
    notificar_ok = models.SmallIntegerField(default=0)
    mails_ok = models.CharField('email ok', max_length=800, blank=True,null=True)
    notificar_error = models.SmallIntegerField(default=0)
    mails_error = models.CharField('email error', max_length=800, blank=True,null=True)


class Prefijo(models.Model):

    class Meta:
        verbose_name = "Prefijo"
        verbose_name_plural = "Prefijos"

    def __str__(self):
        return '{}-{}'.format(self.prefijo,self.descripcion)
    
    prefijo = models.CharField('prefijo',primary_key=True, max_length=5)
    descripcion = models.CharField('descripción', max_length=50)
