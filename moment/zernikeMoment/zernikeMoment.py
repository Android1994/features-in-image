# coding: utf-8
from __future__ import division  # 使用精确除法，即保留小数
import math
import cv2  # 暂时用opencv读取图片进行测试
# from PIL import Image # 我电脑上用不了这个包


# --------------------------------计算Zernike矩---------------------------------------------
# i是行数, j是列数, 从0开始
# 调用接口是result = zernikeMoment(image), image是200 * 300的矩阵, 下面有测试用例


# 求几何矩mpq
def mpq(p, q, image, height, width):
    m = 0L
    for i in range(0, height):
        for j in range(0, width):
            m += (i ** p) * (j ** q) * image[i][j]  # i行,j列
    return m


# 求阶乘
def factorial(n):
    m = 1
    if n < 0:
        return -1
    i = 2
    while i <= n:
        m *= i
        i += 1
    return m


# 常用阶乘
factorial_u = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 39916800]


# 获得像素极坐标半径
def getRadii(height, width, x0, y0, x, y):
    lefttop = math.sqrt((0 - x0) * (0 - x0) + (0 - y0) * (0 - y0))
    righttop = math.sqrt((width - 1 - x0) * (width - 1 - x0) + (0 - y0) * (0 - y0))
    leftbottom = math.sqrt((0 - x0) * (0 - x0) + (height - 1 - y0) * (height - 1 - y0))
    rightbottom = math.sqrt((width - 1 - x0) * (width - 1 - x0) + (height - 1 - y0)*(height - 1 - y0))

    maxRadii = lefttop
    maxRadii = (righttop if maxRadii < righttop else maxRadii)
    maxRadii = (leftbottom if maxRadii < leftbottom else maxRadii)
    maxRadii = (rightbottom if maxRadii < rightbottom else maxRadii)

    Radii = math.sqrt((x - x0) * (x - x0) + (y - y0) * (y - y0)) / maxRadii
    if Radii > 1:
        Radii = 1

    return Radii


# 获得像素极坐标角度
def getAngle(height, width, x, y):
    dia = math.sqrt(width * width + height * height)
    x0 = (int)(width / 2)
    y0 = (int)(height / 2)
    x_unity = (x - x0) / (dia / 2)
    y_unity = (y - y0) / (dia / 2)

    if (x_unity == 0) and (y_unity >= 0):
        o = math.pi / 2
    elif (x_unity == 0) and (y_unity < 0):
        o = 1.5 * math.pi
    else:
        o = math.atan(y_unity / x_unity)

    if (o * y) < 0:  # 第三象限
        o = o + math.pi

    return o


# 求Zernike矩的函数
def zernikeMoment(image):
    height = 200
    width = 300

    m00 = mpq(0, 0, image, height, width)
    m01 = mpq(0, 1, image, height, width)
    m10 = mpq(1, 0, image, height, width)

    x0 = int(m10 / m00 + 0.5)
    y0 = int(m01 / m00 + 0.5)

    R = [0] * 25
    V = [0] * 25
    M = [0] * 4
    Ze = [0] *25

    for n in range(0, 5):
        for m in range(0, 5):  # 只计算以下阶数
            if ((n == 1 and m == 0) or (n == 1 and m == 1) or (n == 2 and m == 0) or (n == 2 and m == 1) or (n == 2 and m == 2)
               or (n == 3 and m == 0) or (n == 3 and m == 1) or (n == 3 and m == 2) or (n == 3 and m == 3) or (n == 4 and m == 0)
               or (n == 4 and m == 1) or (n == 4 and m == 2) or (n == 4 and m == 3) or (n == 4 and m == 4)):
                for y in range(0, height):
                    for x in range(0, width):
                        s = 0
                        while (s <= (n - m) / 2) and (n >= m):
                            temp1 = (factorial(n-s) if n-s > 10 else factorial_u[n-s])
                            temp2 = (factorial(s) if s > 10 else factorial_u[s])
                            temp3 = (factorial((n + m) / 2 - s) if ((n + m) / 2 - s) > 10 else factorial_u[(int)((n + m) / 2) - s])
                            temp4 = (factorial((n - m) / 2 - s) if ((n - m) / 2 - s) > 10 else factorial_u[(int)((n - m) / 2) - s])
                            R[n*5+m] += (math.pow(-1.0, s)
                                         * temp1
                                         * math.pow(getRadii(height, width, x0, y0, x, y), (n - 2 * s))
                                         / (temp2 * temp3 * temp4)
                                         )
                            s += 1

                        Ze[n*5+m] += (R[n*5+m]
                                      * image[y][x]
                                      * math.cos(m * getAngle(height, width, x, y)))  # 实部
                        V[n*5+m] += (R[n*5+m]
                                     * image[y][x]
                                     * math.sin(m * getAngle(height, width, x, y)))  # 虚部
                        R[n*5+m] = 0

                Ze[n * 5 + m] = math.sqrt((Ze[n * 5 + m] ** 2) + (V[n * 5 + m] ** 2)) * (n + 1) / math.pi / m00
                # Ze[n * 5 + m] = math.log10(abs(Ze[n * 5 + m]))  # 取对数

    zernike_moment = [[14], [Ze[5], Ze[6], Ze[10], Ze[11], Ze[12], Ze[15], Ze[16], Ze[17], Ze[18], Ze[20], Ze[21], Ze[22], Ze[23], Ze[24]]]

    return zernike_moment

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
    result = zernikeMoment(ima)  # 测试zernike矩
    results.append(result)

# 输出算法结果
for res in results:
    print "---------图片%d-zernike不变矩(取14个):" % count
    print res[0], res[1]
    count += 1

# ################################################################################
