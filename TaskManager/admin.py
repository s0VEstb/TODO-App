from django.contrib import admin
from TaskManager.models import Status, Task


admin.site.register(Status)

# Register your models here.
@admin.register(Task)
class StatusTask(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'status')
    list_editable = ('title', 'status')
    list_filter = ('created_at', 'status')
    search_fields = ('title', 'status')
    readonly_fields = ('created_at', 'updated_at', 'id')
    fields = ('id', 'title', 'description', 'status')

