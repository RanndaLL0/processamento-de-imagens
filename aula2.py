import FreeSimpleGUI as sg

layout = [
    [sg.Text('Calculadora para burros')],
    [sg.Input(key='-INPUT-')],
    [sg.Text(size=(40,1), key='-OUTPUT-')],
    [sg.Button('SUM'),sg.Button('SUB'),sg.Button('MUT'),sg.Button('DIV')]
]

window = sg.Window('Ola mundo', layout)

while True:
    event,values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'OK':
        break
    window['-OUTPUT-'].update(values['-INPUT-'])

window.close()