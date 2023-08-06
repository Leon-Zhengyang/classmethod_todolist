# get all todos
def get_all_todo(todo_lists):
    todo_arr = []
    for todo in todo_lists:
        todo_arr.append({
            "id": todo.id,
            "title":todo.title,
            "content": todo.content
        })
    return todo_arr