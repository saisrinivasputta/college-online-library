from django.contrib import admin
from .models import Student,Book,IssuedBook,Borrower
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book,BookAdmin)

class IssuedBookAdmin(admin.ModelAdmin):
    pass
admin.site.register(IssuedBook,IssuedBookAdmin)

admin.site.register(Student)
admin.site.register(Borrower)