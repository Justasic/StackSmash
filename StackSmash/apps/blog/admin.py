from django.contrib import admin
from apps.blog.models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'description']
	list_filter  = ['listed', 'created']
	search_fields = ['title', 'content']
	date_heirachy = 'created'
	save_on_top = True
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)

