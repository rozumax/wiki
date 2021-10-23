from django.forms.forms import Form
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django import urls
from . import util
import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


class NewPageForm(forms.Form):
    name = forms.CharField(label="Name")
    context = forms.CharField(label="Context", widget=forms.Textarea)


def newPage(request):
    return render(request, "encyclopedia/newPage.html", {
        "form": NewPageForm()
    })


def editPage(request, title):

    context = util.get_entry(title)

    if context == None:
        return HttpResponseNotFound()
    else:
        default_data = {'name': title, 'context': context}
        newPageForm = NewPageForm(default_data)
        newPageForm.fields['name'].widget.attrs['readonly'] = True
        return render(request, "encyclopedia/editPage.html", {
            "form": newPageForm
    })


def randomPage(request):
    import random
    list_entries = util.list_entries()

    if list_entries:
        title = random.choice(list_entries)
        return HttpResponseRedirect(urls.reverse("wiki", args=[title]))
    else:
        return HttpResponseNotFound()

def wiki(request, title):

    context = util.get_entry(title)

    if context == None:
        return HttpResponseNotFound()
    else:
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "wikiContent": markdown.markdown(context)
        })

def wikiAlreadyExists(request, title):
        wikiContext = f'The article <strong>{title}</strong> already exists. Not saved.'
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "wikiContent": wikiContext
        })


def savePage(request):
    form = NewPageForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest()

    formData = form.cleaned_data

    title = formData["name"]
    title = title.upper()

    if not util.get_entry(title)==None:
        return HttpResponseRedirect(urls.reverse("wikiAlreadyExists", args=[title]))

    util.save_entry(title, formData["context"])
    return HttpResponseRedirect(urls.reverse("wiki", args=[title]))

def saveEditedPage(request):
    form = NewPageForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest()

    formData = form.cleaned_data

    title = formData["name"]
    title = title.upper()

    util.save_entry(title, formData["context"])
    return HttpResponseRedirect(urls.reverse("wiki", args=[title]))


def search(request):

    title = request.GET.get('q')
    title = title.upper().strip()

    list_entries = util.list_entries()

    if title in list_entries:
        return HttpResponseRedirect(urls.reverse("wiki", args=[title]))
    else:

        entries = []

        for entry in list_entries:
            if not entry.find(title) == -1:
                entries.append(entry)

        return render(request, "encyclopedia/search.html", {
            "entries": entries
        })

        