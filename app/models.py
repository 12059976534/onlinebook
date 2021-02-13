
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Leveluser(models.Model):
    level=models.CharField(max_length=10)    

    def __str__(self):
        return '%s' % (self.level)

class User(AbstractUser):
    nama=models.CharField(max_length=200)
    email=models.EmailField(max_length=200,unique=True)
    username=models.CharField(max_length=300,unique=True)
    password=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True, blank=True,null=True)
    leveluser=models.ForeignKey(Leveluser,on_delete=models.CASCADE,null=True, default=1)


    def __str__(self):
        return " %s %s %s %s " % (self.nama,self.username,self.email,self.leveluser)





class Kategoribuku(models.Model):
    kategori=models.CharField(max_length=10)

    def __str__(self):
        return "%s" % (self.kategori)


class Buku(models.Model):
    files=models.TextField(max_length=False) 
    judul=models.CharField(max_length=250)
    penulis=models.CharField(max_length=250)
    penerbit=models.CharField(max_length=500)
    status=models.BooleanField(default=True)
    ate = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    kategori=models.ForeignKey(Kategoribuku, on_delete=models.CASCADE,null=True )
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True )

    def __str__(self):
        return "%s %s %s %s %s %s" % (self.files,self.judul,self.penulis,self.penerbit,self.kategori,self.user)



