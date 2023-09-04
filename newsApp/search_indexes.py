from haystack import indexes
from .models import MyNew


class MyNewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # 使用数据模板去建立索引文件

    def get_model(self):
        return MyNew

    def index_queryset(self, using=None):
        return self.get_model().objects.all();