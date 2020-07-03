from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

from django.utils import timezone
from django.core.validators import RegexValidator

#auto token ganerated___
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
#___


class UserAccountManager(BaseUserManager):
    def create_user(self,username,password=None):
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
    
        return user

    def create_superuser(self,username,password):
        user = self.create_user(
            username=username,
            password=password
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_management_staff = True
        user.is_seller = True
        user.is_customer = True
        user.save(using=self._db)
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64,unique=True)
    first_name = models.CharField(max_length=64,blank=True,null=True)
    last_name = models.CharField(max_length=64,blank=True,null=True)
    email = models.EmailField(verbose_name="Email",max_length=64,unique=True,blank=True,null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(verbose_name="Phone Number",validators=[phone_regex],max_length=15,unique=True,blank=True,null=True)
    date_joined = models.DateTimeField(verbose_name='Date Joined',default=timezone.now)
    last_login= models.DateTimeField(verbose_name='Last Login',auto_now=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=30,null=True,blank=True,default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_management_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs): # Ensures lowercase usernames
        username = self.username
        if username and type(username) in [str]:
            self.username = username.lower()   # Only lower case allowed
        super(UserAccount, self).save(*args, **kwargs)

    def get_full_name(self):
        """" Used to display user's full name """
        return "{}, {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

#a t g___
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)
#___

class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	birth_date = models.DateField(null=True,blank=True)
	bio = models.TextField(max_length=500,null=True,blank=True)
	address = models.CharField(max_length=255,null=True,blank=True)
	about = models.TextField(null=True,blank=True)

	def __str__(self):
		return self.user.username
    
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
