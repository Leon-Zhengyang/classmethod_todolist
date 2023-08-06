import factory
from todolist.models import Todo

class TodoFactory(factory.django.DjangoModelFactory):
      class Meta:
            model = Todo

      title = factory.Sequence(lambda n: u'タイトル %d' % n)
      content = factory.Sequence(lambda n: u'内容 %d' % n)