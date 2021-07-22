#Nome: Stefane Adna dos Santos

import argparse
import cv2
import glob
from pathlib import Path
import os


def open_img(path_img):
    dataset = []
    #carrega as imagens do diretorio
    for i in glob.glob(path_img + '/*.png', recursive=True):
        dataset.append(cv2.imread(i))
    for j in glob.glob(path_img + '/*.jpg', recursive=True):
        dataset.append(cv2.imread(j))
    return dataset


def save_img(dataset):
    #salva os contornos no diretorio
    if Path('questao1').is_dir():
        for i in range(len(dataset)):
            cv2.imwrite('questao1/img'+ str(i+1)+ '.png', dataset[i])
    else:
        os.mkdir('questao1')
        for i in range(len(dataset)):
            cv2.imwrite('questao1/img' + str(i+1) + '.png', dataset[i])


def segmentacao(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #utiliza o canny para detectar as bordas das imagens
    bordas = cv2.Canny(img_gray, 70, 150)
    img_bordas = bordas.copy()

    #encontra os contornos
    objetos,_ = cv2.findContours(img_bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_bordas, objetos, -1, (255, 0, 0), 3)

    elemento_estruturante = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    #realiza o processo de erosão pra remover as bordas indesejadas da imagem
    img_segmentada= cv2.erode(img_bordas, elemento_estruturante , iterations=2)

    return img_segmentada

def process(input_data):
    # função que deve executar fluxograma principal do processo
    dataset = open_img(input_data)

    dataset_img_segmentado = []
    for i in range(len(dataset)):
        dataset_img_segmentado.append(segmentacao(dataset[i]))

    save_img(dataset_img_segmentado)



def main():

    ap = argparse.ArgumentParser()

    ap.add_argument('-i', '--input',
                    default='imagens',
                    help='Input folder path containing test images')


    args = vars(ap.parse_args())

    process(args['input'])


if __name__ == "__main__":
    main()