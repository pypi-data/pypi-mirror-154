# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import numpy as np
from PySide2.QtGui import (
    QImage,
    qRgb
)

gray_color_table = [qRgb(i, i, i) for i in range(256)]


def toQImage(im, copy=False):
    if im is None:
        return QImage()

    if im.dtype == np.uint8:
        if len(im.shape) == 2:
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim.copy() if copy else qim

        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
                return qim.copy() if copy else qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                return qim.copy() if copy else qim


def toArray(im):
    if im is None:
        return np.empty()

    width = im.width()
    height = im.height()

    if im.depth() == 8:
        im = im.convertToFormat(QImage.Format.Format_Indexed8)
        ptr = im.constBits()
        arr = np.array(ptr).reshape(height, width, 2)
        return arr

    elif im.depth() == 32:
        check = im.hasAlphaChannel()
        if check is False:
            im = im.convertToFormat(QImage.Format.Format_RGB888)
            ptr = im.constBits()
            arr = np.array(ptr).reshape(height, width, 3)
            return arr
        elif check is True:
            im = im.convertToFormat(QImage.Format.Format_ARGB32)
            ptr = im.constBits()
            arr = np.array(ptr).reshape(height, width, 4)
            return arr
