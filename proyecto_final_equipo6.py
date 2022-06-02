from PIL import Image
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import LabelFrame
from tkinter import ttk

# Chercar si el valor es par
def isPair(num):
	if num % 2 == 0:
		return True
	return False

# Convierte el mensaje en ASCII (binario 8 bits) 
def getBinary(message):
		formatedData = []
		# Por cada caracter en el mensaje, agregar a formatedData su equivalente en binario
		for i in message:
			formatedData.append(format(ord(i), '08b'))
		return formatedData


# Modifica los pixeles de acuerdo al mensaje en binario y los devuelve en una lista
def alterPixels(pixel, msg):

	datalist = getBinary(msg)
	longitudMensaje = len(datalist)
	imdata = iter(pixel)

	for i in range(longitudMensaje):

		# Extrae 3 pixeles al mismo tiempo
		# Va de tres en tres, sacando los primeros tres numeros de cada objeto dentro del arreglo
		# Es un arreglo de objetos que se ve mas o menos así [(r g b a), (r g b a)] donde solo nos interesan los elementos r,g, y b de cada objeto
		pixel = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# El valor del pixel debe ser 1 si es impar y 0 si es par
		for j in range(0, 8):

			if (datalist[i][j] == '1' and isPair(pixel[j])):
				if(pixel[j] != 0):
					pixel[j] -= 1
				else:
					pixel[j] += 1

			elif (datalist[i][j] == '0' and not isPair(pixel[j])):
				pixel[j] -= 1

			

    # El octavo pixel de cada set dice si se debe detener o leer más impar significa que se debe leer más; par significa que el mensaje acabó.
		if (i == longitudMensaje - 1):
			if (isPair(pixel[-1])):
				if(pixel[-1] != 0):
					pixel[-1] -= 1
				else:
					pixel[-1] += 1

		else:
			if (not isPair(pixel[-1])):
				pixel[-1] -= 1
		pixel = tuple(pixel)

		# Regresar los pixeles con formato para poder ser itreados
		yield pixel[0:3]
		yield pixel[3:6]
		yield pixel[6:9]

def cypherHelper(copyImage, message):
	# Se obtiene el acho en pixeles de la imagen
	width = copyImage.size[0]
	# Estas son las coordenadas para saber donde instartar los nuevos pixeles
	(x, y) = (0, 0)

	for i in alterPixels(copyImage.getdata(), message):

		# Se insertan los pixeles modificados en la nueva imagen
		copyImage.putpixel((x, y), i)
		# Si se llegó al ancho de la imagen, la coordenada y sube en uno y se reinicia en x, si no solo se aumenta en x
		if (x != (width - 1)):
			x += 1
		else:
			x = 0
			y += 1
		

def cypher(imageName, message, outputName):
	# Abrir la imagen como image
	image = Image.open(imageName, 'r')
	print(imageName)
	print(message)
	print(outputName)

	if (len(message) == 0):
		raise ValueError('No hay mensaje a cifrar')

	# copiar los contenidos de image a una nueva imagen para modificarla
	imageCopy = image.copy()
	# Comenzar con el proceso de cifrado de la imagen y el mensaje
	cypherHelper(imageCopy, message)
	#Guardar la imagen con el nombre dado por el usuario con la extensión dada por el usuario
	imageCopy.save(outputName, str(outputName.split(".")[1].upper()))

# Desencripta el mensaje de la imagen
def decypher(imageName):
	image = Image.open(imageName, 'r')
	#Inicializar el arreglo donde se almacenará el acumulado del mensaje 
	data = ''
	# Obrtener los datos de los pixeles de la imagen
	imgdata = iter(image.getdata())

	# Extrae 3 pixeles al mismo tiempo
	# Va de tres en tres, sacando los primeros tres numeros de cada objeto dentro del arreglo
	# Es un arreglo de objetos que se ve mas o menos así [(r g b a), (r g b a)] donde solo nos interesan los elementos r,g, y b de cada objeto
	# Esto lo hace mientras el noveno dígito de cada tercer pixel no sea impar, porque si lo fuera, el programa sabe que ahí termina el mensaje
	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# El mensaje en binario
		binstr = ''
		# Si es par el contenido del pixel, significa que originalmente había un 0, en caso contrario, un 1
		for i in pixels[:8]:
			if (isPair(i)):
				binstr += '0'
			else:
				binstr += '1'

    # Se convierte de binario a char
		data += chr(int(binstr, 2))
		if (not isPair(pixels[-1])):
			# Mandar una ventana emergente con el mensaje descifrado
			tk.messagebox.showinfo("Mensaje", data)
			return data





# Tkinter helper functions
def getImage():
	# Sacar el path de la imagen a partir de la interfaz gráfica
	global image_path
	image_path = fd.askopenfilename()
	return image_path


# Inicializamos la ventana con la librería TK interface
window = tk.Tk()
style = ttk.Style(window)
style.theme_use("alt")
print(style.theme_use())
window.title("Esteganografía de Imágenes")
window.geometry("500x350")

# Configuramos la sección de Cifrado de la GUI
frameEncode = LabelFrame(
    window,
    bg='#f0f0f0',
    font=(20)
)
frameEncode.pack(fill="both", expand="yes", padx=10, pady=10)

# Configuramos la sección de Descifrado de la GUI
frameDecode = LabelFrame(
    window,
    bg='#f0f0f0',
    font=(20)
)
frameDecode.pack(fill="both", expand="yes", padx=10, pady=4)


# Seccion para cifrar align text
tk.Label(frameEncode, text="Cifrar", font=("Arial Bold", 20)).grid(column=0, row=0)

# Etiqueta y botón de la selección de imagen fuente
tk.Label(frameEncode, text="Selecciona una imagen: ").grid(row=1, column=0)
tk.Button(frameEncode, text="Seleccionar", command=getImage).grid(row=1, column=1)

# Etiqueta y entrada de texto de la selección de texto a cifrar dentro de la imagen
tk.Label(frameEncode, text="Escribe el mensaje: ").grid(row=2, column=0)
message = tk.StringVar()
message_entry = tk.Entry(frameEncode, width=30, textvariable=message).grid(row=2, column=1)

# Etiqueta y entrada de texto de la selección del nombre del archivo resultante
tk.Label(frameEncode, text="Nombre imagen destino (con extensión): ", justify="left").grid(row=3, column=0)
outputName = tk.StringVar()
outputName_entry = tk.Entry(frameEncode, width=30, textvariable=outputName).grid(row=3, column=1)

# Botón de cifrar
tk.Button(frameEncode, text="Cifrar", command=lambda: cypher(image_path, message.get(), outputName.get())).grid(row=4, column=1)


# Seccion para descifrar
tk.Label(frameDecode, text="Descifrar", font=("Arial Bold", 20)).grid(column=0, row=5)

# Etiqueta y botón de la selección de imagen fuente
tk.Label(frameDecode, text="Selecciona una imagen: ").grid(row=6, column=0)
tk.Button(frameDecode, text="Seleccionar", command=getImage).grid(row=6, column=1)

# Botón de descifrar
tk.Button(frameDecode, text="Descifrar", command=lambda: decypher(image_path)).grid(row=6, column=2)



window.mainloop()