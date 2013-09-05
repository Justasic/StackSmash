from django.shortcuts import render, get_object_or_404
from apps.blog.models import Post

def index(request):
	# get the blog posts that are published
	posts = Post.objects.filter(listed=True)
	# render to template
	return render(request, 'blog/posts.html', {'posts': posts})


def post(request, slug):
	# Get post object
	post = get_object_or_404(Post, slug=slug)
	# Render to template
	return render(request, 'blog/post.html', {'post': post})
