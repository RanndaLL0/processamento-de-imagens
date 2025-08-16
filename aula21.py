import FreeSimpleGUI as sg
import io
from PIL import Image,ImageChops

def resize_image(image_path):
    img = Image.open(image_path)
    img2 = Image.open('./image.png')

    img = img.resize((1920,1080),Image.Resampling.LANCZOS)
    img2 = img2.resize((1920,1080),Image.Resampling.LANCZOS)

    img = ImageChops.add_modulo(img,img2)  


    return img

layout = [
    [sg.Menu([['Arquivo',['Abrir', 'Fechar']], ['Ajuda',['Sobre']]])],
    [sg.Image(key='-Image-',size=(800,600))]
]

sg.theme('dark grey 9')
window = sg.Window('Um sapo maneiro', layout, resizable=True)

while True:
    event,values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Fechar':
        break
    if event == 'Abrir':
        file_path = sg.popup_get_file('Selecione a imagem')
        if file_path:
            resized_image = resize_image(file_path)

            img_bytes = io.BytesIO()
            resized_image.save(img_bytes, format='PNG')
            window['-Image-'].update(data=img_bytes.getvalue())

        # if file_path:
        #     window['-Image-'].update(filename=file_path)
    elif event == 'Sobre':
        sg.popup("Feito por mim mesmo")


window.close()