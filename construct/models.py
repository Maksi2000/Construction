from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# from django.db import models
from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE = ((1, "CLIENT"), (2, "ARCHITECT"), (3, "ENGINEER"))
    GENDER = [("M", "Male"), ("F", "Female")]
    
    
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name

phases = (
	('Site clearing','Site clearing'),
	('Foundation','Foundation'),
	('Plinth beam/slab','Plinth beam/slab'),
	('Superstructure','Superstructure'),
	('Brick masonry work','Brick masonry work'),
	('The lintel','The lintel'),
	('Roofing coating','Roofing coating'),
	('Electrical/plumbing','Electrical/plumbing'),
	('Exterior/interior finishing','Exterior/interior finishing'),
	('Flooring','Flooring'),
	('Painting','Painting')
	)

status=(
		('Complete','Complete'),
		('Incomplete','Incomplete'),
		('Onprogress','Onprogress'),
		('Stopped','Stopped')
		)
project_type = (
	('Fire Resistive','Fire Resistive'),
	('Non-Combustible','Non-Combustible'),
	('Ordinary','Ordinary'),
	('Heavy Timber','Heavy Timber'),
	('Wooden Framed','Wooden Framed')
	)

APPROVALS = (
	('approved','approved'),
	('notapproved','notapproved')
	)
class Architect(models.Model):
    admin =models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=False)
    project_type = models.CharField(max_length=500,choices=project_type,null=True)
    project_plans = models.FileField(upload_to='ArchitectProjectPlans/')
    budget=models.PositiveIntegerField(null=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.admin.first_name+" "+self.admin.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.admin.first_name

class Client(models.Model):
    admin =models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=False)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.admin.email +" "+self.admin.gender
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.admin.email      

class Engineer(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=True,blank=True)
    project_type = models.CharField(max_length=500,choices=project_type,null=True)
    project_images = models.FileField(upload_to='EngineerProjectImages/')
    budget=models.PositiveIntegerField(null=True)
    status=models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.admin.first_name+" "+self.admin.last_name
    @property
    def get_id(self):
        return self.admin.id
    def __str__(self):
        return self.admin.first_name


class BaseContent(models.Model):
	title = models.CharField(max_length=150)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True



class ConstructionProjects(models.Model): 
	project_client = models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
	project = models.CharField(max_length=254)
	descrition = models.CharField(max_length=254)
	project_type = models.CharField(max_length=254, choices=project_type)
	phases = models.CharField(max_length=150,choices=phases)
	project_eng = models.ForeignKey(Engineer,on_delete=models.CASCADE,null=True)
	project_architect = models.ForeignKey(Architect, on_delete=models.CASCADE,null=True)
	project_plans = models.FileField(upload_to='project_plans')
	status = models.CharField(max_length=254,choices=status)
	startdate = models.DateField(null=True,blank=True)
	propdate = models.DateField(null=True,blank=True)

	def __str__(self):
		return self.project



class ArchitectTask(models.Model):
	constructionproject = models.ForeignKey(ConstructionProjects,on_delete=models.CASCADE,null=True)
	archictect_plan = models.FileField(upload_to='ArchitectProjectPlans/')
	progress = models.BigIntegerField(null=True,blank=True)
	status = models.CharField(max_length=254,choices=status)
	reply = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)   


	

class EngineerTask(models.Model):
	constructionproject = models.ForeignKey(ConstructionProjects,on_delete=models.CASCADE,null=True)
	eng_report = models.FileField(upload_to='engineerReport/')
	eng_images = models.FileField(upload_to='engineerimages/')
	phases = models.CharField(max_length=150,choices=phases)	
	reply = models.TextField()
	eng_approved = models.CharField(max_length=150,choices=APPROVALS,default="notapproved")
    
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)   


class NotificationEngineer(models.Model):
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackArchitect(models.Model):
    archictect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class NotificationArchitect(models.Model):
    archictect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackEngineer(models.Model):
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Client.objects.create(admin=instance)
        if instance.user_type == 2:
            Architect.objects.create(admin=instance)
        if instance.user_type == 3:
            Engineer.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.client.save()
    if instance.user_type == 2:
        instance.architect.save()
    if instance.user_type == 3:
        instance.engineer.save()






