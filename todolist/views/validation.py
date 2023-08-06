from todolist.models import Todo

class validate:
      @classmethod
      def check_title_blank(cls, title):
            return True if title.strip() else False
      
      @classmethod
      def check_double_title(cls, title):
            todos = Todo.objects.filter(title=title).exclude(deleted=1)
            return False if todos.count() > 0 else True

      @classmethod
      def check_double_edit_title(cls, title, pk):
            todos = Todo.objects.filter(title=title).exclude(deleted=1).exclude(pk=pk)
            return False if todos.count() > 0 else True