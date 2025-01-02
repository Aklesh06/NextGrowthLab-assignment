from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users must have an email')
        
        user = self.model(
            email= self.normalize_email(email),
            username=username
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        
        user.is_admin = True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class RegisterUser(AbstractBaseUser):
    email        = models.EmailField(unique=True, max_length=255)
    username     = models.CharField(unique=True, max_length=100)
    password     = models.CharField(max_length=128)
    is_active    = models.BooleanField(default=True)
    is_admin     = models.BooleanField(default=False)
    date_joined  = models.DateTimeField(verbose_name="data_joined", auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']
    objects = AccountManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class AndroidApp(models.Model):
    Category_Type = [
        ('Education','Education'),
        ('Entertenment','Entertenment'),
        ('E-commerce','E-commerce'),
        ('Communication','Communication'),
    ]

    SubCategory_Type = [
        ('Social Media','Social Media'),
        ('Shopping','Shopping'),
        ('Meeting','Meeting'),
        ('Music','Music'),
    ]
    
    appName     = models.CharField(max_length=50)
    appLink     = models.URLField()
    icon        = models.ImageField(upload_to='icons/')
    category    = models.CharField(max_length=50, choices=Category_Type)
    subCategory = models.CharField(max_length=50, choices=SubCategory_Type)
    points      = models.IntegerField()
    
    def __str__(self):
        return self.appName

class ClientInfo(models.Model):
    
    username = models.CharField(max_length=50)
    screenShot = ArrayField(models.CharField(max_length=200), blank=True)
    appNames = ArrayField(models.CharField(max_length=50), blank=True)
    totalPoints = models.IntegerField(default=0)