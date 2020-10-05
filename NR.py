#!/usr/bin/python
# -*- coding: utf-8 -*-
# Programa Cliente

import sys
import random

def numRandomicoReal():
    return random.random()

def numRandomicoUnoToN(N):
    return random.randint(1, N)

def initPoblacion(tamPoblacion,tamTablero):
    poblacion = []
    for i in range(tamPoblacion):
        tmp = list(range(1, tamTablero+1))
        random.shuffle(tmp)
        poblacion.append(tmp)
    return poblacion

def calcFitness (individuo):
    contador=0
    for i in range(1,len(individuo)+1):
        for j in range(1,len(individuo)+1):
            if (((i-j==individuo[i-1]-individuo[j-1]) or ((i-j)+(individuo[i-1]-individuo[j-1]))==0) and (individuo[i-1]!=individuo[j-1])):
                    contador=contador+1
    return contador

def selecIndividuoRuleta (poblacion):
    fitnes = [] #o ruleta...
    sumador = 0.
    temp = 0 #dice que no se usa, pero bajo mi logica deberia estar aqui.

    for number in range(len(poblacion)): #este for es solo para obtener la sumatoria completa de la version invertida. 1/x
        sumador = (1/calcFitness(poblacion[number])) + sumador

    for x in range(len(poblacion)):
        if x == 0:
            fitnes.append((1/calcFitness(poblacion[x])/sumador))
        else:
            temp = (1/calcFitness(poblacion[x]))/sumador
            fitnes.append((temp)+fitnes[x-1])

    seleccion = numRandomicoReal()
    for x in range(len(fitnes)):
        if(x == 0):
            if(seleccion<fitnes[x]):
                seleccion = x
        else:
            if seleccion>fitnes[x-1] and seleccion<fitnes[x]:
                seleccion = x
    print(fitnes)
    return seleccion #deberia devolver entre 0 y el tamaño de la poblacion -1

def correccionIndividuo(individuo):
    #EN PROCESO
    return individuoCorregido

def cruzaIndividuos(individuoA,individuoB):
    separacion = numRandomicoUnoToN(len(individuoA))

    #Separamos los individuos
    a1 = individuoA[:separacion]
    a2 = individuoA[separacion:]
    b1 = individuoB[:separacion]
    b2 = individuoB[separacion:]

    #unimos mezclando
    newIndividuoA = a1+b2
    newIndividuoB = b1+a2

    newIndividuos = []
    newIndividuos.append(newIndividuoA)
    newIndividuos.append(newIndividuoB)

    return newIndividuos

def mutacionIndividuo(individuo):
    #en proceso
    return individuoMutado

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print ("No ha ingresado todos los parametros solicitados.")
        sys.exit(0)
    semilla = int(sys.argv[1])
    tamTablero = int(sys.argv[2]) #Considere si el tablero es de 9x9 entonces ingrese un 9
    tamPoblacion = int(sys.argv[3])
    probCruza = int(sys.argv[4])
    probMutacion = int(sys.argv[5])
    numIteraciones = int(sys.argv[6]) #generaciones

    random.seed(semilla) #Asignamos la semilla al random.

    poblacion = initPoblacion(tamPoblacion,tamTablero)
    print(cruzaIndividuos(poblacion[0],poblacion[1]))

