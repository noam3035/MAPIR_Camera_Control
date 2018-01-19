import os
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.uic as uic
import cv2
import copy
import numpy as np
VIGNETTE_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'MAPIR_Processing_dockwidget_vignette.ui'))
modpath = os.path.dirname(os.path.realpath(__file__))
POS_DICT = {
    "3.2MP, 9.6mm, 850": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 1),
                          (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3),
                          (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                          (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                          (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 0),
                          (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2),
                          (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
                          (8, 5), (8, 6), (8, 7), (8, 8)],
    "3.2MP, 9.6mm, 550": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 1),
                          (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3),
                          (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                          (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                          (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 0),
                          (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2),
                          (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
                          (8, 5), (8, 6), (8, 7), (8, 8)],
    "3.2MP, 9.6mm, 615": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 1),
                          (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3),
                          (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                          (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                          (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 0),
                          (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2),
                          (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
                          (8, 5), (8, 6), (8, 7), (8, 8)],

    "3.2MP, 9.6mm, 725": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 1),
                          (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3),
                          (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                          (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                          (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 0),
                          (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2),
                          (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
                          (8, 5), (8, 6), (8, 7), (8, 8)],

    "3.2MP, 9.6mm, 808": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 1),
                          (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3),
                          (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                          (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                          (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 0),
                          (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2),
                          (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4),
                          (8, 5), (8, 6), (8, 7), (8, 8)]

}

C_DICT = {
    "3.2MP, 9.6mm, 850": [1.003, 0.067623, -3.9727, 0.30708, 19.359, -1.6042, -46.663, 2.4414, 38.547, 0.05715,
                          -0.13491, -0.64939, 1.0447, 0.64835, -5.1295, 1.7349, 9.2829, -0.80875, -7.7209, -0.33443,
                          43.672, 3.1075, -123.06, -6.9536, 109.57, 0.47653, 51.231, -1.3333, 2.1064, 9.1885, -5.0854,
                          -10.789, 6.6426, -4.2704, -4.0212, 0.42696, 55.726, 1.3079, -196.63, -11.687, 252.24, 12.44,
                          1.3725, 6.3119, -22.286, 7.5707, -11.446, -34.972, 11.31, 20.906, 3.6809, 7.9937, -1.6831,
                          3.2193, -209.37, -1.9524, 323.93, 11.62, -44.267, 4.7519, -60.864, 1.1256, -25.303, -13.71,
                          20.464, 37.801, -7.2115, 13.51, -2.0276, 3.815, -1.2111, 1.4413, 296.43, -0.21929, -49.199,
                          1.9409, -85.617, 0.27295, -37.273, -0.31045, -12.106],

    "3.2MP, 9.6mm, 550": [1.0028, 0.030866, -0.9088, 0.0087242, -1.8067, 0.013787, 11.449, -0.23185, -18.829, -0.010119,
                          -0.10686, 0.31075, 1.7413, -3.075, -6.8767, 6.28, 8.7722, 2.6575, -3.2751, -0.13948, 5.9773,
                          2.0461, -14.759, -8.7919, 1.0834, 9.7631, 64.402, 0.16078, 1.1955, -4.2614, -16.1, 24.133,
                          41.981, -4.9668, -37.938, -61.141, 6.3119, 0.11322, -46.294, -9.7681, 205.56, 23.819, -176.31,
                          -14.651, -81.8, -0.69136, -4.9194, 15.515, 56.504, -33.455, -40.654, -64.852, -32.264,
                          -41.144, -8.5747, 0.31265, 176.16, 23.696, -363.43, 18.023, -209.6, -4.581, -69.433, 1.1177,
                          7.2155, -11.382, -79.264, -34.658, -41.083, -36.155, -15.136, -17.558, 4.243, 0.38789, -191.1,
                          -55.756, -244.53, -15.957, -98.037, -7.081, -29.173],

    "3.2MP, 9.6mm, 615": [1.0027, 0.029612, -0.88886, 0.029951, -1.0866, 0.054713, 8.3285, -0.4946, -14.662, 0.012939,
                          -0.11643, -0.04947, 1.5018, -1.0442, -6.5253, 7.7437, 9.5425, -14.567, -3.0971, -0.04477,
                          4.9477, -0.50201, -8.032, -2.775, -5.469, 14.279, 38.59, -0.38885, 1.3482, 0.96373, -14.784,
                          -0.3003, 48.893, 2.4337, -29.178, -18.037, 5.2606, -0.041947, -34.312, 5.0956, 129.71, 3.3542,
                          -70.572, -23.793, -35.54, 2.9201, -4.8475, -3.0852, 40.203, 12.51, -99.264, -13.334, -56.794,
                          -18.254, -5.2279, -2.9605, 155.73, 7.3866, -298.05, -46.945, -130.64, -28.967, -38.935,
                          -6.1273, 4.0739, 1.699, 7.6238, -33.802, -51.185, -20.778, -24.939, -10.769, 1.1419, 9.286,
                          -213.44, -15.023, -199.07, -29.631, -64.826, -14.174, -17.323],

    "3.2MP, 9.6mm, 725": [1.0029, 0.039098, -1.0014, 0.02838, 0.22629, -0.58043, 2.936, 1.2747, -5.8326, 0.060629,
                          -0.058377, -0.162, 1.1359, 0.086272, -7.298, 0.42058, 14.444, 0.87893, -3.0799, -0.58293,
                          7.4569, 3.6709, -22.371, -14.791, 36.804, 22.091, -11.973, -0.17597, 0.13502, 0.74392,
                          -4.7027, 4.8825, 36.192, -10.145, -50.044, 3.8438, 6.4152, 5.1805, -47.642, -19.798, 176.47,
                          13.353, -120.37, 39.791, -78.182, 0.29679, 3.7295, 1.613, -25.411, -18.328, -20.536, -15.43,
                          -25.206, -4.9083, -11.277, -23.491, 176.65, 30.004, -334.7, 39.343, -164.98, 25.822, -56.432,
                          0.18976, -13.135, -6.0877, 97.212, -9.3171, 16.173, -4.5982, -1.9369, -1.3945, 12.571, 39.086,
                          -214.08, 16.324, -220.37, 18.334, -77.656, 10.25, -22.714],

    "3.2MP, 9.6mm, 808": [1.0023, 0.025352, -1.3251, 0.38706, 1.3963, -2.6798, 1.466, 5.4697, -7.0036, -0.025544,
                          -0.12072, -0.028576, 1.36, 1.5008, -5.2585, -6.1745, 6.8156, 6.9049, -3.7878, 0.011141,
                          11.258, -2.6083, -29.7, 13.39, 37.39, -25.891, 19.451, 0.315, 1.4645, -1.8421, -13.163,
                          -5.6545, 34.258, 33.679, -15.81, -27.387, 12.672, -0.016697, -66.15, 9.6174, 177.59, -6.3116,
                          -141.32, -6.6181, -81.428, -1.5184, -5.7607, 14.924, 41.323, 10.317, -58.943, -45.138,
                          -34.365, -34.659, -34.296, -4.7785, 214.12, -7.467, -265.58, -13.861, -161.08, -6.9337,
                          -57.897, 2.7338, 7.1747, -26.372, -30.07, -42.416, -36.919, -35.092, -15.508, -16.217, 42.968,
                          16.323, -246.6, -35.012, -204.99, -14.882, -79.394, -4.2923, -24.095]

}
class Vignette(QtWidgets.QDialog, VIGNETTE_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Vignette, self).__init__(parent=parent)
        self.parent = parent

        self.setupUi(self)
    def on_VignetteSaveButton_released(self):
        # c1 = float(self.VignetteCoef.text())
        h, w = self.parent.display_image_original.shape[:2]
        pict = cv2.imread(self.parent.KernelBrowserFile.text(), -1)
        # vig_image = cv2.imread(modpath + os.sep + "Vignettes" + os.sep + "vig_615.tif", -1)
        # pict = pict / vig_image

        # cx = w/2
        # cy = h/2
        # np.array((key for (key, val) in POS_DICT.items())).astype("float64")
        # i_list = []
        # j_list = []
        # vig_image = np.ones((h, w),np.dtype("float32"))
        # vig_image = cv2.imread(modpath + os.sep + "Vignettes" + os.sep + "vig_615.tif", -1)
        # if len(pict.shape) > 2:
        #     b, g, r = cv2.split(pict)
        #     b = b / vig_image
        #     g = g / vig_image
        #     r = r / vig_image
        #     pict = cv2.merge((b,g,r))
        # else:
        #     pict = pict / vig_image
        #
        # for (i, j) in POS_DICT[str(self.VigSensorSelect.currentText()) + ", " + str(self.VigLensSelect.currentText()) + ", " + str(self.VigFilterSelect.currentText())]:
        #     i_list.append(i)
        #     j_list.append(j)
        try:
            # for Y in range(self.parent.display_image_original.shape[:2][0]):
            #     for X in range(self.parent.display_image_original.shape[:2][1]):
            #         # dx = (x - cx)/(w/2)
            #         # dy = (y - cy)/(h/2)
            #         #
            #         # r2 = (dx*dx) + (dy*dy)
            #         x = X - (w/2)
            #         y = Y - (h/2)
            #         # for n in range(len(POS_DICT["3.2MP, 9.6mm, 850"])):
            #         vig_image[Y, X] = sum(C_DICT[str(self.VigSensorSelect.currentText()) + ", " + str(self.VigLensSelect.currentText()) + ", " + str(self.VigFilterSelect.currentText())][:] * (np.power((x/w), i_list) * np.power((y/h), j_list)))
            #
            #         # pict[y, x] = (pict[y, x] * (1 + (c1 * r2)))
            #         # pict[Y, X] = pict[Y, X] / v
            # with open(modpath + os.sep + r"Vignettes" + os.sep + r"vig_image.txt", "wb") as vigfile:
            #     vigfile.write(bytes(vig_image.data))


            with open(modpath + os.sep + r"Vignettes" + os.sep + r"vig_" + str(self.VigFilterSelect.currentText()) + r"image.txt", "rb") as vigfile:
                v_array = np.ndarray((h, w), np.dtype("float32"), np.fromfile(vigfile, np.dtype("float32")))
                pict = pict / v_array
                pict = pict / 65535.0
                pict = pict * 255.0
                pict = pict.astype("uint8")

            if pict.dtype == np.dtype("uint16"):
                pict = pict / 65535.0
                pict = pict * 255.0
                pict = pict.astype("uint8")
            elif pict.dtype == np.dtype("float32"):
                pict = pict / np.finfo("float32").max
                pict = pict * 255.0
                pict = pict.astype("uint8")
            # mx = pict.max()  # np.percentile(pict, 98)
            # mn = pict.min()  # np.percentile(pict, 2)
            if len(pict.shape) > 2:
                pict = cv2.cvtColor(pict, cv2.COLOR_BGR2RGB)
            else:
                pict = cv2.cvtColor(pict, cv2.COLOR_GRAY2RGB)
            # pict[pict > mx] = mx
            # pict[pict < mn] = mn
            self.parent.display_image_original = pict
            self.parent.display_image = pict

            if self.parent.calcwindow:
                self.parent.calcwindow.processIndex()
            if self.parent.LUTwindow:
                self.parent.LUTwindow.RasterMin.setText(str(round(self.parent.LUT_Min, 2)))
                self.parent.LUTwindow.RasterMax.setText(str(round(self.parent.LUT_Max, 2)))
                self.parent.LUTwindow.processLUT()
            self.parent.applyLUT()
            self.parent.applyRaster()
            self.parent.stretchView()
            # if len(pict.shape) > 2:
            #     pict = cv2.cvtColor(pict, cv2.COLOR_BGR2RGB)
            #     img2 = QtGui.QImage(pict, w, h, w * 3, QtGui.QImage.Format_RGB888)
            # else:
            #     img2 = QtGui.QImage(pict, w, h, w , QtGui.QImage.Format_Grayscale8)

        except Exception as e:
            print(e)
    def on_VignetteCloseButton_released(self):
        self.close()