from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from StackSmash.apps.blog.models import Post, Comment
from StackSmash.apps.docs.views import page
from django import forms

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ["post"]

def index(request):
	# get the blog posts that are published, order by date
	posts = Post.objects.filter(listed=True).order_by('-pub_date')
	# Do 8 posts per page. That seems pretty reasonable.
	paginator = Paginator(posts, 8)

	try:
		page = int(request.GET.get("page", '1'))
	except ValueError:
		page = 1

	try:
		posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	ctx = RequestContext(request, {
		'posts': posts,
		})

	# render to template
	return render_to_response('blog/posts.html', ctx)


def post(request, year, month, slug):
	# Get post object
	post = get_object_or_404(Post, slug = slug,
				 pub_date__year = int(year),
				 pub_date__month = int(month))

	comments = Comment.objects.filter(post=post)

	username = None
	if request.user.is_authenticated():
		username = request.user.username

	ctx = RequestContext(request, {
		'post': post,
		'comments': comments,
		'form': CommentForm(initial={'author': username}),
		})

	# Render to template
	return render_to_response('blog/post.html', ctx)

# To do..
def archives(request, year, month):
	return HttpResponse('Yay!')

def add_comment(request, pk):
	"""Add a new comment."""
	p = request.POST

	if p.has_key("body") and p["body"]:
		author = "Anonymous"
		if p["author"]:
			author = p["author"]

		post = Post.objects.get(pk=pk)
		comment = Comment(post=post)
		cf = CommentForm(p, instance=comment)
		cf.fields["author"].required = False

		comment = cf.save(commit=False)
		comment.author = author
		comment.save()
		return HttpResponseRedirect(reverse("post", args=(post.pub_date.year, post.pub_date.month, post.slug,)))

def about(request):
	# just use the docs view from docs/, it's much easier than making a custom view
	return page(request, 'aboutme')
