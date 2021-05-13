import PySimpleGUI as sg
import stego

def hide():
    # Changing the color theme of the GUI
    sg.theme('Topanga')

    # Defining the layout of the window with the secret message and the image
    layout = [
        [sg.Text('Please enter the secret message')],
        [sg.Text('Secret Message', size=(15, 1)), sg.InputText(key='msg')],
        [sg.Text('Please select an image')],
        [sg.Text('Image:', size=(8, 1)), sg.Input(key='img'), sg.FileBrowse()],
        [sg.Text('Output Folder:'), sg.Input(key='folder'), sg.FolderBrowse(target='folder')],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Hide Image', layout)
    # Reading values of the text fields and checking if we cancel the program
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        window.close()
        exit()

    # Checking if all the fields were completed in order to run the program
    while values['msg'] == '' or values['img'] == '' or values['folder'] == '':
        # If some field was empty pop up an error
        if event == 'Submit':
            sg.popup('Error: You must enter all parameters')
        # If you cancel the program, exit
        else:
            window.close()
            exit()

        # Read the values of the fields again
        event, values = window.read()

    # Checking if the selected image is a png, jpg or bmp file
    while values['img'].endswith('.png') == False and values['img'].endswith('.jpg') == False and values[
        'img'].endswith('.bmp') == False:
        # If not pop up an error
        if event == 'Submit':
            sg.popup('Error: You must enter a valid image file (jpg, png or bmp)')
        # If you cancel the program, exit
        else:
            window.close()
            exit()

        # Read the values of the fields again
        event, values = window.read()

    # We save the data of the fields and close the window
    data = values['msg']
    file_encode = values['img']
    outputPath = values['folder']

    window.close()

    return data, file_encode, outputPath

def unhide():
    # Changing the color theme of the GUI
    sg.theme('Topanga')

    # Defining the layout of the window with the secret message and the image
    layout2 = [
        [sg.Text('Please select the image with the secret message')],
        [sg.Text('Image:', size=(8, 1)), sg.Input(key='img2'), sg.FileBrowse()],
        [sg.Submit(), sg.Cancel()]
    ]

    window2 = sg.Window('Unhide image', layout2)
    # Reading values of the text fields and checking if we cancel the program
    event2, values2 = window2.read()
    if event2 in (sg.WIN_CLOSED, 'Cancel'):
        window2.close()
        exit()

    # Checking if all the fields were completed in order to run the program
    while values2['img2'] == '':
        # If some field was empty pop up an error
        if event2 == 'Submit':
            sg.popup('Error: You must select an image')
        # If you cancel the program, exit
        else:
            window2.close()
            exit()

        # Read the values of the fields again
        event2, values2 = window2.read()

    # Checking if the selected image is a png, jpg or bmp file
    while not values2['img2'].endswith('.bmp') and not values2['img2'].endswith('.png'):
        # If not pop up an error
        if event2 == 'Submit':
            sg.popup('Error: You must enter a valid image file (bmp or png)')
        # If you cancel the program, exit
        else:
            window2.close()
            exit()

        # Read the values of the fields again
        event2, values2 = window2.read()

    # We save the data of the fields and close the window

    file_decode = values2['img2']

    data = stego.stego_find(file_decode)

    sg.popup(data)

    window2.close()

    return

# Changing the color theme of the GUI
sg.theme('Topanga')

# Defining the layout of the window with the secret message and the image
layout3 = [
    [sg.Text('Welcome to StegoBMP, select a steganography option')],
    [[sg.Button('Hide')], [sg.Button('Unhide')]]
]

window3 = sg.Window('StegoBMP', layout3)
# Reading values of the text fields and checking if we cancel the program
event3, values2 = window3.read()

if event3 in (sg.WIN_CLOSED, 'Cancel'):
    window3.close()
    exit()

if event3 == 'Hide':
    window3.close()
    data, file_encode, outputPath = hide()
    data += '\0'
    name = file_encode.rsplit("/", 1)[1]
    name = name.split(".")[0]
    file_output = outputPath + "/" + name + "_output.png"
    print(file_output)
    stego.stego_hide(file_encode, data.encode('ascii'), file_output)

if event3 == 'Unhide':
    window3.close()
    unhide()