from django.db import models
from django.contrib.auth.base_user  import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models     import PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, password=None, is_active=True, is_superuser=False, first_name=None, last_name=None):
        if not email:
            raise ValueError('Email Alanı Boş Bırakılamaz!')

        if not password:
            raise ValueError('Şifre Alanı Boş Bırakılamaz!')

        user = self.model(
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.first_name     = first_name
        user.last_name      = last_name
        user.active         = is_active
        user.super_user     = is_superuser
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, first_name=None, last_name=None):
        user = self.create_user(
            email,
            password        = password,
            is_superuser    = True,
            first_name      = first_name,
            last_name       = last_name
        )
        return user

class User(PermissionsMixin, AbstractBaseUser):
    email           = models.EmailField(verbose_name='Email Adresi', unique=True)
    first_name      = models.CharField(verbose_name='Ad', max_length=50)
    last_name       = models.CharField(verbose_name='Soyad', max_length=50)
    super_user      = models.BooleanField(verbose_name='Süper Kullanıcı', help_text='Süper kullanıcı tüm yetkilere sahiptir.', default=False)
    active          = models.BooleanField(verbose_name='Aktif', default=True)

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_superuser(self):
        return self.super_user
    
    @property
    def is_staff(self):
        return True if self.super_user else False
 
    class Meta:
        db_table            ='user'
        managed             = True
        verbose_name        = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

class Task(models.Model):

    TO_DO = 'to_do'
    DONE  = 'done'

    STATUS = (
        (TO_DO,'YAPILACAK'),
        (DONE, 'TAMAMLANDI')
    )
    status              = models.CharField(max_length=100, verbose_name="Durum")
    assigned_user       = models.ForeignKey(User,verbose_name='Görevin Atandığı Kullanıcı',related_name='tast_assigned_user', on_delete=models.CASCADE,null=True,blank=True)
    title               = models.CharField(max_length=100,verbose_name='Başlık')
    description         = models.CharField(max_length=4000,verbose_name='Açıklama')
    created_at          = models.DateTimeField(auto_now_add=True,verbose_name='Oluşturulduğu Tarih')
    completed_at        = models.DateTimeField(null=True,blank=True,verbose_name='Tamamlandığı Tarih')
    created_by          = models.ForeignKey(User,verbose_name='Görevi Atayan Kullanıcı', related_name='tast_created_by',on_delete=models.CASCADE)

    class Meta:
        db_table                = 'task'
        managed                 = True
        verbose_name            = 'Görev'
        verbose_name_plural     = 'Görevler'
