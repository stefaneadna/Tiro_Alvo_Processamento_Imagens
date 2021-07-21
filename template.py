
import argparse
import cv2
import glob
from pathlib import Path
import os
import random
import numpy as np
def open_img(path_img):
    dataset = []
    #carrega as imagens do diretorio
    for i in glob.glob(path_img + '/*.png', recursive=True):
        dataset.append(cv2.imread(i))
    for j in glob.glob(path_img + '/*.jpg', recursive=True):
        dataset.append(cv2.imread(j))
    return dataset


def save_img(dataset):
    #salva os contornos no diretorio diretorio
    if Path('teste').is_dir():
        for i in range(len(dataset)):
            cv2.imwrite('teste/img'+ str(i)+ '.png', dataset[i])
    else:
        os.mkdir('teste')
        for i in range(len(dataset)):
            cv2.imwrite('teste/img' + str(i) + '.png', dataset[i])



def segmentacao(dataset):
    img = dataset[0]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(img_gray, 70, 150)

    objetos,_ = cv2.findContours(bordas.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_bordas = bordas.copy()
    cv2.drawContours(img_bordas , objetos, -1, (255, 0, 0), 3)

    elementoEstruturante = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (2,2)
    )
    img_segmentada= cv2.erode(
        img_bordas , elementoEstruturante, iterations=2
    )

    cv2.imshow("Resultado", img_bordas )
    cv2.imshow("Bordas", img_segmentada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process(input_data):
    # função que deve executar fluxograma principal do processo
    print("teste")
    dataset = open_img(input_data)
    segmentacao(dataset)
    #save_img(dataset)

    # cv2.imshow("Imagem", dataset[5])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # aux_function_B()


def main():

    ap = argparse.ArgumentParser()

    ap.add_argument('-i', '--input',
                    default='imagens',
                    help='Input folder path containing test images')


    args = vars(ap.parse_args())

    process(args['input'])


if __name__ == "__main__":
    main()