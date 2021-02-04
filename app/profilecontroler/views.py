from django.shortcuts import render,reverse
from app import models
from django.http import HttpResponse
from module.gmail import sending
import uuid
from django.http import HttpResponseRedirect
from errno import ENETUNREACH

def profile(request):
    sesi=request.session['user']
    user=models.User.objects.get(username=sesi)
    return render(request,'app/profile.html',{'data':user,'userlogin':user.nama})

def mybook(request):
    sesi=request.session['user']
    user=models.User.objects.get(username=sesi)
    nama=user.nama
    book=models.Buku.objects.filter(user=user)

    return render(request,'app/mybook.html',{'book':book,'userlogin':nama})    

def upaccount(request,id):
    data=models.User.objects.get(id=id)
    if request.method == 'POST':
        name=request.POST['name']
        username=request.POST['username']
        password=request.POST['password']

        up=models.User.objects.filter(id=id)
        check=models.User.objects.filter(username=username)
    
        if check:
           return HttpResponse('pilih username yang lain')
        up.update(nama=name,username=username,password=password)

        try:
            del request.session['user']
        except:
            return HttpResponse('erorr session')  

        request.session['user'] = username    
        return HttpResponseRedirect(reverse('profile'))
    
    return render(request,'app/upaccount.html',{'data':data})
