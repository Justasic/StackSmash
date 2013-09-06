from django.contrib import admin
from StackSmash.apps.blog.models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ['title']
	list_filter  = ['listed', 'pub_date']
	search_fields = ['title', 'content']
	date_heirachy = 'pub_date'
	save_on_top = True
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)

