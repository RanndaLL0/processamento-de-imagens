import FreeSimpleGUI as sg
import io
from PIL import Image,ImageChops, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS, IFD
import webbrowser
import os

def convert_gps_info(coords,ref):
    decimal = float(coords[0]) + float(coords[1]) / 60 + float(coords[2]) / 3600
    if ref == "S" or ref == "W":
        decimal = -1 * decimal
    return decimal

def extract_gps_info(image_path):

    imagem = Image.open(image_path)
    img_exif = imagem.getexif()

    GPS_INFO = next(
        tag for tag, name in TAGS.items() if name == "GPSInfo"
    )
    gpsinfo = img_exif.get_ifd(GPS_INFO)
    print(gpsinfo)
    return {
        "latitude": convert_gps_info(gpsinfo[2],gpsinfo[1]),
        "longitude": convert_gps_info(gpsinfo[4], gpsinfo[3]),
        "altitude": gpsinfo[6]
    }

def extract_image_metadata(image_path):
    imagem = Image.open(image_path)
    img_exif = imagem.getexif()

    metadata_template = '\n'
    if img_exif is not None:
        for key, value in img_exif.items():
            metadata_template.join([f"{tag}: {value}" for _,tag in ExifTags.TAGS])
    print(metadata_template)


def image_info(image_path):
    imagem = Image.open(image_path)

    return {
        "format": imagem.format,
        "height": imagem.height,
        "width": imagem.width,
        "tamanho": os.path.getsize(image_path)
    }

def resize_image(image_path):
    img = Image.open(image_path)
    img2 = Image.open('./image.png')
    return img


layout = [
    [sg.Menu([['Arquivo',['Abrir', 'Fechar']],["Sobre a imagem",["Mostrar sobre"]],['EXIF',["Mostrar dados da imagem","Mostrar dados do GPS"]], ['Ajuda',['Sobre']]])],
    [sg.Image(key='-Image-',size=(800,600))]
]

sg.theme('dark grey 9')
window = sg.Window('Um sapo maneiro', layout, resizable=True)

file_path = None
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

    elif event == 'Sobre':
        sg.popup("Feito por mim mesmo")

    elif event == 'Mostrar sobre':
        print("Entrou aqui")
        if window['-Image-'] is not None:
            gps_infos = image_info(file_path)
            infos = '\n'.join([f"{key}: {value}" for key,value in image_info(file_path).items()]) + "\nFeito pelo ramos (indio)"
            sg.popup(infos)
            
    elif event == 'Mostrar dados do GPS':
        if window['-Image-'] is not None:
            gps_infos = extract_gps_info(file_path)
            print(gps_infos)
            webbrowser.open(f'https://www.google.com.br/maps?q={gps_infos['latitude']},{gps_infos['longitude']}')
    
    elif event == 'Mostrar dados da imagem':
        if window['-Image-'] is not None:
            extract_image_metadata(file_path)


window.close()