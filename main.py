import cv2
from math import *
import numpy as np


def sort(list):
    list.sort()
    list1 = [() for i in range(7)]
    list1[0], list1[1] = sorted(list[0:2], key=lambda x: x[1])
    list1[2], list1[3], list1[4] = sorted(list[2:5], key=lambda x: x[1])
    list1[5], list1[6] = sorted(list[5:7], key=lambda x: x[1])
    list2 = [list1[0], list1[2], list1[5], list1[1], list1[3], list1[6], list1[4]]
    return list2


def function(list):
    global g
    global concentration
    g += 1
    list_normal = list[2]/255
    list_A = -log(list_normal, 10)
    print("Введите концетрацию(в моль/л) в(о) " + str(g) + " крышке")
    concentration.append(float(input()))
    list_component = (list_A)/(concentration[-1])
    return list_component


# Шаг 1: Загрузите изображение
image = cv2.imread('photo_2024-05-26_00-46-14.jpg')

# Шаг 2: Преобразуйте изображение в градации серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

rows = gray.shape[0]
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                          param1=100, param2=25,
                          minRadius=60, maxRadius=80)
centers = []
concentration = []
g = 0
res = np.zeros(image.shape)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        centers.append((i[0], i[1]))
print(centers)
centers = sort(centers)
co = 0
colours = [[0, 0, 0] for i in range(7)]
height, width, somth = image.shape
for i in range(30):
    for j in range(30):
        if i**2 + j**2 <= 900:
            for k in centers:
                index = centers.index(k)
                little_list = [int(image[i+k[1], j+k[0]][0]), int(image[i+k[1], j+k[0]][1]), int(image[i+k[1], j+k[0]][2])]
                colours[index][2] += little_list[0]
                colours[index][1] += little_list[1]
                colours[index][0] += little_list[2]
                co += 1
co //= len(centers)
for i in range(7):
    colours[i] = [round(colours[i][j] / co, 6) for j in range(3)]
compare_list = []
for i in range(len(colours) - 2):
    compare_list.append(function(colours[i]))
near = [[0, 0], [0, 0], [99999, 99999]]
for i in range(len(colours) - 1):
    if abs(sum(colours[6]) - sum(colours[i])) <= near[2][0]:
        near[0] = near[1]
        near[1] = near[2]
        near[2] = [abs(sum(colours[6]) - sum(colours[i])), i]
blue = [colours[near[2][1]][-1], colours[-1][-1]]
A = -log(blue[-1]/255, 10)
if blue[1]/blue[0] >= 1.3 and blue[1]-blue[0] >= 30:
    u = 1
else:
    u = 0
C = A/(compare_list[near[2][1]-u]*1.2)
print(C*320*1000)