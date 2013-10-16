from django.contrib import admin
from StackSmash.apps.projects.models import Project

#def clear_cache(modeladmin, request, queryset):
	#num_rows = 0
	
	#if num_rows == 0:
		#self.message_user(request, "No cache to clear.")
	#else:
		#self.message_user(request, "%s cached items were cleared" % num_rows)

class ProjectAdmin(admin.ModelAdmin):
	list_display = ['name']
	list_filter  = ['start_date', 'completion_date']
	search_fields = ['name', 'description']
	date_heirachy = 'start_date'
	save_on_top = True
	prepopulated_fields = {"slug": ("name",)}
	#actions=[clear_cache]
	

admin.site.register(Project, ProjectAdmin)
