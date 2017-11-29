from django.urls import reverse_lazy
from django.db.models import Q
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as alogin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from notes.core import *
from itertools import chain

obj = CoreOps()
# obj.getTgasForAllNotes()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('userid')
        password = request.POST.get('pwd')
        user = User.objects.create_user(username=username, password=password)
        alogin(request, user)
        return redirect('new_home')
    else:
        return render(request, 'register.html')


@login_required
def home(request):
    # user_tags = obj.getCBforUser(request.user.get_username())
    all_public_notes = notes.objects.filter(type=0).order_by('date')
    user_notes = notes.objects.filter(username=request.user.get_username()).order_by('-date')[:4]
    tagged_notes = TagNotes.objects.all().order_by('-date')
    myquery = request.GET.get("query")
    # result_list = sorted(
    #     chain(all_public_notes, user_notes),
    #     key=lambda instance: instance.date)
    if myquery:
        all_public_notes = all_public_notes.filter(Q(title__contains=myquery) |
                                                   Q(content__contains=myquery)).distinct()
    context = {'all_notes': all_public_notes,
               'tagged_notes': tagged_notes,
               'navbar': 'home',
               'user_notes': user_notes}
    return render(request, 'new_home.html', context)

def displayUserProfile(request):
    user_name = request.user.get_username()
    context = {}
    if request.method == "POST":
        tags = request.POST.get('tags')
        print(tags)
    return render(request, 'profilePage.html', context)

@login_required
def mynotes(request):
    n = notes.objects.filter(username=request.user.get_username()).order_by('-date')
    tagged_notes = TagNotes.objects.all().order_by('-date')
    myquery = request.GET.get("query")
    if myquery:
        n = n.filter(Q(title__contains=myquery) |
                     Q(content__contains=myquery)).distinct()
    context = {'notes': n, 'tagged_notes': tagged_notes, 'navbar': 'mynotes'}
    return render(request, 'mynotes.html', context)


def CheatSheet(request):
    c = CheatSheet.objects.filter()
    tagged_notes = TagNotes.objects.all().order_by('-date')
    context = {'tagged_notes':tagged_notes,'navbar': 'cheatsheet'}
    return render(request,'cheatsheet.html',context)


def NoteDetail(request, pk):
    obj.userOpenedNote(request.user.get_username(), pk)
    # updates your tags , call only when user openes others notes
    CB_title_tags, CB_note_tags = obj.getCBforNote(pk)
    # for any note, results will contain mynotes also, filter it

    n = notes.objects.get(noteid=pk)
    try:
        lm = Likes.objects.filter(noteid=pk)
    except Likes.DoesNotExist:
        lm = None
    if not lm:
        context = {'notes': n, 'Likes': None}
    else:
        context = {'notes': n, 'Likes': lm}
    return render(request, 'note_detail.html', context)


def NoteCreate(request):

    tagged_notes = TagNotes.objects.all().order_by('-date')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        type = request.POST.get('type')
        date_time = datetime.now()
        tagged_notes = TagNotes.objects.all().order_by('-date')
        notes.objects.create(type=type, username=request.user.get_username(), authorid=request.user.get_username(),
                             title=title, content=content, date=date_time)
        temp = notes.objects.get(authorid=request.user.get_username(),
                             title=title, content=content, date=date_time)
        obj.saveTheNote(temp.noteid, title, content)
        return redirect('mynotes')
    else:
        return render(request, 'create_note.html', {'navbar': 'note_create','tagged_notes': tagged_notes})


def NoteEdit(request, pk):
    mynote = get_object_or_404(notes, noteid=pk)
    tagged_notes = TagNotes.objects.all().order_by('-date')
    # n = notes.objects.get(noteid=pk)
    if request.method == 'POST':
        edited_note = notes.objects.get(noteid=pk)
        edited_note.title = request.POST.get('title')
        edited_note.type = request.POST.get('type')
        edited_note.content = request.POST.get('content')
        edited_note.username = request.user.get_username()
        edited_note.authorid = request.user.get_username()
        edited_note.date = datetime.now()
        edited_note.save()
        return redirect('mynotes')
    else:
        return render(request, 'edit_note.html', {'navbar': 'note_update', 'mynote': mynote, 'tagged_notes': tagged_notes})


# def SearchQuery(request):
#     myquery=request.GET.get("query")

# class NoteEdit(UpdateView):
#     model = notes
#     fields = ['type', 'title', 'content']
#     success_url = reverse_lazy('mynotes')


def NoteDelete(request, pk):
    edited_note = notes.objects.get(noteid=pk)
    edited_note.delete()
    return redirect('mynotes')


def NoteTag(request, pk):
    tag_this_note = notes.objects.get(noteid=pk)
    set_tag = notes.objects.get(noteid=pk)
    set_tag.tagged = 1;
    set_tag.save()
    TagNotes.objects.create(username=tag_this_note.username, noteid=tag_this_note.noteid,
                            title=tag_this_note.title, content=tag_this_note.content, date=datetime.now())
    return redirect('home')


def NoteUnTag(request, pk):
    tag_this_note = TagNotes.objects.get(noteid=pk)
    set_tag = notes.objects.get(noteid=pk)
    set_tag.tagged = 0;
    tag_this_note.delete()
    set_tag.save()
    return redirect('home')


def NoteUp(request, pk):
    upvote = notes.objects.get(noteid=pk)
    upvote.upvote += 1;
    upvote.save()
    Likes.objects.create(voted_user=request.user.get_username(), noteid=pk)
    return redirect('note_view', pk=pk)


def NoteDown(request, pk):
    downvote = notes.objects.get(noteid=pk)
    downvote.downvote += 1;
    downvote.save()
    Likes.objects.create(voted_user=request.user.get_username(), noteid=pk)
    return redirect('note_view', pk=pk)
