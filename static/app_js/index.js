import * as va from './var.js'
import * as util from './util.js'
window.addEventListener('DOMContentLoaded', () => {
      // show all todolists
      util.get_all_todo()

      // todo create new
      va.regist_btn.addEventListener("click", function(){
            if(util.regist_todo_validate()){
                  util.regist_todo()
            }
      })

      // reset textbox(regist)
      va.reset_regist_btn.addEventListener("click", function(){
            va.title_regist.value = ""
            va.content_regist.value = ""
      })

      // reset textbox(search)
      va.reset_search_btn.addEventListener("click", function(){
            va.title_search.value = ""
            va.content_search.value = ""
      })

      // check title and content
      va.title_regist.addEventListener("keyup", util.check_inputs)
      va.content_regist.addEventListener("keyup", util.check_inputs)
      
      // search todolist
      va.search_btn.addEventListener("click", function(){
            const data = {
                  title_search: va.title_search.value,
                  content_search: va.content_search.value,
            };
            fetch(`/api/todo_items/list`, {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                      "X-CSRFToken": getCookie('csrftoken'),
                  },
                  body: JSON.stringify(data),
              })
              .then(response => {
                  if (response.status !== 200) {
                        let res = this.response
                  }
                  return response.json();
              })
              .then(todo_json => {
                  util.create_html(todo_json)
              })
      })
})
