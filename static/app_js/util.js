import * as va from './var.js'

// get cookie
export function getCookie(name){
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

// get all todolist
export function get_all_todo(){
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
            create_html(todo_json); 
        })
}

// check title and content blank
export function regist_todo_validate(){
      if(!va.content_regist.value.length > 0 || !va.title_regist.value.length > 0){
            va.error_msg.innerText = "タイトルと内容を両方入力してください"
            return false
      }else{
            return true
      }
}

// regist new todo API
export function regist_todo(){
      const data = {
            title: va.title_regist.value,
            content: va.content_regist.value,
      };
      fetch(`/api/todo_items/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken'),
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (response.status == 201) {
                  va.title_regist.value = ""
                  va.content_regist.value = ""
            }
            return response.json();
        })
        .then(todo_json => {
            if("error" in todo_json){
                  va.error_msg.innerText = todo_json["error"]
            }else{
                  create_html(todo_json)
                  va.error_msg.innerText = ""
            }
        })
        .catch(e => {
            console.log(e)
        })
}

// check title and content
export function check_inputs(){
      if(va.title_regist.value.length > 0 && va.content_regist.value.length > 0){
            va.regist_btn.style.backgroundColor = "#006FD5"
            va.regist_btn.disabled = false
      }else{
            va.regist_btn.style.backgroundColor = "#c7c7c7"
            va.regist_btn.disabled = true
      }
}

// todo list 一覧描画
export function create_html(todo_json){
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
      va.list_table.innerHTML = tr_html
}
