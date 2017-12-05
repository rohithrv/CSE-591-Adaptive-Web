from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models import F
from django.views import defaults

from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as alogin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from notes.core import *
from itertools import chain
from django.contrib.auth.views import login

obj = CoreOps()


# obj.getTgasForAllNotes()
def error404(request):
    return render(request, '404.html')


def error500(request):
    return HttpResponseRedirect('login')


def my_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('home')
    else:
        return login(request)


def register(request):
    if request.method == "POST":
        print("hello")
        username = request.POST.get('userid')
        password = request.POST.get('pwd')
        user = User.objects.create_user(username=username, password=password)
        notes.objects.create(type=1, username=username, authorid=username,
                             title="", content="", date=datetime.now())
        user_meta.objects.create(user_id=username)
        alogin(request, user)
        return redirect('home')
    else:
        return render(request, 'register.html')


@login_required
def home(request):
    user_tags = obj.getCBforUser(request.user.get_username())
    user_tags_1 = obj.getCFforUser(request.user.get_username())
    group_tags = obj.getMostusedTags()
    recomemended_cb = notes.objects.filter(noteid__in=user_tags, type=0)
    recomemended_cf = notes.objects.filter(noteid__in=user_tags_1, type=0)
    recomemended = sorted(
        chain(recomemended_cb, recomemended_cf),
        key=lambda instance: instance.date)
    user_notes = notes.objects.filter(username=request.user.get_username()).order_by('-date')[:3]
    tagged_notes = TagNotes.objects.filter(username=request.user.get_username()).order_by('-date')
    myquery = request.GET.get("query")
    # result_list = sorted(
    #     chain(all_public_notes, user_notes),
    #     key=lambda instance: instance.date)
    if myquery:
        recomemended = notes.objects.filter(Q(title__contains=myquery) |
                                                   Q(content__contains=myquery)).distinct()
    context = {'tagged_notes': tagged_notes,
               'navbar': 'home',
               'user_notes': user_notes,
               'r': recomemended,
               'groups': group_tags}
    return render(request, 'new_home.html', context)

@login_required
def displayUserProfile(request):
    if request.method == "POST":
        print("-------POST________________")
    user_name = request.user.get_username()
    context = {}
    static_tags = obj.getTagsForUser(request.user.get_username())
    context = {"tags": static_tags}
    tags = static_tags
    if request.method == "POST":
        saved_tags = request.POST.get('tags')
        print("----------")
        print(saved_tags)
        obj.saveUserPref(request.user.get_username(), saved_tags)
        static_tags = obj.getTagsForUser(request.user.get_username())
        context = {"tags": static_tags}
        return render(request, 'profilePage.html', context)
    return render(request, 'profilePage.html', context)


@login_required
def mynotes(request):
    n = notes.objects.filter(username=request.user.get_username()).order_by('-date')
    tagged_notes = TagNotes.objects.filter(username=request.user.get_username()).order_by('-date')
    myquery = request.GET.get("query")
    if myquery:
        n = n.filter(Q(title__contains=myquery) |
                     Q(content__contains=myquery)).distinct()
    context = {'notes': n, 'tagged_notes': tagged_notes, 'navbar': 'mynotes'}
    return render(request, 'mynotes.html', context)

@login_required
def Discover(request):
    all_public_notes = notes.objects.filter(type=0).order_by('upvote')
    tagged_notes = TagNotes.objects.filter(username=request.user.get_username()).order_by('-date')
    myquery = request.GET.get("query")
    if myquery:
        myquery = myquery.lstrip("Search: ")
        print(myquery)
        l = myquery.split(" ")
        print(l[0], l[1])
        all_public_notes0 = all_public_notes.filter(Q(title__contains=l[0]) |
                                                   Q(content__contains=l[0])).distinct()
        all_public_notes1 = all_public_notes.filter(Q(title__contains=l[1]) |
                                                   Q(content__contains=l[1])).distinct()
        all_public_notes = sorted(
             chain(all_public_notes0, all_public_notes1),
             key=lambda instance: instance.date)
    return render(request,'discover.html', {'notes': all_public_notes, 'navbar': 'discover', 'tagged_notes': tagged_notes })

@login_required
def DeleteCheatsheet(request, id):
    c = CheatSheets.objects.get(user_id=request.user.get_username(), cheatsheet_title=id)
    CheatSheet.objects.filter(user_id=request.user.get_username(), cheatsheet_title=id).delete()
    c.delete()
    return redirect('cheatsheet')

@login_required
def groups(request, pk):
    tagged_notes = TagNotes.objects.filter(username=request.user.get_username()).order_by('-date')
    all_public_notes = notes.objects.filter(type=0).order_by('upvote')
    all_public_notes = all_public_notes.filter(Q(title__contains=pk) |
                                               Q(content__contains=pk)).distinct()[:30]
    return render(request, 'groups.html', {'notes': all_public_notes, 'tagged_notes': tagged_notes, 'gname': pk})

@login_required
def Cheatsheet(request):
    cn = CheatSheet.objects.filter(user_id=request.user.get_username())
    c = CheatSheets.objects.filter(user_id=request.user.get_username())
    tagged_notes = TagNotes.objects.filter(username=request.user.get_username()).order_by('-date')
    n = notes.objects.all()
    if request.method == "POST":
        ctitle = request.POST.get('ctitle')
        CheatSheets.objects.create(cheatsheet_title=ctitle, user_id=request.user.get_username())
        return redirect('cheatsheet')
    context = {'tagged_notes': tagged_notes, 'navbar': 'cheatsheet', 'c': c, 'cn': cn, 'n': n}
    return render(request, 'cheatsheet.html', context)

@login_required
def NoteDetail(request, pk):
    obj.userOpenedNote(request.user.get_username(), pk)
    # updates your tags , call only when user openes others notes
    CB_title_tags, CB_note_tags = obj.getCBforNote(pk)
    print(CB_title_tags)
    # for any note, results will contain mynotes also, filter it
    title_rec = notes.objects.filter(noteid__in=CB_title_tags, type=0)
    content_rec = notes.objects.filter(noteid__in=CB_note_tags, type=0)
    n = notes.objects.get(noteid=pk)
    c = CheatSheets.objects.filter(user_id=request.user.get_username())
    try:
        cn = CheatSheet.objects.filter(note_id=pk)
    except CheatSheet.DoesNotExist:
        cn = None
    try:
        lm = Likes.objects.filter(noteid=pk, voted_user=request.user.get_username())

    except Likes.DoesNotExist:
        lm = None
    if not lm:
        context = {'notes': n, 'Likes': None, 'title_rec': title_rec, 'content_rec': content_rec,'c': c, 'cn': cn}
    else:
        context = {'notes': n, 'Likes': lm, 'title_rec': title_rec, 'content_rec': content_rec, 'c': c, 'cn': cn}
    return render(request, 'note_detail.html', context)

@login_required
def AddToCheat(request, id, pk):
    CheatSheet.objects.create(user_id=request.user.get_username(), cheatsheet_title=id, note_id=pk, date=datetime.now())
    return redirect('note_view', pk=pk)

@login_required
def RemoveFromCheat(request, id, pk):
    cn = CheatSheet.objects.get(user_id=request.user.get_username(), cheatsheet_title=id, note_id=pk)
    cn.delete()
    return redirect('note_view', pk=pk)

@login_required
def NoteCreate(request):
    tagged_notes = TagNotes.objects.filter(username=request.user.get_username()).order_by('-date')
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
        return render(request, 'create_note.html', {'navbar': 'note_create', 'tagged_notes': tagged_notes})

@login_required
def NoteEdit(request, pk):
    mynote = get_object_or_404(notes, noteid=pk)
    tagged_notes = TagNotes.objects.filter(username=request.user.get_username()).order_by('-date')
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
        obj.saveTheNote(pk, edited_note.title, edited_note.content)
        return redirect('mynotes')
    else:
        return render(request, 'edit_note.html',
                      {'navbar': 'note_update', 'mynote': mynote, 'tagged_notes': tagged_notes})


# def SearchQuery(request):
#     myquery=request.GET.get("query")

# class NoteEdit(UpdateView):
#     model = notes
#     fields = ['type', 'title', 'content']
#     success_url = reverse_lazy('mynotes')

@login_required
def NoteDelete(request, pk):
    edited_note = notes.objects.get(noteid=pk)
    edited_note.delete()
    notemeta = note_meta.objects.get(note_id=pk)
    notemeta.delete()
    return redirect('mynotes')

@login_required
def NoteTag(request, pk):
    tag_this_note = notes.objects.get(noteid=pk)
    set_tag = notes.objects.get(noteid=pk)
    set_tag.tagged = 1;
    set_tag.save()
    TagNotes.objects.create(username=request.user.get_username(), noteid=tag_this_note.noteid,
                            title=tag_this_note.title, content=tag_this_note.content, date=datetime.now())
    return redirect('home')

@login_required
def NoteUnTag(request, pk):
    tag_this_note = TagNotes.objects.get(noteid=pk)
    set_tag = notes.objects.get(noteid=pk)
    set_tag.tagged = 0;
    tag_this_note.delete()
    set_tag.save()
    return redirect('home')

@login_required
def NoteUp(request, pk):
    upvote = notes.objects.get(noteid=pk)
    upvote.upvote += 1;
    upvote.save()
    Likes.objects.create(voted_user=request.user.get_username(), noteid=pk)
    return redirect('note_view', pk=pk)

@login_required
def NoteDown(request, pk):
    downvote = notes.objects.get(noteid=pk)
    downvote.downvote += 1;
    downvote.save()
    Likes.objects.create(voted_user=request.user.get_username(), noteid=pk)
    return redirect('note_view', pk=pk)