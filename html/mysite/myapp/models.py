# by EMILIO
# Contains all the models of the website
# Models are similar to classes or structs
# They are 'containers' of information
# Examples include users and posts
# All models have been imported from MySQL databse


from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.core.files.storage import FileSystemStorage

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

fs = FileSystemStorage(location='media/post_imgs')

# Create your models here.

class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=200)
    type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'images'


class Admin(models.Model):
    user = models.ForeignKey('RegisteredUser', models.DO_NOTHING)
    admin_id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Agent(models.Model):
    user = models.ForeignKey('RegisteredUser', models.DO_NOTHING)
    agent_id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        managed = False
        db_table = 'agent'


class BanList(models.Model):
    user_id = models.IntegerField(primary_key=True)
    ban_length = models.CharField(max_length=45, blank=True, null=True)
    time_remaining = models.CharField(max_length=45, blank=True, null=True)
    registered_user_user = models.ForeignKey('RegisteredUser', models.DO_NOTHING, db_column='Registered_User_user_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ban_list'


class Categories(models.Model):
    category_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('RegisteredUser', models.DO_NOTHING)
    time = models.DateTimeField()
    #approval = models.IntegerField()
    #status = models.CharField(max_length=45)
    description = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=45)
    location = models.CharField(max_length=100)
    image = models.ImageField(storage=fs)
    type = models.CharField(max_length=45, blank=True, null=True)
    thumbnail = ImageSpecField(source='image',
				     processors=[ResizeToFill(286,180)],
				     format='JPEG',
				     options={'quality':100})
    class Meta:
        managed = False
        db_table = 'post'
        unique_together = (('post_id', 'user'),)


class PostApproval(models.Model):
    post = models.OneToOneField(Post, models.DO_NOTHING, primary_key=True)
    admin = models.ForeignKey(Admin, models.DO_NOTHING, blank=True, null=True)
    approval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'post_approval'


class PostStatus(models.Model):
    post = models.OneToOneField(Post, models.DO_NOTHING, primary_key=True)
    status = models.CharField(max_length=45)
    agent = models.ForeignKey(Agent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_status'


class PostSubmit(models.Model):
    post = models.OneToOneField(Post, models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey('RegisteredUser', models.DO_NOTHING)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'post_submit'



class RegisteredUser(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45, unique=True)
    register_date = models.DateField()
    password = models.CharField(max_length=100)
    ban = models.CharField(max_length=45, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = 'password'

    class Meta:
        managed = True
        db_table = 'registered_user'


class UserAuthority(models.Model):
    user = models.ForeignKey(RegisteredUser, models.DO_NOTHING)
    role_name = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'user_authority'
        unique_together = (('role_name', 'user'),)



class Register(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
