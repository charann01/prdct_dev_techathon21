from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self,email,username,phone,user_type,password,**other_fields):
        if not email:
            raise ValueError("Email Id is a required field")
        if not username:
            raise ValueError("Username is a required field")
        if not phone:
            raise ValueError("Phone Number is a required field")
        if not user_type:
            raise ValueError("User Type is a required field.")
        user = self.model(email=self.normalize_email(email),username=username,phone=phone,**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,username,phone,password,**other_fields):
        other_fields.setdefault("is_active",True)
        other_fields.setdefault("is_staff",True)
        other_fields.setdefault("is_superuser",True)
        user = self.create_user(email,username,phone,password,**other_fields)
        user.save()
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True,max_length=100)
    phone = models.CharField(max_length=10,unique=True)
    user_choices = (
        ('student','Student'),
        ('teacher','Teacher'),
        ('admin','Admin')
    )
    user_type = models.CharField(max_length=10,choices=user_choices)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone','user_type']
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    def __str__(self):
        return self.email

class TokenModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    token = models.CharField(max_length=16)