# coding: utf-8
from __future__ import division  # 使用精确除法，即保留小数
import math
import cv2  # 暂时用opencv读取图片进行测试
# from PIL import Image # 我电脑上用不了这个包


# -------------------------------------- 计算Hu矩------------------------------
# i是行数, j是列数, 从0开始
# 调用接口是result = huMoment(image), image是200 * 300的矩阵, 下面有测试用例


# 求几何矩mpq
def mpq(p, q, image, height, width):
    m = 0L
    for i in range(0, height):
        for j in range(0, width):
            m += (i ** p) * (j ** q) * image[i][j]  # i行,j列
    return m


# 求中心矩upq
def upq(p, q, image, height, width, x0, y0):
    u = 0L
    for i in range(0, height):
        for j in range(0, width):
            u += ((i - x0) ** p) * ((j - y0) ** q) * image[i][j]  # i行,j列
    return u


# 规格化中心矩
def npq(p, q, upq_f, u00):
    r = ((p + q)/2) + 1  # ????要不要加1, 有的文献加1, 有的没加
    n = (upq_f/(u00 ** r))
    return n


# 求Hu矩的函数
def huMoment(image):
    height = 200
    width = 300

    m00 = mpq(0, 0, image, height, width)
    m01 = mpq(0, 1, image, height, width)
    m02 = mpq(0, 2, image, height, width)
    m03 = mpq(0, 3, image, height, width)
    m10 = mpq(1, 0, image, height, width)
    m11 = mpq(1, 1, image, height, width)
    m12 = mpq(1, 2, image, height, width)
    m20 = mpq(2, 0, image, height, width)
    m21 = mpq(2, 1, image, height, width)
    m30 = mpq(3, 0, image, height, width)

    x0 = int(m10 / m00 + 0.5)
    y0 = int(m01 / m00 + 0.5)

    u00 = upq(0, 0, image, height, width, x0, y0)
    u01 = upq(0, 1, image, height, width, x0, y0)
    u02 = upq(0, 2, image, height, width, x0, y0)
    u03 = upq(0, 3, image, height, width, x0, y0)
    u10 = upq(1, 0, image, height, width, x0, y0)
    u11 = upq(1, 1, image, height, width, x0, y0)
    u12 = upq(1, 2, image, height, width, x0, y0)
    u20 = upq(2, 0, image, height, width, x0, y0)
    u21 = upq(2, 1, image, height, width, x0, y0)
    u30 = upq(3, 0, image, height, width, x0, y0)

    n00 = npq(0, 0, u00, u00)
    n01 = npq(0, 1, u01, u00)
    n02 = npq(0, 2, u02, u00)
    n03 = npq(0, 3, u03, u00)
    n10 = npq(1, 0, u10, u00)
    n11 = npq(1, 1, u11, u00)
    n12 = npq(1, 2, u12, u00)
    n20 = npq(2, 0, u20, u00)
    n21 = npq(2, 1, u21, u00)
    n30 = npq(3, 0, u30, u00)

    # 计算Hu矩
    num = 7
    ele1 = n20 + n02
    ele2 = ((n20 - n02) ** 2) + 4 * (n11 ** 2)
    ele3 = ((n20 - 3 * n12) ** 2) + 3 * ((n21 - n03) ** 2)
    ele4 = ((n30 + n12) ** 2) + ((n21 + n03) ** 2)
    ele5 = (n30 + 3 * n12) * (n30 + n12) * ((n30 + n12) ** 2 - 3 * ((n21 + n03) ** 2)) + (3 * n21 - n03) * (n21 + n03) * (3 * ((n30 + n12) ** 2)-(n21 + n03) ** 2)
    ele6 = (n20 - n02) * ((n30 + n12) ** 2 - (n21 + n03) ** 2) + 4 * n11 * (n30 + n12) * (n21 + n03)
    ele7 = (3 * n21 - n03) * (n30 + n12) * ((n30 + n12) ** 2 - 3 * ((n21 + n03) ** 2)) + (3 * n12 - n03) * (n21 + n03) * (3 * ((n30 + n12) ** 2)-(n21 + n03) ** 2)
    hu_moment = [[num], [math.log10(abs(ele1)), math.log10(abs(ele2)), math.log10(abs(ele3)), math.log10(abs(ele4)), math.log10(abs(ele5)), math.log10(abs(ele6)), math.log10(abs(ele7))]]
    # hu_moment = [[num], [ele1, ele2, ele3, ele4, ele5, ele6, ele7]] # 没有对结果取对数
    return hu_moment

# __________________________________________________________________________________________________________________________________________________
# #####################函数测试部分,使用OpenCV读取图像进行测试##############################################

# 读取图像
imgName = ['test1.jpg', 'test2.jpg', 'test3.jpg']
# 存储二维图像
imageSet = []

for name in imgName:
    # 读取图片
    img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
    # 统一尺寸
    img = cv2.resize(img, (300, 200))
    # 将图像转换为二维数组格式
    sp = img.shape
    height = sp[0]
    width = sp[1]
    image = []
    for i in range(0, height):
        image_width = []
        for j in range(0, width):
            image_width.append(img[i][j])
        image.append(image_width)
    # 将二维图像存储
    imageSet.append(image)

# 算法入口
count = 1
results = []
for ima in imageSet:
    result = huMoment(ima)  # 测试Hu矩
    results.append(result)

# 输出算法结果
for res in results:
    print "---------图片%d-Hu不变矩(取对数):" % count
    print res[0], res[1]
    count += 1

# ################################################################################
