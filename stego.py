from PIL import Image

def stego_hide(file, data, output):
    #Abrir la imagen
    with Image.open(file) as im:
        px = im.load()

        # Establecer pixel de inicio
        pixel = (1, 1)
        recorrido = [pixel]

        # Por cada caracter del mensaje
        for c in data:
            # Descomponer el caracter
            c1 = c // 16
            c2 = c % 16
            print("Caracter: ", chr(c), ", charN: ", c, ", parte mayor: ", c1, ", parte menor: ", c2)

            # Leer datos del pixel
            pixelData = px[pixel[0], pixel[1]]
            print("Leyendo pixel ", pixel)
            print("PixelData inicial: ", pixelData)

            # Crear nuevos datos para el pixel
            newG = pixelData[1] - pixelData[1] % 16 + c1
            newB = pixelData[2] - pixelData[2] % 16 + c2

            if (pixelData[1] - newG > 8) and (newG + 16 <= 255): newG += 16
            elif (pixelData[1] - newG < -8) and (newG - 16 >= 0): newG -= 16
            if (pixelData[2] - newB > 8) and (newB + 16 <= 255): newB += 16
            elif (pixelData[2] - newB < -8) and (newG - 16 >= 0): newB -= 16

            pixelData = (pixelData[0], newG, newB)
            print("PixelData final: ", pixelData)

            # Modificar pixel
            im.putpixel(pixel, pixelData)

            # Asignar nuevo pixel
            pixel = (((pixel[0] * pixelData[0] // 16) % im.size[0]), \
                     ((pixel[1] * pixelData[1] // 16) % im.size[1]))

            # Detectar colisión
            pixelOri = pixel
            while pixel in recorrido:
                pixel = (((pixel[0] + 1) % im.size[0]),
                         (pixel[1]))
                if (pixel == pixelOri):
                    pixel = ((pixel[0]),
                             (pixel[1] + 1) % im.size[1])
                    pixelOri = pixel

            # Añadir al recorrido
            recorrido.append(pixel)

        im.show()
        im.save(output)

def stego_find(file):
    # Abrir la imagen
    with Image.open(file) as im:
        px = im.load()

        data = ""
        c = '0'

        # Establecer pixel de inicio
        pixel = (1, 1)
        recorrido = [pixel]

        # Mientras no se detecte la secuencia de escape
        while c != '\0':
            # Leer datos del pixel
            pixelData = px[pixel[0], pixel[1]]
            print("Leyendo pixel ", pixel)

            #Reconstruir caracter y almacenar en mensaje
            c = chr((pixelData[1] % 16) * 16 + pixelData[2] % 16)
            data += c
            print("Caracter reconstruido: ", c)

            #Calcular siguiente pixel
            pixel = (((pixel[0] * pixelData[0] // 16) % im.size[0]), \
                     ((pixel[1] * pixelData[1] // 16) % im.size[1]))

            # Detectar colisión
            pixelOri = pixel
            while pixel in recorrido:
                pixel = (((pixel[0] + 1) % im.size[0]),
                         (pixel[1]))
                if (pixel == pixelOri):
                    pixel = ((pixel[0]),
                             (pixel[1] + 1) % im.size[1])
                    pixelOri = pixel

            # Añadir al recorrido
            recorrido.append(pixel)

        return data