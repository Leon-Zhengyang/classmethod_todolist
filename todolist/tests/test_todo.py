import pytest
from rest_framework.test import APIClient
from todolist.models import Todo

client = APIClient()
@pytest.fixture
def priority_todo_factory(db, todo_factory):

      todo_factory.create(title="todo1", content="content1")
      todo_factory.create(title="todo2", content="content2")
      todo_factory.create(title="todo3", content="content3")

@pytest.mark.django_db
def test_count(priority_todo_factory):
      priority_todo_factory
      count_todo = Todo.objects.all().count()
      assert count_todo == 3

# todo一覧取得
@pytest.mark.django_db
def test_get_all_todo(priority_todo_factory):
      priority_todo_factory
      response = client.get('/api/all_list/')
      assert response.status_code == 200
      assert len(response.json()) == 3

# todo新規作成（成功）
@pytest.mark.django_db
def test_regist_new(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/', {'title': 'new title', 'content': 'new content'}, format='json')
      todo = Todo.objects.get(title='new title', deleted=0)
      assert todo.content == 'new content'
      assert response.status_code == 201
      assert len(response.json()) == 4

# todo新規作成（失敗:タイトルが空白）
@pytest.mark.django_db
def test_regist_fail_blank(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/', {'title': '', 'content': 'new content'}, format='json')
      assert response.status_code == 400
      assert response.json()["error"] == 'スペースを除いて、タイトルを入力してください。'

# todo新規作成（失敗:重複）
@pytest.mark.django_db
def test_regist_fail_double(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/', {'title': "todo1", 'content': "content1"}, format='json')
      assert response.status_code == 409
      assert response.json()["error"] == 'このタイトルは既に登録済み、別のタイトルを登録してください。'

# todo編集（成功）
@pytest.mark.django_db
def test_edit(priority_todo_factory):
      priority_todo_factory
      todo = Todo.objects.get(title='todo1')
      id = todo.id
      response = client.put('/api/todo_items/{0}/'.format(id), {'title': "todo1_update", 'content': "content1_update"}, format='json')
      todo_update = Todo.objects.get(id=id)
      assert todo_update.title == "todo1_update"
      assert todo_update.content == "content1_update"
      assert response.status_code == 200

# todo編集（失敗：タイトルが空白）
@pytest.mark.django_db
def test_edit_fail_blank(priority_todo_factory):
      priority_todo_factory
      todo = Todo.objects.get(title='todo1')
      id = todo.id
      response = client.put('/api/todo_items/{0}/'.format(id), {'title': "", 'content': "content1_update"}, format='json')
      assert response.json()["error"] == 'スペースを除いて、タイトルを入力してください。'
      assert response.status_code == 400

# todo編集（失敗：todo存在しない）
@pytest.mark.django_db
def test_edit_fail_not_exist(priority_todo_factory):
      priority_todo_factory
      response = client.put('/api/todo_items/100/', {'title': "title1_update", 'content': "content1_update"}, format='json')
      assert response.json()["error"] == '該当のtodoが見つかりません!'
      assert response.status_code == 404

# todo編集（失敗：タイトルが重複）
@pytest.mark.django_db
def test_edit_fail_double(priority_todo_factory):
      priority_todo_factory
      todo = Todo.objects.get(title='todo1')
      id = todo.id
      response = client.put('/api/todo_items/{0}/'.format(id), {'title': "todo2", 'content': "content1_update"}, format='json')
      assert response.json()["error"] == 'このタイトルは既に登録済み、別のタイトルを登録してください。'
      assert response.status_code == 409

# todo削除（成功）
@pytest.mark.django_db
def test_delete(priority_todo_factory):
      priority_todo_factory
      todo = Todo.objects.get(title='todo1')
      id = todo.id
      assert todo.deleted == 0
      response = client.delete('/api/todo_items/{0}/'.format(id), format='json')
      todo_deleted = Todo.objects.get(id=id)
      assert todo_deleted.deleted == 1
      assert todo_deleted.title == "todo1"
      assert response.status_code == 200

# todo削除（失敗）
@pytest.mark.django_db
def test_delete_not_exist(priority_todo_factory):
      priority_todo_factory
      response = client.delete('/api/todo_items/100/', format='json')
      assert response.json()["error"] == '該当のtodoが見つかりません!'
      assert response.status_code == 404


# todo検索（成功:titleのみ、件数:3）
@pytest.mark.django_db
def test_search_title_all(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "todo", 'content_search': ""}, format='json')
      assert len(response.json()) == 3
      assert response.status_code == 200

# todo検索（成功:titleのみ、件数:1）
@pytest.mark.django_db
def test_search_title_one(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "todo1", 'content_search': ""}, format='json')
      assert len(response.json()) == 1
      assert response.status_code == 200
      assert response.json()[0]['title'] == 'todo1'
      assert response.json()[0]['content'] == 'content1'

# todo検索（成功:titleのみ、部分一致、件数:1）
@pytest.mark.django_db
def test_search_part_title_one(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "do1", 'content_search': ""}, format='json')
      assert len(response.json()) == 1
      assert response.status_code == 200
      assert response.json()[0]['title'] == 'todo1'
      assert response.json()[0]['content'] == 'content1'

# todo検索（失敗:titleのみ、件数：0）
@pytest.mark.django_db
def test_search_part_title_fail_one(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "todo123", 'content_search': ""}, format='json')
      assert len(response.json()) == 0
      assert response.status_code == 200

# todo検索（成功:contentのみ、件数:3）
@pytest.mark.django_db
def test_search_content_all(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "", 'content_search': "content"}, format='json')
      assert len(response.json()) == 3
      assert response.status_code == 200

# todo検索（成功:contentのみ、件数:1）
@pytest.mark.django_db
def test_search_content_one(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "", 'content_search': "content1"}, format='json')
      assert len(response.json()) == 1
      assert response.status_code == 200
      assert response.json()[0]['title'] == 'todo1'
      assert response.json()[0]['content'] == 'content1'

# todo検索（成功:contentのみ、部分一致、件数:1）
@pytest.mark.django_db
def test_search_content_part_one(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "", 'content_search': "ent1"}, format='json')
      assert len(response.json()) == 1
      assert response.status_code == 200
      assert response.json()[0]['title'] == 'todo1'
      assert response.json()[0]['content'] == 'content1'

# todo検索（失敗:contentのみ、件数：0）
@pytest.mark.django_db
def test_search_content_fail_part_one(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "", 'content_search': "content123"}, format='json')
      assert len(response.json()) == 0
      assert response.status_code == 200

# todo検索（成功:title&content）
@pytest.mark.django_db
def test_search_title_content1(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "todo", 'content_search': "content1"}, format='json')
      assert len(response.json()) == 1
      assert response.status_code == 200
      assert response.json()[0]['title'] == 'todo1'
      assert response.json()[0]['content'] == 'content1'

# todo検索（成功:title&content）
@pytest.mark.django_db
def test_search_title_content2(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "todo1", 'content_search': "content"}, format='json')
      assert len(response.json()) == 1
      assert response.status_code == 200
      assert response.json()[0]['title'] == 'todo1'
      assert response.json()[0]['content'] == 'content1'

# todo検索（成功:title&content）
@pytest.mark.django_db
def test_search_title_content3(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "todo", 'content_search': "content"}, format='json')
      assert len(response.json()) == 3
      assert response.status_code == 200

# todo検索（失敗:title&content、title:yes、content:no）
@pytest.mark.django_db
def test_search_title_content4(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "todo1", 'content_search': "content123"}, format='json')
      assert len(response.json()) == 0
      assert response.status_code == 200

# todo検索（失敗:title&content、title:no、content:yes）
@pytest.mark.django_db
def test_search_title_content5(priority_todo_factory):
      priority_todo_factory
      response = client.post('/api/todo_items/list/',  {'title_search': "todo123", 'content_search': "content1"}, format='json')
      assert len(response.json()) == 0
      assert response.status_code == 200