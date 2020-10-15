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
        if(calcFitness(poblacion[number]) == 0): #CLARO ESTA, QUE SI EL FITNESS ES 0 ENTONCES NO PODEMOS DIVIDIR 1/0 , POR ENDE LO VOLVEREMOS 1, PARA CONSIDERARLO UN VALOR CON MAYOR PROBABILIDAD, YA QUE ES PERFECTO.
            sumador = (1 / 1) + sumador
        else:
            sumador = (1/calcFitness(poblacion[number])) + sumador

    for x in range(len(poblacion)):
        if x == 0:
            if (calcFitness(poblacion[x]) == 0):
                fitnes.append((1/1)/sumador)
            else:
                fitnes.append((1/calcFitness(poblacion[x])/sumador))
        else:
            if (calcFitness(poblacion[x]) == 0):
                temp = (1 / 1) / sumador
            else:
                temp = (1 / calcFitness(poblacion[x])) / sumador
            fitnes.append((temp)+fitnes[x-1])

    seleccion = numRandomicoReal()
    for x in range(len(fitnes)):
        if(x == 0):
            if(seleccion<fitnes[x]):
                seleccion = x
        else:
            if seleccion>fitnes[x-1] and seleccion<fitnes[x]:
                seleccion = x
    return poblacion[seleccion] #devuelvo el individuo seleccionado

def correccionIndividuo(individuo):
    ubicacion = []
    faltan = [0] * len(individuo) #aqui marco con 1 los que si estan y los que faltan quedan en cero

    for i in range(len(individuo)):
        for j in range(i,len(individuo)):
            faltan[individuo[i]-1]=1 #marcado de los que si estan
            if ((individuo[i] == individuo[j]) and i!=j):
                ubicacion.append(j)

    for i in range(len(faltan)):
        if (faltan[i]==0):
            individuo[ubicacion[0]] = i+1
            del ubicacion[0]

    return individuo# individuoCorregido

def cruzaIndividuos(individuoA,individuoB): #OJO que el profesor en clases cuando hacia decendencia salian 2 hijos y yo hago lo mismo.
    separacion = numRandomicoUnoToN(len(individuoA)-1)

    #Separamos los individuos
    a1 = individuoA[:separacion]
    a2 = individuoA[separacion:]
    b1 = individuoB[:separacion]
    b2 = individuoB[separacion:]

    #unimos mezclando
    newIndividuoA = a1+b2
    newIndividuoB = b1+a2

    #corregimos los hijos
    newIndividuoA = correccionIndividuo(newIndividuoA)
    newIndividuoB = correccionIndividuo(newIndividuoB)

    #Unimos ambas listas para poder retornarlas (ambos hijos
    newIndividuos = []
    newIndividuos.append(newIndividuoA)
    newIndividuos.append(newIndividuoB)

    return newIndividuos #AHI SE VAN LOS HIJOS

def mutacionIndividuo(individuo):
    numero1 = numRandomicoUnoToN(len(individuo)-1)
    numero2 = numRandomicoUnoToN(len(individuo)-1)
    while(numero1 == numero2):
        numero2 = numRandomicoUnoToN(len(individuo)-1)
    tmp = individuo[numero1]
    individuo[numero1] = individuo[numero2]
    individuo[numero2] = tmp
    return individuo

def reduccionPob(poblacionTotal):
    for j in range (len(poblacionTotal)):
        valorInicial = calcFitness(poblacionTotal[j])
        posicion = j
        for i in range (j,len(poblacionTotal)):
            newValor = calcFitness(poblacionTotal[i])
            if (valorInicial > newValor):
                posicion = i
                valorInicial = newValor
        poblacionTotal.insert(j,poblacionTotal.pop(posicion))
    return (poblacionTotal[0:int(len(poblacionTotal)/2)])

def generarPobHijos(poblacion,probCruza,probMutacion):
    poblacionHijos = []
    while (len(poblacionHijos)<len(poblacion)):
        if (probCruza/100 >= numRandomicoReal()):
            individuo = cruzaIndividuos(selecIndividuoRuleta(poblacion),selecIndividuoRuleta(poblacion))
            if(probMutacion/100 >= numRandomicoReal()):
                individuo[0] = mutacionIndividuo(individuo[0]) #  que mute el primer hijo
            if (probMutacion / 100 >= numRandomicoReal()):
                individuo[1] = mutacionIndividuo(individuo[1])  # que mute el segundo hijo
            poblacionHijos += (individuo)
    if(len(poblacionHijos)>len(poblacion)): #PARA QUE LA CANTIDAD DE HIJOS SEAN IGUAL A LA CANTIDAD DE PADRES, BORRAMOS UNO YA QUE LA CRUZA NOS DA 2 HIJOS NO UNO.
        poblacionHijos.pop(0)
    return poblacionHijos

def existeSol (poblacion):
    soluciones = []
    for i in range(len(poblacion)):
        if (calcFitness(poblacion[i])==0):
            soluciones.append(poblacion[i])
    return soluciones


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

    poblacionInicial = initPoblacion(tamPoblacion, tamTablero)

    bandera =0
    for x in range(numIteraciones):
        hijos = generarPobHijos(poblacionInicial,probCruza,probMutacion)
        nuevaPoblacion = reduccionPob(poblacionInicial+hijos)
        poblacionInicial.clear()
        hijos.clear()
        poblacionInicial = nuevaPoblacion
        sol = existeSol(poblacionInicial)
        if(len(sol)!=0):
            print("Se encontro/encontraron la(s) siguiente(s) solucion(es) :", sol)
            bandera = 1
            break
        else:
            sol.clear()
    if(bandera==0):
        print("No se encontraron soluciones!")