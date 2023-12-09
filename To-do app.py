import functions
import PySimpleGUI as ui
import time

ui.theme("Black")

clock = ui.Text('', key='clock')
label = ui.Text("Type in a To-Do - ")
input_box = ui.InputText(tooltip='Add your todo here...', key='todo')

list_box = ui.Listbox(values=functions.get_todos(),
                      key='todos',
                      enable_events=True, size=[30, 10]
                      )
add_button = ui.Button(button_text='Add', mouseover_colors='LightBlue2')
edit_button = ui.Button("Edit")
complete_button = ui.Button("Complete")
exit_button = ui.Button("Exit")
clear_todos = ui.Button(button_text="Clear", key='Clear')

window = ui.Window(title='SaX To Do',
                   layout=[

                       [clock],
                       [label],
                       [input_box, add_button],
                       [clear_todos],
                       [list_box, edit_button, complete_button, ],
                       [exit_button]

                   ],
                   font=('Helvetica', 10))

while True:
    event, values = window.read(timeout=200)
    window['clock'].update(value=time.strftime("Date-%d %B %Y Time-%H:%M:%S"))

    match event:
        case 'Add':
            todos = functions.get_todos()
            new_todo = values['todo'] + '\n'
            todos.append(new_todo)
            functions.write_todos(todos)

            window['todos'].update(values=todos)

        case 'Edit':
            try:
                todo_to_edit = values['todos'][0]
                new_todo = values['todo']

                todos = functions.get_todos()
                index = todos.index(todo_to_edit)
                todos[index] = new_todo
                functions.write_todos(todos)

                window['todos'].update(values=todos)
            except (IndexError, ValueError):
                ui.popup("There's no item to edit.")

        case 'Clear':
            todos = functions.get_todos()

        case 'Complete':
            try:
                todo_to_complete = values['todos'][0]
                todos = functions.get_todos()
                todos.remove(todo_to_complete)
                functions.write_todos(todos)

                window['todos'].update(values=todos)
                window['todo'].update(value='')
            except (IndexError, ValueError):
                ui.popup("There's no items.")

        case 'Exit':
            break
        case 'todos':
            try:
                window['todo'].update(value=values['todos'][0])
            except IndexError:
                ui.popup("There's no item.")
        case ui.WIN_CLOSED:
            break

window.close()
