from django.urls import path
from .views import index, search, create, update_or_delete

urlpatterns = [
    path("", index.index, name="index"),
    # ToDo一覧取得する(GET)
    path("api/all_list/", index.all_list, name="init_list"),
    # ToDo新規作成する (POST)
    path("api/todo_items/", create.create_todo_item, name="create_todo_item"),
    # ToDoリスト検索する(POST)
    path("api/todo_items/list/", search.get_todo_list, name="get_todo_list"),
    # ToDo更新、削除する (PUT, DELETE)
    path("api/todo_items/<int:pk>/", update_or_delete.todo_item_detail, name="todo_item_detail"),
]