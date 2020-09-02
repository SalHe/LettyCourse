from LettySchool import Ocr
import cv2
from PIL import Image
from PIL import ImageEnhance

if __name__ == '__main__':
    Ocr.init()
    Ocr.analyse_schedule(cv2.imread("table.jpg"))
