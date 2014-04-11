# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from StackSmash.apps.uploader.models import Document
from StackSmash.apps.uploader.forms import DocumentForm


def list(request):
    # Make sure the user is authenticated and able to modify the blog
    if not request.user.is_superuser:
        raise Http404

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('upload:list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'uploader/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def delete(request, pk):
    # Make sure the user is authenticated and able to modify the blog
    if not request.user.is_superuser:
        raise Http404

    Document.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('list'))
