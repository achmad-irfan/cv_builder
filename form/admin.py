from django.contrib import admin
from .models import CV, Education,Skill,Experience,Certificate
# Register your models here.

admin.site.register(CV)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Certificate)
