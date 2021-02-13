from django.contrib import admin

# Register your models here.

from . import models
admin.site.register([models.User,models.Leveluser,models.Buku,models.Kategoribuku])
# admin.site.register(models.User)
# admin.site.register(models.Leveluser)
# admin.site.register(models.Buku)
# admin.site.register(models.Kategoribuku)

