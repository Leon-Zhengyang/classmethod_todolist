// edit todo
function editRow(obj){
      let objtr = obj.parentNode.parentNode
      let row_id = objtr.sectionRowIndex
      let todo_id = objtr.querySelector("#todo-id-" + row_id)
      let edit_btn = document.getElementById("edit-btn-" + row_id)
      let todo_list_title = objtr.querySelector("#todo-list-title-" + row_id)
      let todo_list_content = objtr.querySelector("#todo-list-content-" + row_id)
      if(edit_btn.value == "編集"){
            todo_list_title.style.cssText = "border:1px solid #888;"
            todo_list_title.readOnly = false
            todo_list_content.style.cssText = "border:1px solid #888;"
            todo_list_content.readOnly = false
            todo_list_title.focus()
            edit_btn.value = "確定"
      }else{
            const data = {
                  title: todo_list_title.value,
                  content: todo_list_content.value,
            };
            fetch(`/api/todo_items/${todo_id.innerText}/`, {
                  method: "PUT",
                  headers: {
                      "Content-Type": "application/json",
                      "X-CSRFToken": getCookie('csrftoken'),
                  },
                  body: JSON.stringify(data),
              })
              .then(response => {
                  return response.json();
              })
              .then(todo_json => {
                  if("error" in todo_json){
                        alert(todo_json["error"])
                  }
                  get_all_todo()
              })
              .catch(e => {
                  console.log(e)
              })
            todo_list_title.style.cssText = "border:none;"
            todo_list_title.readOnly = true
            todo_list_content.style.cssText = "border:none;"
            todo_list_content.readOnly = true
            edit_btn.value = "編集"
      }
}

// delete todo
function deleteRow(obj){
      let objtr = obj.parentNode.parentNode
      let row_id = objtr.sectionRowIndex
      let id = objtr.querySelector("#todo-id-" + row_id).innerText
      fetch(`/api/todo_items/${id}/`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken'),
            },
        })
        .then(response => {
            if (response.status !== 200) {
                throw new Error("nonono");
            }
            get_all_todo()
        })
}

function getCookie(name){
      let cookie_value = null
      if(document.cookie && document.cookie !== ''){
            let cookies = document.cookie.split(';')
            for(let i=0; i<cookies.length; i++){
                  let cookie = cookies[i].trim()
                  cookie_value = decodeURIComponent(cookie.substring(name.length + 1))
                  break
            }
      }
      return cookie_value
}

function get_all_todo(){
      fetch(`/api/all_list/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken'),
            },
        })
        .then(response => {
            if (response.status !== 200) {
                  let res = this.response
            }
            return response.json();
        })
        .then(todo_json => {
            create_todo_html(todo_json); 
        })
}

// todo list 一覧描画
function create_todo_html(todo_json){
      let tr_html = ""
      for(let key in todo_json){
            if(todo_json[key]){
                  let td_html = ""
                  td_html += "<td hidden id='todo-id-" + key + "'>" +todo_json[key]["id"] + "</td>"
                  td_html += "<td><input id='todo-list-title-" + key + "' type='text' style='border:none' value='" + todo_json[key]["title"] +"' readonly></td>"

                  let com_fill = todo_json[key]["content"].length>0?todo_json[key]["content"]:'&nbsp;'
                  td_html += "<td><input id='todo-list-content-" + key + "' type='text' style='border:none' value='" + com_fill + "' readonly></td>"    

                  let td_delete = "<td id='td-operate'><input type='button' id='edit-btn-" + key + "' value='編集' onclick='editRow(this)'> \
                  <input type='button' id='delete-btn-" + key + "' value='削除' onclick='deleteRow(this)'></td>"
                  tr_html += "<tr>" + td_html + td_delete + "</tr>"
            }
      }
      let list_table = document.querySelector("#list-table tbody")
      list_table.innerHTML = tr_html
}