from django.contrib import admin
from vault.models import Project, Secret


class SecretInline(admin.TabularInline):
    model = Secret
    extra = 2


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
        # Date info is auto generated
        #('Date Information', {'fields': ['create_date', 'modified_date']})
    ]
    inlines = [SecretInline]
    list_display = ['name']
    list_filter = ['create_date']
    search_fields = ['name']
    date_hierarchy = 'create_date'


admin.site.register(Project, ProjectAdmin)
