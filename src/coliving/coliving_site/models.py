from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# try:
#   admin = ColivingUser.objects.get(pk='')
# except:
#   pass

class ColivingUser(AbstractBaseUser):
  name = models.CharField(max_length=100)
  login = models.CharField(max_length=100, primary_key=True, unique=True)
  password = models.CharField(max_length=100)
  contact = models.CharField(max_length=100)
  role = models.DecimalField(max_digits=1, decimal_places=0)

  USERNAME_FIELD = 'login'

  def isAdmin(self):
    return self.role == 0

  def isUser(self):
    return self.role == 1

  def isOrganizer(self):
    return self.role == 2

  def isConsultant(self):
    return self.role == 3

  def __str__(self):
    return str(self.login)

class Request(models.Model):
  title       = models.CharField(max_length=100, null=True, blank=True)
  description = models.CharField(max_length=400)
  adress      = models.CharField(max_length=120)
  freeSpaces  = models.DecimalField(max_digits=2, decimal_places=0, null=True, blank=True)
  state       = models.DecimalField(max_digits=1, decimal_places=0)
  organizer   = models.ForeignKey(ColivingUser, related_name='organizer', on_delete=models.SET_NULL, null=True)
  consultant  = models.ForeignKey(ColivingUser, related_name='consultant', on_delete=models.SET_NULL, null=True)
  user        = models.ForeignKey(ColivingUser, related_name='user', on_delete=models.CASCADE)
  image      = models.FileField(upload_to='images/')

  def __str__(self):
    return str(self.id)

