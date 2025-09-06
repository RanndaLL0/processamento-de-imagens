import FreeSimpleGUI as sg
from PIL import Image, ExifTags, ImageEnhance, ImageFilter, ImageDraw
import io
import os
import webbrowser
import requests
import time
 
previous_states = []
forward_states = []
image_atual = None
image_path = None
 
def make_img_atual_negative():
  global image_atual
  global previous_states
 
  if image_atual:
    width, height = image_atual.size
    previous_states.append(image_atual.copy())
    pixels = image_atual.load()
    for x in range(1, width):
      for y in range(1, height):
        pixel  = image_atual.getpixel((x, y))
        new_r = 255 - pixel[0]
        new_g = 255 - pixel[1]
        new_b = 255 - pixel[2]
        pixels[x, y] = (new_r, new_g, new_b, pixel[3]) if len(pixel) > 3 else (new_r, new_g, new_b)
    show_image(image_atual)

def make_img_atual_rotate_left():
    global image_atual
    global previous_states

    previous_states.append(image_atual.copy())
    image_atual = image_atual.rotate(90)
    show_image(image_atual)

def make_img_atual_rotate_right():
    global image_atual
    global previous_states

    previous_states.append(image_atual.copy())
    image_atual = image_atual.rotate(270)
    show_image(image_atual)

def make_img_atual_sharpeness():
    global image_atual
    global previous_states

    previous_states.append(image_atual.copy())
    enhancer  = ImageEnhance.Sharpness(image_atual)
    factor = 32
    show_image(enhancer.enhance(factor))

def make_img_atual_four_bits():
    global image_atual
    global previous_states

    try:
       if image_atual:
          previous_states.append(image_atual.copy())
          image_atual = image_atual.convert('P', palette=Image.ADAPTIVE, colors=4)
          show_image(image_atual)
       else:
          sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de 4 bits")
   
def make_img_atual_sepia():
  global image_atual
  global previous_states  
 
  if image_atual:
    width, height = image_atual.size
    previous_states.append(image_atual.copy())
    pixels = image_atual.load()
    for x in range(1, width):
      for y in range(1, height):
        pixel  = image_atual.getpixel((x, y))
        new_r = min(pixel[0] + 150, 255)
        new_g = min(pixel[1] + 100, 255)
        new_b = min(pixel[2] + 50, 255)
        pixels[x, y] = (new_r, new_g, new_b, pixel[3]) if len(pixel) > 3 else (new_r, new_g, new_b)
    show_image(image_atual)

def make_img_atual_grayscale():
    width, height = image_atual.size
    previous_states.append(image_atual.copy())
    pixels = image_atual.load()
    for x in range(1, width):
      for y in range(1, height):
        pixel  = image_atual.getpixel((x, y))
        new_r = int(pixel[0] * 0.30)
        new_g = int(pixel[1] * 0.59)
        new_b = int(pixel[2] * 0.11)

        gray = new_r + new_g + new_b
        pixels[x, y] = (gray , gray, gray)
    show_image(image_atual)

def make_img_atual_blur():
   global image_atual
   global previous_states

   if image_atual:
      previous_states.append(image_atual.copy())
      image_atual = image_atual.filter(ImageFilter.GaussianBlur(radius=5))
      show_image(image_atual)

def make_img_atual_edge():
   global image_atual
   global previous_states

   if image_atual:
      previous_states.append(image_atual.copy())
      image_atual = image_atual.filter(ImageFilter.EDGE_ENHANCE)
      show_image(image_atual)
 
def undo():
  global image_atual
  global previous_states
  global forward_states
 
  if len(previous_states) > 0:
    forward_states.append(image_atual)
    image_atual = previous_states[-1]
    del previous_states[-1]
    show_image(image_atual)
   
def forward():
  global image_atual
  global previous_states
  global forward_states
 
  if len(forward_states) > 0:
    previous_states.append(image_atual)
    image_atual = forward_states[-1]
    del forward_states[-1]
    show_image(image_atual)
 
def url_download(url):
    global image_atual
    global previous_states
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            image_atual = Image.open(io.BytesIO(r.content))
            previous_states.append(image_atual.copy())
            show_image(image_atual)
        else:
            sg.popup("Falha ao baixar a imagem. Verifique a URL e tente novamente.")
    except Exception as e:
        sg.popup(f"Erro ao baixar a imagem: {str(e)}")
 
def show_image(img):
    try:
        resized_img = resize_image(img)
        img_bytes = io.BytesIO()
        resized_img.save(img_bytes, format='PNG')
        window['-IMAGE-'].update(data=img_bytes.getvalue())
    except Exception as e:
        sg.popup(f"Erro ao exibir a imagem: {str(e)}")
 
def resize_image(img):
    try:
        img = img.resize((800, 600), Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        sg.popup(f"Erro ao redimensionar a imagem: {str(e)}")
 
def open_image(filename):
    global image_atual
    global image_path
    try:
        image_path = filename
        image_atual = Image.open(filename)    
        show_image(image_atual)
    except Exception as e:
        sg.popup(f"Erro ao abrir a imagem: {str(e)}")

def make_img_atual_histogram():
    global image_atual
    global previous_states

    try:
        if image_atual:
            img_rgb = image_atual.convert('RGB')

            r,g,b = img_rgb.split()
            width, height = 256,256
            margin = 10
            max_count = max(max(r), max(g), max(b))
            hist_img = Image.new('RGB', (width, height), 'black')
            
            draw = ImageDraw.draw()

            for x in range(256):
                rh = int((r[x] / max_count) * (height - margin))
                gh = int((g[x] / max_count) * (height - margin))
                bh = int((b[x] / max_count) * (height - margin))

                draw.line([(x, height - 1), (x, height - 1 - rh)], fill=(255, 0, 0))
                draw.line([(x, height - 1), (x, height - 1 - gh)], fill=(0, 255, 0))
                draw.line([(x, height - 1), (x, height - 1 - bh)], fill=(0, 0, 255))

            scale_x, scale_y = 3, 2
            hist_big = hist_img.resize((width * scale_x, height * scale_y), Image.LANCZOS)

            img_bytes = io.BytesIO()
            hist_big.save(img_bytes, format='PNG')

            layout = [
                [sg.Image(data=img_bytes.getvalue(), key='-HIST-')],
                [sg.Button('Fechar')]
            ]
            win_hist = sg.Window('Histograma RGB', layout, modal=True, finalize=True)
            while True:
                e, _ = win_hist.read()
                if e in (sg.WINDOW_CLOSED, 'Fechar'):
                    break
            win_hist.close()
    except Exception as e:
        sg.popup(f"Erro ao gerar histograma: {str(e)}")

 
def save_image(filename):
    global image_atual
    try:
        if image_atual:
            with open(filename, 'wb') as file:
                image_atual.save(file)
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao salvar a imagem: {str(e)}")
 
def info_image():
    global image_atual
    global image_path
    try:
        if image_atual:
            largura, altura = image_atual.size
            formato = image_atual.format
            tamanho_bytes = os.path.getsize(image_path)
            tamanho_mb = tamanho_bytes / (1024 * 1024)
            sg.popup(f"Tamanho: {largura} x {altura}\nFormato: {formato}\nTamanho em MB: {tamanho_mb:.2f}")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")
 
def exif_data():
    global image_atual
    try:
        if image_atual:
            exif = image_atual._getexif()
            if exif:
                exif_data = ""
                for tag, value in exif.items():
                    if tag in ExifTags.TAGS:
                        if tag == 37500 or tag == 34853:
                            continue
                        tag_name = ExifTags.TAGS[tag]
                        exif_data += f"{tag_name}: {value}\n"
                sg.popup("Dados EXIF:", exif_data)
            else:
                sg.popup("A imagem não possui dados EXIF.")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao ler dados EXIF: {str(e)}")
 
def gps_data():
    global image_atual
    try:
        if image_atual:
            exif = image_atual._getexif()
            if exif:
                gps_info = exif.get(34853)  #Tag para informações de GPS
                print (gps_info[1], gps_info[3])
                if gps_info:
                    latitude = int(gps_info[2][0]) + int(gps_info[2][1]) / 60 + int(gps_info[2][2]) / 3600
                    if gps_info[1] == 'S':  #Verifica se a direção é 'S' (sul)
                        latitude = -latitude
                    longitude = int(gps_info[4][0]) + int(gps_info[4][1]) / 60 + int(gps_info[4][2]) / 3600
                    if gps_info[3] == 'W':  #Verifica se a direção é 'W' (oeste)
                        longitude = -longitude
                    sg.popup(f"Latitude: {latitude:.6f}\nLongitude: {longitude:.6f}")
                    open_in_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
                    if sg.popup_yes_no("Deseja abrir no Google Maps?") == "Yes":
                        webbrowser.open(open_in_maps_url)
                else:
                    sg.popup("A imagem não possui informações de GPS.")
            else:
                sg.popup("A imagem não possui dados EXIF.")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao ler dados de GPS: {str(e)}")
 
layout = [
    [sg.Menu([
            ['Arquivo', ['Abrir', 'Abrir URL', 'Salvar', 'Fechar']],
            ['Filtros', ['Inverter', 'Sepia', 'Voltar', 'Preto e Branco','Avançar']],
            ['Girar', ['Girar Esquerda', 'Girar Direita']],
            ['imagem', ['Sharpeness','4 bits','Blur','Edge','Histogram']],
            ['EXIF', ['Mostrar dados da imagem', 'Mostrar dados de GPS']],
            ['Sobre a image', ['Informacoes']],
            ['Sobre', ['Desenvolvedor']]
        ])],
    [sg.Image(key='-IMAGE-', size=(1024, 768))],
]
 
window = sg.Window('Photo Shoping', layout, finalize=True, resizable=True)
 
while True:
    event, values = window.read()
 
    if event in (sg.WINDOW_CLOSED, 'Fechar'):
        break
    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)
    elif event == 'Abrir URL':
        url = sg.popup_get_text("Digite a url")
        if url:
            url_download(url)
    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == "Inverter":
      make_img_atual_negative();
    elif event == "Sepia":
      make_img_atual_sepia()
    elif event == 'Informacoes':
        info_image()
    elif event == 'Mostrar dados da imagem':
        exif_data()
    elif event == 'Mostrar dados de GPS':
        gps_data()
    elif event == 'Desenvolvedor':
        sg.popup('Desenvolvido por Indio - BCC 6º Semestre')
    elif event == "Voltar":
      undo()
    elif event == "Avançar":
      forward()
    elif event == "Preto e Branco":
      make_img_atual_grayscale()
    elif event == "Girar Esquerda":
      make_img_atual_rotate_left()
    elif event == "Girar Direita":
      make_img_atual_rotate_right()
    elif event == "Sharpeness":
      make_img_atual_sharpeness()
    elif event == "4 bits":
      make_img_atual_four_bits()
    elif event == "Blur":
      make_img_atual_blur()
    elif event == "Edge":
      make_img_atual_edge()
    elif event == "Histogram":
      make_img_atual_histogram()
 
window.close()