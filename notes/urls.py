
from django.conf.urls import url, include
from django.contrib.auth import views as aviews
from . import views as myviews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^home/$', myviews.home, name='home'),
    url(r'^mynotes/$', myviews.mynotes, name='mynotes'),
    url(r'^cheatsheet/$', myviews.Cheatsheet, name='cheatsheet'),
    url(r'^addtocheatsheet/(?P<id>.*)/(?P<pk>[0-9]+)/$', myviews.AddToCheat, name='addtocheat'),
    url(r'^removefromcheatsheet/(?P<id>.*)/(?P<pk>[0-9]+)/$', myviews.RemoveFromCheat, name='removefromcheat'),
    url(r'^removecheatsheet/(?P<id>.*)/$', myviews.DeleteCheatsheet, name='removecheat'),
    url(r'^notes/add/$', myviews.NoteCreate, name='note_create'),
    url(r'^notes/discover/$', myviews.Discover, name='discover'),
    url(r'^notes/(?P<pk>[0-9]+)/$', myviews.NoteDetail, name='note_view'),
    url(r'^notes/(?P<pk>[0-9]+)/update/$', myviews.NoteEdit, name='note_update'),
    url(r'^notes/(?P<pk>[0-9]+)/tag/$', myviews.NoteTag, name='note_tag'),
    url(r'^notes/(?P<pk>[0-9]+)/upvote/$', myviews.NoteUp, name='note_upvote'),
    url(r'^notes/(?P<pk>[0-9]+)/downvote/$', myviews.NoteDown, name='note_downvote'),
    url(r'^notes/(?P<pk>[0-9]+)/removetag/$', myviews.NoteUnTag, name='note_untag'),
    url(r'^notes/(?P<pk>[0-9]+)/delete/$', myviews.NoteDelete, name='note_delete'),
    url(r'^$',aviews.login,{'template_name': 'login.html'},name='login'),
    url(r'^logout/$',aviews.logout, {'next_page': 'login'}, name='logout'),
    url(r'^register/$', myviews.register, name='register'),
    # url(r'^summernote/', include('django_summernote.urls')),
    url(r'^profile/$', myviews.displayUserProfile, name='profile'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)