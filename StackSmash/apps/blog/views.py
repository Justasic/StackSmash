from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.conf import settings
from StackSmash.apps.blog.models import Post, Comment
from StackSmash.apps.docs.views import page
from django import forms
import time
from calendar import month_name
from recaptcha.client import captcha


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]


def make_archive_list():
    if not Post.objects.count():
        return []

    year, month = time.localtime()[:2]
    first = Post.objects.order_by("pub_date")[0]
    fyear = first.pub_date.year
    fmonth = first.pub_date.month
    months = []

    for y in range(year, fyear-1, -1):
        start, end = 12, 0
        if y == year:
            start = month
        if y == fyear:
            end = fmonth-1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months


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
        'months': make_archive_list(),
        'archive': False,
    })

    # render to template
    return render_to_response('blog/posts.html', ctx)


def archive(request, year, month):
    """Monthly archive."""
    posts = Post.objects.filter(pub_date__year=year, pub_date__month=month, listed=True)
    ctx = RequestContext(request, {
        'posts': posts,
        'months': make_archive_list(),
        'archive': True,
        })

    return render_to_response("blog/posts.html", ctx)


def post(request, year, month, slug):
    # Get post object
    post = get_object_or_404(Post, slug=slug,
                             pub_date__year=int(year),
                             pub_date__month=int(month))

        # Only allow non-listed posts to be viewed if you're not authenticated.
    if not request.user.is_authenticated() and not post.listed:
        raise Http404

    comments = Comment.objects.filter(post=post, listed=True)

    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = "Anonymous"

    ctx = RequestContext(request, {
        'post': post,
        'comments': comments,
        'form': CommentForm(initial={'author': username}),
        'months': make_archive_list(),
        })

    # Render to template
    return render_to_response('blog/post.html', ctx)


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

        if request.user.is_authenticated():
            comment.listed = True

        comment.save()

        if request.user.is_authenticated():
            # I would have loved to use reverse() but it refuses to resolve named urls
            # so I use this nasty hack instead.
            return HttpResponseRedirect(reverse('blog:index') + '%d/%.2d/%s/#comments' %
                                        (post.pub_date.year, post.pub_date.month, post.slug))
            #return HttpResponseRedirect(reverse("blog:post", kwargs={
            #    'year': post.pub_date.year,
            #    'month': post.pub_date.month,
            #    'slug': post.slug}) + '#comments')
        else:
            return HttpResponseRedirect(reverse("blog:captcha", args=(post.pk, int(comment.pk),)))


def captcha_check(request, post_pk, pk):
    """ Force a captcha check to prevent spam from comments.
        If the user is logged in (eg. me), auto-approve the
        comment and let it be posted, otherwise force the user
        to answer the captcha or have the post deleted. """
    post = Post.objects.get(pk=post_pk)
    comment = Comment.objects.get(pk=pk)
    if request.user.is_authenticated():
        if not comment.listed:
            comment.listed = True
            comment.save()
        return HttpResponseRedirect(reverse('blog:index') + '%d/%.2d/%s/#comments' %
                                    (post.pub_date.year, post.pub_date.month, post.slug))
    else:
        ctx = RequestContext(request, {
        'google_captcha_api_key': settings.GOOGLE_CAPTCHA_PUBLIC_API_KEY,
        'post': post,
        'comment': comment,
        })

    return render_to_response('blog/captcha.html', ctx)


def captcha_verify(request, post_pk, pk):
    """ Verify the captcha response. If it is invalid,
        inform the user. Otherwise allow the post to be listed. """
    post = Post.objects.get(pk=post_pk)
    comment = Comment.objects.get(pk=pk)

    response = captcha.submit(
        request.POST.get('recaptcha_challenge_field'),
        request.POST.get('recaptcha_response_field'),
        settings.GOOGLE_CAPTCHA_PRIVATE_API_KEY,
        request.META['REMOTE_ADDR'],)

    if response.is_valid:
        comment.listed = True
        comment.save()
        return HttpResponseRedirect(reverse('blog:index') + '%d/%.2d/%s/#comments' %
                                    (post.pub_date.year, post.pub_date.month, post.slug))
    else:
        ctx = RequestContext(request, {
            'google_captcha_api_key': settings.GOOGLE_CAPTCHA_PUBLIC_API_KEY,
            'post': post,
            'comment': comment,
            'captcha_response': "Invalid Captcha.",
        })
        return render_to_response('blog/captcha.html', ctx)


def delete_comment(request, post_pk, pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        if not pk:
            pklst = request.POST.getlist("delete")
        else:
            pklst = [pk]

        post = Post.objects.get(pk=post_pk)
        for pk in pklst:
            Comment.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('blog:index') + '%d/%.2d/%s/#comments' %
                                    (post.pub_date.year, post.pub_date.month, post.slug))


def about(request):
    # just use the docs view from docs/, it's much easier than making a custom view
    return page(request, 'aboutme')
