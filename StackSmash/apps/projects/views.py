from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.core.cache import cache
from django.template import loader
from StackSmash.apps.projects.models import Project
import os


def index(request):
    # Get all projects and order them by start date. This may change later
    # but for now it works.
    projects = Project.objects.all()

    ctx = RequestContext(request, {
        'projects': projects.order_by('-start_date'),
    })

    # render to template
    return render_to_response('projects/projects.html', ctx)


def detail(request, slug):
    # Get post object
    project = get_object_or_404(Project, slug=slug)

    ctx = RequestContext(request, {
        'project': project,
    })

    return render_to_response('projects/project.html', RequestContext(request, ctx))
