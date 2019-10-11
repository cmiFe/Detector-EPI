import sys
import cv2
import imutils
from imutils.video import VideoStream
import dlib
import multiprocessing

video = cv2.VideoCapture(0)
detector = dlib.simple_object_detector('detector_epi_6.svm')
queue_from_cam = multiprocessing.Queue()
outputQueue = multiprocessing.Queue()
objetosDetectados = []
contaFrame = 0
pulaFrame = 2

def detectaObjetos(queue_from_cam,outputQueue):
    while True:
        if not queue_from_cam.empty():
            frame = queue_from_cam.get()
            objetosDetectados = detector(frame,1)
            outputQueue.put(objetosDetectados)


if __name__ == '__main__':
    processo = multiprocessing.Process(target=detectaObjetos,args=(queue_from_cam,outputQueue,))
    processo.daemon = True
    processo.start()
    while video.isOpened():
        ret,frame = video.read()
        contaFrame +=1
        if contaFrame % pulaFrame == 0:
            if queue_from_cam.empty():
                queue_from_cam.put(frame)
            if not outputQueue.empty():
                objetosDetectados = outputQueue.get()
            for i in objetosDetectados:
                e,t,d,b = (int(i.left()),int(i.top()),int(i.right()),int(i.bottom()))
                cv2.rectangle(frame,(e,t),(d,b),(0,0,255),2)
        cv2.imshow('img',frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

cv2.destroyAllWindows()
video.release()
sys.exit(0)
