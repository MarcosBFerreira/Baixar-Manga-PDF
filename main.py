import os

import img2pdf
from skimage import io
import cv2
import requests
from io import BytesIO
from pypdf import PdfMerger


pdfs = []
imagens = []
mesclar = PdfMerger()

i = 1
nome_manga = input('NOME DO MANGÁ: ')
cap = int(input('NÚMERO DO CAPÍTULO: '))
link_original = input('DIGITE O LINK DA PRIMEIRA IMAGEM DO MANGÁ: ')

while True:

    link = link_original.split('/')
    link[-1] = link[-1].replace('1', f'{i}')
    link = '/'.join(link)
    response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        link = io.imread(BytesIO(response.content))

        cv2.imwrite(f'{i}.jpg', cv2.cvtColor(link, cv2.COLOR_BGR2RGB))

    except:
        break

    pdf_bytes = img2pdf.convert(f'{i}.jpg')
    pdf = open(f'{i}.pdf', 'wb')
    pdf.write(pdf_bytes)
    pdfs.append(f'{i}.pdf')
    imagens.append(f'{i}.jpg')
    pdf.close()
    i += 1


for pdf in pdfs:

    mesclar.append(pdf)

mesclar.write(f'{nome_manga} - Capítulo {cap}.pdf')
mesclar.close()

for i in range(len(pdfs)):
    os.remove(pdfs[i])
    os.remove(imagens[i])
