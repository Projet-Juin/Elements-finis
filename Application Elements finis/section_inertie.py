# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 18:02:26 2020

@author: Clara
"""
import math

def getInertie(N, entrees):
    if N==0:
        return carré(1,*entrees)
    elif N==1:
        return carré_creux(1,*entrees)
    elif N==2:
        return rectangle(1,*entrees)
    elif N==3:
        return rectangle_creux(1,*entrees)
    elif N==4:
        return I(1,*entrees)
    elif N==5:
        return T(1,*entrees)
    elif N==6:
        return L(1,*entrees)
    elif N==7:
        return Z(1,*entrees)
    elif N==8:
        return triangle_rectangle(1,*entrees)
    elif N==9:
        return cercle(1,*entrees)
    elif N==10:
        return cercle_creux(1,*entrees)
    elif N==11:
        return demi_cercle(1,*entrees)
    elif N==12:
        return quart_cercle(1,*entrees)
    elif N==13:
        return ovale(1,*entrees)
    elif N==14:
        return croix(1,*entrees)
    elif N==15:
        return losange(1,*entrees)

def carré(L, b) :
    S = b**2
    Igz = pow(b,4)/12
    volume = S*L
    return Igz, volume

def carré_creux(L, b, b1) :
    S = b**2 - b1**2
    Igz = ((b**4)-(b1**4))/12
    volume = S*L
    return Igz, volume

def rectangle(L, b, h) :
    S = h*b
    Igz = (b *(pow(h,3)))/12
    volume = S*L
    return Igz, volume

def rectangle_creux(L, b, h, b1, h1) :
    S = h*b - h1*b1
    Igz = ((b*(h**3)) - b1*(h1**3))/12
    volume = S*L
    return Igz, volume

def I(L, b, h, b1, b2, h1) :
    S = h1*(b - b1 - b2) + h*(b1 + b2)
    Igz =  (2*b*(h1**3)+((h**3)-(h1**3))*(b1 + b2)) / 24
    volume = S*L
    return Igz, volume

def T(L, b, h, b1, h1) :
    S = b1*h - h1*(b1 - b)
    Igz =  (b*(h1**3)+((h**3)-(h1**3))*b1) / 12
    volume = S*L
    return Igz, volume

def L(L, b, h, b1, h1) :
    S = h*b1 - h1*(b1-b)
    Igz = (b*(h1**3)+((h**3)-(h1**3))*b1) / 12
    volume = S*L
    return Igz, volume

def Z(L, b, h, b1, b2, h1) :
    S =  h1*(b-b1-b2)+h*(b1+b2)
    Igz = (2*b*(h1**3)+((h**3)-(h1**3))*(b1+b2)) / 24
    volume = S*L
    return Igz, volume

def triangle_rectangle(L, b, h) :
    S = h*b/2
    Igz = b*(h**3)/36
    volume = S*L
    return Igz, volume

def cercle(L, R) :
    S = math.pi * R**2
    Igz = math.pi* (R**4) / 4
    volume = S*L
    return Igz, volume

def cercle_creux(L, R, R1) :
    S = math.pi * (R**2 - R1**2)
    Igz = math.pi*((R**4)-(R1**4)) / 4
    volume = S*L
    return Igz, volume

def demi_cercle(L, R) :
    S = math.pi*(R**2)/2
    Igz =  (R**4)*((math.pi/8)-(8/(9*math.pi)))
    volume = S*L
    return Igz, volume

def quart_cercle(L, R) :
    S = (math.pi*((R)**2))/4
    Igz = (R**4)*((math.pi/8) - (8/(9*math.pi))) / 2
    volume = S*L
    return Igz, volume

def ovale(L, D2, D1) :
    S = (math.pi*D1*D2) / 4
    Igz = (math.pi*D1*(D2**3)) / 64
    volume = S*L
    return Igz, volume

def croix(L, b, h) :
    S = 2*b*h - b**2
    Igz = (b*(h**3)+(b**3)*h-(b**4))/12
    volume = S*L
    return Igz, volume

def losange(L, D2, D1) :
    S = D1*D2 / 2
    Igz = (D1**3)*D2 / 48
    volume = S*L
    return Igz, volume


        


    