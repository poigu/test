#!/usr/bin/python3

import os
import pyglet
import gphoto2 as gp
import configparser
import exifread
from pyautogui import prompt, alert
from PIL import Image
global i
i = 0

#gp.check_result(gp.use_python_logging())
#camera = gp.Camera()
#camera.init()

config = configparser.ConfigParser()
config.read("config.ini")

#Функция проверки пути
def pathChecker(path):
    if (path.startswith('"') or path.startswith("'")) and \
            (path.endswith('"') or path.endswith('"')):
        path = path[1:-1]
    if path.endswith("/"):
        return path
    else:
        path = path + "/"
        return path

#Запуск сессии
def sessionStart():
    user = prompt(text="Введите имя пользователя:", title="Пользователь")
    MAIN_PHOTO_FOLDER = None

    if "MAIN_PHOTO_FOLDER" in config["base_conf"] and \
            len(config["base_conf"]["MAIN_PHOTO_FOLDER"]) > 0:
        MAIN_PHOTO_FOLDER = config["base_conf"]["MAIN_PHOTO_FOLDER"]
        MAIN_PHOTO_FOLDER = pathChecker(MAIN_PHOTO_FOLDER)

    else:
        MAIN_PHOTO_FOLDER = os.environ.get("MAIN_PHOTO_FOLDER", \
                os.environ.get("HOME"))

        MAIN_PHOTO_FOLDER = pathChecker(MAIN_PHOTO_FOLDER)
    
    if user:
        new_folder_path = os.path.join(MAIN_PHOTO_FOLDER, user)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            os.chdir(new_folder_path)
        else:
            alert(text="Такая папка уже существует!\nВведите другое имя", \
                    title="Error", button="OK")
            sessionStart()

    screens = pyglet.canvas.get_display().get_screens()
    screen = screens[0]
    checkWindow = pyglet.window.Window(width=760, height=540, screen=screen)

sessionStart()

def takePhoto():
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

    target = f"photo_{i}.jpg"
    camera_file = camera.file_get(file_path.folder, file_path.name, \
            gp.GP_FILE_TYPE_NORMAL)

    gp.check_result(gp.gp_file_save(camera_file, target))

#window = pyglet.window.Window(width=1920, height=1080)

screens = pyglet.canvas.get_display().get_screens()

# Выбираем второй монитор
screen = screens[1]

# Устанавливаем размеры окна в книжной ориентации
width = 1080
height = 1920

# Создаем окно на втором мониторе
window = pyglet.window.Window(fullscreen=True, width=width, height=height, screen=screen)

# Устанавливаем положение окна в книжной ориентации
#x = screen.x + screen.width + (width - height)  // 2
x = screen.x
y = screen.y + (height - width) // 2
window.set_location(x, y)

# Отображаем окно
window.set_visible(True)

@window.event
def on_mouse_press(x, y, button, modifier):
    global i
    if button == pyglet.window.mouse.RIGHT:
        takePhoto()
        with open(f'photo_{i}.jpg', 'rb') as f:
            tags = exifread.process_file(f)

        img = Image.open(f'photo_{i}.jpg')

        if 'Image Orientation' in tags:
            orientation = tags['Image Orientation']
            if orientation.values[0] == 6:
                img = img.transpose(Image.ROTATE_270)
            elif orientation.values[0] == 8:
                img = img.transpose(Image.ROTATE_90)
            elif orientation.values[0] == 3:
                img = img.transpose(Image.ROTATE_180)

       # img = img.convert("CMYK")
        img = img.convert("L")
        img.save(f"photo_{i}.jpg")
        img = pyglet.image.load(f"photo_{i}.jpg")
        img.blit(0,0)
        i += 1

@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.ESCAPE:
        camera.exit()

pyglet.app.run()

