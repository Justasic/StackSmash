from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from StackSmash.apps.blog.models import Post

def index(request):
	# get the blog posts that are published, order by date
	posts = Post.objects.filter(listed=True).order_by('pub_date')
	# render to template
	return render(request, 'blog/posts.html', {'posts': posts})


def post(request, year, month, slug):
	# Get post object
	post = get_object_or_404(Post, slug=slug)
	# Render to template
	return render(request, 'blog/post.html', {'post': post})


def archives(request, year, month):
	return HttpResponse('Yay!')

def about(request):
	return HttpResponse('Yay!')
