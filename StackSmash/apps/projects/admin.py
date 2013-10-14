from django.contrib import admin
from StackSmash.apps.projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
	list_display = ['name']
	list_filter  = ['start_date', 'completion_date']
	search_fields = ['name', 'description']
	date_heirachy = 'start_date'
	save_on_top = True
	prepopulated_fields = {"slug": ("name",)}
	

admin.site.register(Project, ProjectAdmin)
