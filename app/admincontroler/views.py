from django.shortcuts import render,reverse
from app import models
from django.http import HttpResponse
from module.gmail import sending
import uuid
from django.http import HttpResponseRedirect
from errno import ENETUNREACH
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminku(request):
    if request.session.has_key('user'):
      
      sesi=request.session['user']
      uorad=models.User.objects.get(username=sesi)
      data= str(uorad.leveluser)
      if data == '1':
          return HttpResponseRedirect(reverse('profile'))
      user=models.User.objects.get(username=sesi)
      nama=user.nama  
      print("levelll:",user.leveluser,type(user.leveluser))
      datauser=models.User.objects.filter(leveluser=2)
      dataadmin=models.User.objects.filter(leveluser=1)
      semua=models.User.objects.all()
      buku=models.Buku.objects.all()
   
    #   book
      kategori1=models.Kategoribuku.objects.get(kategori='teknik')
      teknik=models.Buku.objects.filter(kategori=kategori1)
      kategori2=models.Kategoribuku.objects.get(kategori='religion')
      religion=models.Buku.objects.filter(kategori=kategori2)
      kategori3=models.Kategoribuku.objects.get(kategori='politik')
      politik=models.Buku.objects.filter(kategori=kategori3)
      history=models.Kategoribuku.objects.filter(kategori='history')
      print('panjang p:',len(politik),'panjang t',len(teknik),'panjang r',len(religion))

      data={
          'userlogin':nama,
          'jumlahuser':len(datauser),
          'jumlahadmin':len(dataadmin),
          'all':len(semua),
          'buku':len(buku),
          'teknik':len(teknik),
          'religion':len(religion),
          'politik':len(politik),
          'hostory':len(history),
          }

      return render(request,'app/admin.html',data)
    return HttpResponseRedirect(reverse('login'))  

def tablebuku(request):
    if request.session.has_key('user'):

        sesi=request.session['user']
        uorad=models.User.objects.get(username=sesi)
        data= str(uorad.leveluser)
        if data == '1':
          return HttpResponseRedirect(reverse('profile'))



        buku=models.Buku.objects.all()
        return render(request,'app/bukutable.html',{'buku':buku})    
    return HttpResponseRedirect(reverse('login'))    

def tableadmin(request):
    if request.session.has_key('user'):

        sesi=request.session['user']
        uorad=models.User.objects.get(username=sesi)
        data= str(uorad.leveluser)
        if data == '1':
          return HttpResponseRedirect(reverse('profile'))



        level=models.Leveluser.objects.get(level=2)
        admin=models.User.objects.filter(leveluser=level)   
        print("tablel adminnnnn id:",level.id)
        return render(request,'app/admintable.html',{'admin':admin})    
    return HttpResponseRedirect(reverse('login'))

def tableuser(request):
    if request.session.has_key('user'):

        sesi=request.session['user']
        uorad=models.User.objects.get(username=sesi)
        data= str(uorad.leveluser)
        if data == '1':
          return HttpResponseRedirect(reverse('profile'))




        level=models.Leveluser.objects.get(level=1)
        userku=models.User.objects.filter(leveluser=level)
        return render(request,'app/usertable.html',{'userku':userku}) 
    return HttpResponseRedirect(reverse('login'))       

def newadmin(request):
    if request.session.has_key('user'):

        sesi=request.session['user']
        uorad=models.User.objects.get(username=sesi)
        data= str(uorad.leveluser)
        if data == '1':
          return HttpResponseRedirect(reverse('profile'))

        return render(request,'app/createadmin.html')    
    return HttpResponseRedirect(reverse('login'))

def updateuser(request,id):
    if request.session.has_key('user'):

        sesi=request.session['user']
        uorad=models.User.objects.get(username=sesi)
        data= str(uorad.leveluser)
        if data == '1':
          return HttpResponseRedirect(reverse('profile'))

        data=models.User.objects.get(id=id)
        if request.method == 'POST':

            name=request.POST['name']
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            passwordpalid=request.POST['passwordpalid']
            models.User.objects.filter(id=id).update(nama=name,username=username,email=email,password=password)
            jalur=models.User.objects.get(id=id)
            dat=str(jalur.leveluser)
            if dat == '1':
                return HttpResponseRedirect(reverse('tableuser'))
            return HttpResponseRedirect(reverse('tableadmin'))      
        return render(request,'app/updateuser.html',{'data':data}) 
    return HttpResponseRedirect(reverse('login'))    

def deletuser(request,id):
    if request.session.has_key('user'):

        sesi=request.session['user']
        uorad=models.User.objects.get(username=sesi)
        data= str(uorad.leveluser)
        if data == '1':
          return HttpResponseRedirect(reverse('profile'))



        de=models.User.objects.get(id=id)
        data=str(de.leveluser)
        if data == "1":
            de.delete()
            return HttpResponseRedirect(reverse('tableuser'))
        de.delete()
        return HttpResponseRedirect(reverse('tableadmin'))
    return HttpResponseRedirect(reverse('login'))    

