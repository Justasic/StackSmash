from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from StackSmash.apps.blog.models import Post
from StackSmash.apps.docs.views import page

def index(request):
	# get the blog posts that are published, order by date
	posts = Post.objects.filter(listed=True)

	ctx = RequestContext(request, {
		'posts': posts.order_by('-pub_date'),
		})

	# render to template
	return render_to_response('blog/posts.html', ctx)


def post(request, year, month, slug):
	# Get post object
	post = get_object_or_404(Post, slug = slug,
				 pub_date__year = int(year),
				 pub_date__month = int(month))

	ctx = RequestContext(request, {
		'post': post.render(),
		})

	# Render to template
	return render_to_response('blog/post.html', ctx)


def archives(request, year, month):
	return HttpResponse('Yay!')

def about(request):
	# just use the docs view from docs/, it's much easier than making a custom view
	return page(request, 'aboutme')
