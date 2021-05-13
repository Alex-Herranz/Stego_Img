from PIL import Image

def stego_hide(file, data, output):
    # Open the image
    with Image.open(file) as im:
        px = im.load()

        # Establish initial pixel
        pixel = (1, 1)
        path = [pixel]

        # For each character in the message
        for c in data:
            # Split the character in two
            c1 = c // 16
            c2 = c % 16
            #print("Caracter: ", chr(c), ", charN: ", c, ", parte mayor: ", c1, ", parte menor: ", c2)

            # Read target pixel data
            pixelData = px[pixel[0], pixel[1]]
            #print("Leyendo pixel ", pixel)
            #print("PixelData inicial: ", pixelData)

            # Crear nuevos datos para el pixel
            newG = pixelData[1] - pixelData[1] % 16 + c1
            newB = pixelData[2] - pixelData[2] % 16 + c2

            if (pixelData[1] - newG > 8) and (newG + 16 <= 255): newG += 16
            elif (pixelData[1] - newG < -8) and (newG - 16 >= 0): newG -= 16
            if (pixelData[2] - newB > 8) and (newB + 16 <= 255): newB += 16
            elif (pixelData[2] - newB < -8) and (newG - 16 >= 0): newB -= 16

            pixelData = (pixelData[0], newG, newB)
            #print("PixelData final: ", pixelData)

            # Modify target pixel
            im.putpixel(pixel, pixelData)

            # Check if there's available pixels left
            if len(path) == (im.size[0] * im.size[1]):
                #print("Mensaje demasiado largo, finalizando")
                break

            # Assign new target pixel
            pixel = (((pixel[0] * pixelData[0] // 16) % im.size[0]), \
                     ((pixel[1] * pixelData[1] // 16) % im.size[1]))

            # Collision treatment
            pixelOri = pixel
            while pixel in path:
                pixel = (((pixel[0] + 1) % im.size[0]),
                         (pixel[1]))
                if (pixel == pixelOri):
                    pixel = ((pixel[0]),
                             (pixel[1] + 1) % im.size[1])
                    pixelOri = pixel

            # Append to path
            path.append(pixel)

        im.show()
        im.save(output)

def stego_find(file):
    # Open the image
    with Image.open(file) as im:
        px = im.load()

        data = ""
        c = '0'

        # Establish initial pixel
        pixel = (1, 1)
        path = [pixel]

        # While escape sequence is not detected
        while c != '\0':
            # Read target pixel data
            pixelData = px[pixel[0], pixel[1]]
            #print("Leyendo pixel ", pixel)

            # Reconstruct character and append to message
            c = chr((pixelData[1] % 16) * 16 + pixelData[2] % 16)
            data += c
            #print("Caracter reconstruido: ", c)

            # Check if there are pixels left to read
            if len(path) == (im.size[0] * im.size[1]): break

            # Assign new target pixel
            pixel = (((pixel[0] * pixelData[0] // 16) % im.size[0]), \
                     ((pixel[1] * pixelData[1] // 16) % im.size[1]))

            # Collision treatment
            pixelOri = pixel
            while pixel in path:
                pixel = (((pixel[0] + 1) % im.size[0]),
                         (pixel[1]))
                if (pixel == pixelOri):
                    pixel = ((pixel[0]),
                             (pixel[1] + 1) % im.size[1])
                    pixelOri = pixel

            # Append to path
            path.append(pixel)

        return data