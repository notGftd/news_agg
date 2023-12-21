from django.contrib import admin
from .models import Website1, Website2, Website3

admin.site.site_header = "Yonse News"
admin.site.site_title = "Yonse!"
admin.site.index_title = "Welcome to the Yonse Admin"

class CustomModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('title',)

admin.site.register(Website1, CustomModelAdmin)
admin.site.register(Website2, CustomModelAdmin)
admin.site.register(Website3, CustomModelAdmin)