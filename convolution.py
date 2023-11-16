from PIL import Image
import numpy as np
import winsound
import time
import sys

def convolucion(img, kernel, tecnica):
    '''Realiza la convolucion segun la tecnica indicada.
    Return: Matriz numpy con la convolucion
    '''
    try:
        filas_img, columnas_img= img.shape
    except:
        print("La imagen selecionada debe ser a blanco y negro con extensión .bmp")
        input('Presione una tecla para continuar...')
        sys.exit(1)
        
    filas_kernel, columnas_kernel= kernel.shape
    
    if tecnica == 'stride':
        filas_conv = filas_img - filas_kernel + 1
        columnas_conv = columnas_img - columnas_kernel + 1
    
    elif tecnica == 'zero_padding':
        filas_conv = filas_img
        columnas_conv = columnas_img
        
        fila_zeros = np.zeros(columnas_img, dtype=int).reshape(1,-1)
        img = np.append(fila_zeros, img, axis=0)
        img = np.append(img, fila_zeros, axis=0)
        
        col_zeros = np.zeros(filas_img+2, dtype=int).reshape(-1,1)
        img = np.append(col_zeros, img, axis=1)
        img = np.append(img, col_zeros, axis=1)
    
    elif tecnica == 'reflective_padding':
        filas_conv = filas_img
        columnas_conv = columnas_img
         
        fila_reflejo_superior = img[0].reshape(1,-1)
        fila_reflejo_inferior = img[-1].reshape(1,-1)
        img = np.append(fila_reflejo_superior, img, axis=0)
        img = np.append(img, fila_reflejo_inferior, axis=0)
        
        col_reflejo_izquierda = img[:,0].reshape(-1,1)
        col_reflejo_derecha = img[:,-1].reshape(-1,1)
        img = np.append(col_reflejo_izquierda, img, axis=1)
        img = np.append(img, col_reflejo_derecha, axis=1)
    
    else:
        print('Técnica no disponible')
        return np.zeros((3,3))
    
    conv = np.empty([filas_conv, columnas_conv])
    
    for i in range(filas_conv):
        aux = np.array([])
        for j in range(columnas_conv):
            seleccion_img = img[i:i+filas_kernel, j:j+columnas_kernel]
            valor = np.vdot(seleccion_img, kernel)
            aux = np.append(aux, valor)
            
        conv[i] = aux
        print(f'Proceso: {i+1}/{filas_conv}')
    return conv

def generar_bmp(matriz):
    nuevas_filas, nuevas_columnas = matriz.shape

    # Crea una imagen BMP a partir de la matriz de píxeles
    imagen = Image.new("L", (nuevas_columnas, nuevas_filas))
    imagen.putdata([valor for fila in matriz for valor in fila])
    
    #Invierte los colores
    imagen = Image.eval(imagen, lambda x: 255 - x)
    return imagen

def kernels():
    return {
         1: np.array([[0, 1, 0], 
                    [1, -4, 1],
                    [0, 1, 0]]),
         2: np.array([[-1, -1, -1], 
                    [-1, 8, -1],
                    [-1, -1, -1]]),
         3: np.array([[0.25, 0, -0.25], 
                    [0.50, 0, -0.50],
                    [0.25, 0, -0.25]]),
         4: np.array([[-0.25, -0.50, -0.25], 
                    [0, 0, 0],
                    [0.25, 0.50, 0.25]]),
    }

image_name = 'vase.bmp' #Nombre del archivo .bmp que está en la misma carpeta
img_original = Image.open(image_name)
img_matriz = np.array(img_original)

kernel = kernels()
num_kernel = 1 # 1-4
tecnica = 'stride' #stride, zero_padding, reflective_padding

inicio = time.time()
matriz_convolucion = convolucion(img_matriz, kernel[num_kernel], tecnica)
fin = time.time()
tiempo = round(fin-inicio, 2)

print('Finalizado')
print('Tiempo:',tiempo,'segundos')

img_nueva = generar_bmp(matriz_convolucion)
file_name = f'{image_name[0:len(image_name)-4]}_{tecnica}_kernel{num_kernel}_segundos_{tiempo}.bmp'
img_nueva.save(file_name)
img_nueva.close()

frequency = 2500 
duration = 1000
winsound.Beep(frequency, duration)

#Abrir
Image.open(file_name).show()