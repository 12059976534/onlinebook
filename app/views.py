from django.shortcuts import render,reverse
from . import models
from django.http import HttpResponse
from module.gmail import sending
import uuid
from django.http import HttpResponseRedirect
from errno import ENETUNREACH

from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.http import FileResponse, Http404


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


# Create your views here.
def index(request):
    data=models.Buku.objects.all()
    kategori=models.Kategoribuku.objects.all()
    return render(request,'app/index.html',{'data':data,'kategori':kategori})

def bacabuku(request,id):
    kategori=models.Kategoribuku.objects.all()
    data=models.Buku.objects.filter(kategori=id)
    return render(request,'app/bacabuku.html',{'data':data,'kategori':kategori})    

def baca(request,id):
    data=models.Buku.objects.get(id=id)
    buku=data.files
    opendata='static/file/pdf/'+buku
    try:
        return FileResponse(open(opendata, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def register(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        palidpassword=request.POST['passwordpalid']
        kode =request.POST.get('sandi')
    

        global nama,mail,user,pas,palid,kodeku
        kodeku=kode
        print("code hiden form:",kodeku)
        print(type(kodeku))
        nama=name
        mail=email
        user=username
        pas=password
        palid=palidpassword

        def my_random_string(string_length=10):
            """Returns a random string of length string_length."""
            random = str(uuid.uuid4()) # Convert UUID format to a Python string.
            random = random.upper() # Make all characters uppercase/membuat semua  karak ter menjadi hurup besar.
            random = random.replace("-","") # Remove the UUID '-'.
            return random[0:string_length] # Return the random string.

        global cod 
        cod=[]
        code=my_random_string(6)
        cod.clear()
        cod.append(code)
        codeperivikasi="haii "+name+"berikut kode veripikasi anda "+code
        
        subjek='verivikasi'

        data=models.User.objects.filter(nama=name)
        if data:
            return HttpResponse("pilih nama yang lain")
        data=models.User.objects.filter(email=email)    
        if data:
            return HttpResponse("email telah terdaptar")
        try:
            # tricky code goes here
            sending.kirim(str(codeperivikasi),subjek,email)
            return HttpResponseRedirect(reverse('palidacount'))
        except IOError as e:
            # an IOError exception occurred (socket.error is a subclass)
            if e.errno == ENETUNREACH:
                # now we had the error code 101, network unreachable
                return HttpResponse("101")
            else:
                return HttpResponse("no internet conection") 
           
    return render(request,'app/register.html')

def palidacount(request):
    if request.method == 'POST':
        peripikasi=request.POST['peripikasi']
        if cod[0] == peripikasi:
            data=models.User.objects.all()
            if kodeku == '1':   
                level=models.Leveluser.objects.get(id=2)   
                s=models.User(nama=nama,email=mail,username=user,password=pas,leveluser=level) 
                s.save()  
                return HttpResponseRedirect(reverse('login'))
            if data:       
               s=models.User(nama=nama,email=mail,username=user,password=pas) 
               s.save()
               return HttpResponseRedirect(reverse('login'))   
            
            level=models.Leveluser.objects.get(id=2)   
            s=models.User(nama=nama,email=mail,username=user,password=pas,leveluser=level) 
            s.save()  
            return HttpResponseRedirect(reverse('login'))
        pass    
    print(kodeku)
    return render(request,'app/palidacount.html')


def login(request):
    if request.session.has_key('user'):
        return HttpResponseRedirect(reverse('adminku'))
    if request.method == 'POST':
        username=request.POST['username']
        passwords=request.POST['password']

        
        user=models.User.objects.filter(username=username) 
        if user:
            user=models.User.objects.get(username=username)
            if passwords==user.password:
               request.session['user'] = username
               jalur=models.User.objects.get(username=username)
               jal=str(jalur.leveluser)
               if jal == "1":
                     return HttpResponseRedirect(reverse('profile'))
               return HttpResponseRedirect(reverse('adminku'))      
               
            return HttpResponse(" cek password")   

        email=models.User.objects.filter(email=username)
        if email:
            email=models.User.objects.get(email=username)
            if passwords==email.password:
                request.session['user'] = username
                jalur=models.User.objects.get(email=username)
                jal=str(jalur.leveluser)
                if jal == "1":
                     return HttpResponseRedirect(reverse('profile'))
                return HttpResponseRedirect(reverse('adminku'))     
            return HttpResponse("cek password")    
       
        return render(request,'app/login.html')
    return render(request,'app/login.html')

def uploadbuku(request):
    if request.session.has_key('user'):
        if request.method == 'POST' and request.FILES['myfile']:
    
            judul=request.POST['judul']
            penulis=request.POST['penulis']
            kategori=request.POST['kategori']
            penerbit=request.POST['penerbit']
            myfile=request.FILES['myfile']

            # upload file
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            dirs='pdf'
            s=os.path.join(media_root,dirs)

            fs = FileSystemStorage(s)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            print("uploadd file=",uploaded_file_url)
            print("get file name=",filename)
            data=models.Kategoribuku.objects.all()
            idkate=int(kategori)
            kbook=models.Kategoribuku.objects.get(id=idkate)
            sesku=request.session['user']
            usersesi=models.User.objects.get(username=sesku)
            sa=models.Buku(judul=judul,penulis=penulis,penerbit=penerbit,files=filename,kategori=kbook,user=usersesi)
            sa.save()
            ses=models.User.objects.get(username=sesku)
            seid=str(ses.leveluser)
            if seid == "1":
                return HttpResponseRedirect(reverse('mybook'))
            return HttpResponseRedirect(reverse('tablebuku'))
            # end upload
            
        data=models.Kategoribuku.objects.all()
        return render(request,'app/uploadbuku.html',{'data':data})
    return HttpResponseRedirect(reverse('login'))    

def logout(request):
    if request.session.has_key('user'):
        try:
            del request.session['user']
        except:
            return HttpResponse('erorr')    
        return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('index'))    


def updatebuku(request,id):
    data=models.Buku.objects.get(id=id)
    kategori=models.Kategoribuku.objects.all()
    kate=[]
    for i in kategori:
        kate.append(i.kategori)
    kate.remove(str(data.kategori))    
    kate.insert(0,data.kategori)    
    kate={'kategori':kate,'data':data}

    if request.method == 'POST' and request.FILES['myfile']:

        judul=request.POST['judul']
        penulis=request.POST['penulis']
        kategori=request.POST['kategori']
        penerbit=request.POST['penerbit']
        myfile=request.FILES['myfile']
        
        fil=str(data.files)
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        dirs='pdf'
        j=os.path.join(media_root,dirs)
        files=fil
        os.remove(os.path.join(j, files))
        

        media_root = getattr(settings, 'MEDIA_ROOT', None)
        dirs='pdf'
        s=os.path.join(media_root,dirs)
        fs = FileSystemStorage(s)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        k=models.Kategoribuku.objects.get(kategori=kategori)

        models.Buku.objects.filter(id=id).update(judul=judul,penulis=penulis,penerbit=penerbit,files=filename,kategori=k)
        sesku=request.session['user']
        ses=models.User.objects.get(username=sesku)
        iduser=str(ses.leveluser)
        if iduser == "1":
            return HttpResponseRedirect(reverse('mybook'))
        return HttpResponseRedirect(reverse('tablebuku'))

    return render(request,'app/updatebuku.html',kate)




def deletbuku(request,id):
    sesi=request.session['user']
    de=models.User.objects.get(username=sesi)
    lev=str(de.leveluser)

    book=models.Buku.objects.get(id=id)

    if lev == "1": 
        book.delete()
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        dirs='pdf'
        j=os.path.join(media_root,dirs)
        files=book.files
        os.remove(os.path.join(j, files))
        return HttpResponseRedirect(reverse('mybook'))
    book.delete()
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    dirs='pdf'
    j=os.path.join(media_root,dirs)
    files=book.files
    os.remove(os.path.join(j, files))
    return HttpResponseRedirect(reverse('tablebuku'))






def some_view(request):
    from reportlab.lib.units import inch
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))   
    buffer = io.BytesIO()
    my_text = "online book merupakan aplikasi yang menyediakan buku gratis \n setiap orang yang memiliki account online book bebas menyebarkan buku "
    
    c = canvas.Canvas(buffer,)
    
    textobject = c.beginText(2*cm, 29 * cm - 5 * cm)
    ketobject = c.beginText(9*cm, 29.7 * cm - 2 * cm)
    for line in my_text.splitlines(False):
        textobject.textLine(line.rstrip())
    c.drawText(textobject)
    # c.translate(inch,inch)
    # c.line(0,0,0,1.7*inch) pertikal line
    c.line(10,740,8.1*inch,740) #horizon line
    c.line(10,738,8.1*inch,738)
    c.drawString(180, 770, "Data pengembang aplikasi online book")

    datauser=models.User.objects.filter(leveluser=1)
    dataadmin=models.User.objects.filter(leveluser=2)
    semua=models.User.objects.all()
    buku=models.Buku.objects.all()

    data=str(len(buku))
    

    c.drawString(50, 580, "nama:saipul bahri")
    c.drawString(50, 560, "nurhidayati")
    c.drawString(50, 540, "Sopian hariadi")
    c.drawString(50, 520, "muhammad zainuddin")
    c.drawString(50, 500, "Andri wahyu Anugrah")
    
    
    c.save()
  
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    
    
