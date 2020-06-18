from .models import ColivingUser, hashString

class AuthBackend():

  @staticmethod
  def authenticate(login, password):
    try:
      user = ColivingUser.objects.get(pk = login)
      if user.password == hashString(password):
        return user
      return None
    except:
      return None

  @staticmethod
  def getUser(login):
    try:
      user = ColivingUser.objects.get(pk = login)
      return user
    except:
      return None

