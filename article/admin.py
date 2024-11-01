from django.contrib import admin
from .models import Question
from .models import Answer
from .models import Test

class Questionadmin(admin.ModelAdmin):
    search_fields = ['subject']
class Anweradmin(admin.ModelAdmin):
    search_fields = ['create_date']
class Testadmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Question,Questionadmin)
admin.site.register(Answer,Anweradmin)
admin.site.register(Test,Testadmin)

# Register your models here.
