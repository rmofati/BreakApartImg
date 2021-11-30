# Resolução do Exercício 1 - Visão Computacional.
# Aluno: Rafael Mofati Campos

import numpy as np
import cv2
import PIL
from PIL import Image
from matplotlib import pyplot as plt

def erosao(img):
    img_erodida = np.zeros_like(img)
    for x in range(img.shape[0]):               # For Altura da imagem
        for y in range(img.shape[1]):           # For Largura da imagem
            try:
                if img[x][y + 1] == 255 and img[x - 1][y] == 255 and img[x][y] == 255 and img[x+1][y] == 255 and img[x][y-1] == 255:
                    img_erodida[x][y] = 255
                else:
                    img_erodida[x][y] = 0
            except:
                continue
    return img_erodida

def contorno(img, img_erodida):
    img_contorno = np.zeros_like(img)
    for x in range(img.shape[0]):      # For Altura da imagem
        for y in range(img.shape[1]):  # For Largura da imagem
            try:
                img_contorno[x][y] = img[x][y] - img_erodida[x][y]
            except:
                continue
    return img_contorno

def area(img):
    val_area = np.count_nonzero(img)
    return val_area

def perimetro(img):
    val_perimetro = np.count_nonzero(img)
    return val_perimetro

def compacidade(img):
    pass

def maior_eixo(img):
    white_pixels = np.argwhere(perimetro_aux == 255)
    
    maior_distancia = 0

    xa_final_maior = white_pixels[0][1]
    ya_final_maior = white_pixels[0][0]

    for i in range(len(white_pixels)):
        current_xa = white_pixels[i][1]
        current_ya = white_pixels[i][0]

        for h in range(len(white_pixels)):
            try:
                dist_calc = ((white_pixels[h+1][1] - current_xa)**2 + (white_pixels[h+1][0] - current_ya)**2)**(1/2)

                if dist_calc > maior_distancia:
                    maior_distancia = dist_calc
                    xa_final_maior = current_xa
                    ya_final_maior = current_ya
                    xb_final_maior = white_pixels[h+1][1]
                    yb_final_maior = white_pixels[h+1][0]
                
                h += 1

            except:
                continue

    return xa_final_maior, ya_final_maior, xb_final_maior, yb_final_maior, maior_distancia

def menor_eixo(img):
    white_pixels = np.argwhere(perimetro_aux == 255)
    
    menor_distancia = 9999

    xa_final_menor = white_pixels[0][1]
    ya_final_menor = white_pixels[0][0]

    for i in range(len(white_pixels)):
        current_xa = white_pixels[i][1]
        current_ya = white_pixels[i][0]

        for h in range(len(white_pixels)):
            try:
                dist_calc = ((white_pixels[h+1][1] - current_xa)**2 + (white_pixels[h+1][0] - current_ya)**2)**(1/2)

                if dist_calc < menor_distancia:
                    menor_distancia = dist_calc
                    xa_final_menor = current_xa
                    ya_final_menor = current_ya
                    xb_final_menor = white_pixels[h+1][1]
                    yb_final_menor = white_pixels[h+1][0]
                
                h += 1

            except:
                continue

    return xa_final_menor, ya_final_menor, xb_final_menor, yb_final_menor, menor_distancia

def bounding_box(img):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            try:
                if img[y][x] == 255:
                    min_y = y
                    break
                else:
                    continue
            except:
                continue
        if img[y][x] == 255:
            break

    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            try:
                if img[y][x] == 255:
                    min_x = x
                    break
                else:
                    continue
            except:
                continue
        if img[y][x] == 255:
            break

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            try:
                if img[y][x] == 255:
                    max_y = y
                else:
                    continue
            except:
                continue
        if img[y][x] == 255:
            break
    
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            try:
                if img[y][x] == 255:
                    max_x = x
                else:
                    continue
            except:
                continue
        if img[y][x] == 255:
            break
    
    return min_x, min_y, max_x, max_y

images = ["img_separada0.png", "img_separada1.png", "img_separada2.png", "img_separada3.png", "img_separada4.png"]

for count, img in enumerate(images):
    work_img = cv2.imread(img, 0)
    
    val_area = area(work_img)
    print("Área da imagem " + str(count) + ": " + str(val_area) + " pixels")

    perimetro_aux = erosao(work_img)
    perimetro_aux = contorno(work_img, perimetro_aux)
    val_perimetro = perimetro(perimetro_aux)
    print("Perímetro da imagem " + str(count) + ": " + str(val_perimetro) + " pixels")

    compacidade = (val_perimetro**2) / val_area
    print("Compacidade da imagem " + str(count) + ": " + str(compacidade))

    xa_final_maior, ya_final_maior, xb_final_maior, yb_final_maior, maior_dist = maior_eixo(perimetro_aux)
    xa_final_menor, ya_final_menor, xb_final_menor, yb_final_menor, menor_dist = menor_eixo(perimetro_aux)
    print("Maior eixo nesta figura: " + str(maior_dist) + " pixels")
    print("Menor eixo nesta figura: " + str(menor_dist) + " pixels")
    perimetro_aux_pronto = cv2.line(perimetro_aux, (xa_final_maior, ya_final_maior), (xb_final_maior, yb_final_maior), (120, 120, 120), 2)

    min_x, min_y, max_x, max_y = bounding_box(perimetro_aux)
    eixo_x = max_x - min_x
    eixo_y = max_y - min_y
    alongamento = eixo_y/eixo_x

    print("Alongamento da imagem: " + str(alongamento))
    print("Tamanho eixo x: " + str(eixo_x) + " pixels")
    print("Tamanho eixo y: " + str(eixo_y) + " pixels")
    #print(min_x, min_y, max_x, max_y)

    # Desenha BoundingBox ao redor das imagens
    #perimetro_aux_pronto = cv2.rectangle(perimetro_aux_pronto, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

    # Desenha eixo menor na imagem
    #perimetro_aux_pronto = cv2.line(perimetro_aux, (xa_final_menor, ya_final_menor), (xb_final_menor, yb_final_menor), (255, 0, 0), 5)
    
    cv2.imshow("Eixos", perimetro_aux_pronto)

    print("")
    cv2.waitKey(0)

cv2.waitKey(0)
cv2.destroyAllWindows()