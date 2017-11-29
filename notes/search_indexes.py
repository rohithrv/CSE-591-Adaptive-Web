from haystack import indexes
from .models import *


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    noteid = indexes.PositiveIntegerField(model_attr='noteid')
    authorid = indexes.PositiveIntegerField(model_attr='authorid')
    type = indexes.PositiveIntegerField(model_attr='type')
    username = indexes.CharField(model_attr='username')
    points = indexes.PositiveIntegerField(model_attr='points')
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(document=True, use_template=True)
    date = indexes.DateTimeField(model_attr='date')

    def get_model(self):
        return notes
