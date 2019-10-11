import os
import dlib
import cv2
import glob


detector = dlib.simple_object_detector('detector_epi_6.svm')
print(dlib.test_simple_object_detector('treinamento_epi_6.xml','detector_epi_7.svm'))


for imagem in glob.glob(os.path.join('EPI_teste','*jpg')):
    img = cv2.imread(imagem)
    objetosDetectados = detector(img,3)
    for d in objetosDetectados:
        e,t,d,b = (int(d.left()),int(d.top()),int(d.right()),int(d.bottom()))
        cv2.rectangle(img,(e,t),(d,b),(0,0,255),2)
    cv2.imshow('img',img)
    cv2.waitKey(0)

cv2.destroyAllWindows()