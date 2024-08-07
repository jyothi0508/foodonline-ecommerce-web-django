from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser

class NewUserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email,password= None):
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('User must have an username')
        user=self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name= last_name,
            username = username,
        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, first_name, last_name, username, email,password=None) :
        user= self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name= last_name,
            username = username,
            password = password,
        )
        user.is_active = True  
        user.is_staff =  True
        user.is_superuser =  True
        user.is_admin =  True
        user.save()
        return user
class NewUser(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    Role_choices = (
        (VENDOR,'Vendor'),
        (CUSTOMER,'Customer')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150,unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=Role_choices, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    objects = NewUserAccountManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name","last_name"]

    def __str__(self):
        if self.username:
            return self.username
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:  
            user_role = 'Customer'
        return user_role
class UserProfile(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures',blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos',blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    # address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}'
    def __str__(self):
        return self.user.username