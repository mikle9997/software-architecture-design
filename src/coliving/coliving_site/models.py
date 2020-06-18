from django.db import models
from django.contrib.auth.models import AbstractBaseUser

import hashlib
from sys import getdefaultencoding

def hashString(input):
  return hashlib.md5(input.encode('utf-8')).hexdigest()

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

  def setHashedPassword(self, input):
    self.password = hashString(input)

  def __str__(self):
    return str(self.login)

class Request(models.Model):
  title       = models.CharField(max_length=100, null=True, blank=True)
  description = models.CharField(max_length=400)
  adress      = models.CharField(max_length=120)
  freeSpaces  = models.DecimalField(max_digits=2, decimal_places=0, null=True, blank=True)
  state       = models.DecimalField(max_digits=1, decimal_places=0)
  organizer   = models.ForeignKey(ColivingUser, related_name='organizer', on_delete=models.SET_NULL, null=True)
  user        = models.ForeignKey(ColivingUser, related_name='user', on_delete=models.CASCADE)
  image       = models.FileField(upload_to='images/')
  project     = models.FileField(upload_to='projects/', null=True, blank=True)

  def __str__(self):
    return "{} {} {} {} {}".format(self.id, self.title, self.user, self.organizer, self.state)

try:
  ColivingUser.objects.get(pk='superadmin')
except:
  superadmin = ColivingUser(name='superadmin', login='superadmin', password='', contact='', role=0)
  superadmin.setHashedPassword('rfhectkm')
  superadmin.save()