import numpy as np
import random as random
import math
import time
import copy 

import flpwebProject.externals.FuncionObjetivo as fo



def busquedaVecindarioSecuencial(A):
    """
    Devuelve un array de todo el vecindario a explorar en orden

    Parameters:
    A: Vector Solución 
    matrices: np array de matriz con todas las matrices
    Salidas:
    vecindario: np array con el vecindario

    Nota: en la posición cero, queda el array solucion
    """
    vecindario = []
    vecindario.append(A)
    n = len(A)
    contador = 0
    for i in range(n):
        for j in range(i+1,n):
            y = copy.deepcopy(A) #Hace una copia
            anterior = A[i] #Almacena el anterior
            posterior = A[j] ##Almacena el posterior
            y[j] = anterior #Cambia el siguiente con el anterior
            y[i] = posterior #cambia el anterior con el siguiente
            contador = contador +1
            vecindario.append(y) #Adiciona el vector arreglado
    return np.asarray(vecindario)



def busquedaVecindarioAleatoria(A):
    """
 
    Parameters:
    A: np array, array solución con aleatorio
    
    Salidas:
    vecindario: np array con el vecindario
    

    """
    X0 = copy.deepcopy(A)#copia el vector

    #Obtiene dos aleatorios para el intercambio
    ran_1 = np.random.randint(0,len(X0))
    ran_2 = np.random.randint(0,len(X0))
    
    #asegura que las dos posiciones sean aleatorias
    while ran_1==ran_2:
        ran_2 = np.random.randint(0,len(X0))
    
    XT = [] #Nueva vector solución con
    A1 = X0[ran_1]
    A2 = X0[ran_2]
    w = 0
    #Hace el intercambio
    for i in X0:
        if X0[w]==A1:
            XT = np.append(XT,A2)
        elif X0[w]==A2:
            XT = np.append(XT,A1)
        else:
            XT=np.append(XT,X0[w])
        w = w+1
    return np.asarray(XT,dtype=int)

def calculoTiTf(matrices,A,K,lambdas=np.array([0.5,0.05]),simetria=True):
    """
    Calcula la Ti y la Tf
    Parameters
    matrices : numpy array de Matriz que contiene las matrices
    simetria : si las matrices son simétricas o no


    """
    Acopy = copy.deepcopy(A)
    n = len(Acopy)
    matrixes = copy.deepcopy(matrices) 
    R = int(K/2) 
    # ZInicial = fo.funcionObjetivo(matrixes,A,A)#Funcion objetivo de la primera solucion que es [1,2,3,4,...,n]
    vecindario= [ busquedaVecindarioAleatoria(Acopy) for x in range(R)]
    Z = [fo.funcionObjetivo(matrixes,x,simetria) for x in vecindario]
    dif = [ abs(Z[i]-Z[j]) for i in range(n) for j in range(i+1,n)]
    #List comprehension link
    #https://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/
    # Es lo mismo que la línea de arriba
    # dif= []
    # for i in range(len(Z)):
    #     for j in range(i+1,n):
    #         dif.append(abs(Z[i]-Z[j]))
    Zmin = min(dif)
    Zavg = np.mean(dif)
    Ti = ((1-lambdas[0])*Zmin)+(lambdas[0]*Zavg)
    Tf = ((1-lambdas[1])*Zmin)+(lambdas[1]*Zavg)
    return Ti, Tf


 ###########################################################################

def recocidoSimulado(parametros,matrices,simetria):
    """
    Calcula la mejor funcion objetivo de las matrices que se ingresan

    Parameters:
    matrices: matriz array las matrices con las que se va a trabajar
    simetria: True si las matrices son simétricas, 
              False caso contrario
    Q:        int Numero de iteraciones que va a trabajar el sa
    lambdas: np array contiene los porcentajes para hacer el cálculo de Ti y Tf    

    Return:
    aFOBest,valsFOTemps,tempInicialFinal
    aFOBest: np array que contiene en la posicion 0 la mejor FO y en la 1 el vector sln de esa FO
    valsFOTemps: np array que contiene en la posicion 0 un vector con todos los valores de FO
                 en la posicion 1 un vector con todos los valores de temperatura 
                 estos datos son los que arrojo durante toda la ejecución el SA
    tempInicialFinal: np array que contiene en la posicion 0 la Ti y en la 1 la Tf
    """
    lambda1,lambda2,Q = parametros
    start = time.time()
    n = matrices[0].getNumpyMatrix().shape[0]#TAMAÑO DEL PROBLEMA
    Ainicial = [x for x in range(1,n+1)]#SOLUCION INICIAL, n+1, para que llegue hasta el final del tamaño
    Ainicial = np.asarray(Ainicial)
    K = n*(n-1)/2 #K = SALTOS
    L = Q*K #Schedule Length
    L = int(L)
    lambdas = np.array([lambda1,lambda2])
    Ti, Tf = calculoTiTf(matrices,Ainicial,K,lambdas,simetria)
    tempInicialFinal = [Ti,Tf]
    beta = (Ti-Tf)/(L*Ti*Tf)#cooling annealing schedule
    t = Ti #Temperatura
    i = 0
    j = 0
    # A = np.copy(Ainicial)
    Abest = copy.deepcopy(Ainicial) 
    mejoresA = []
    mejoresA.append(Abest)
    funcionObjABest = 0
    iters=0
    valsFuncObjetivo = []
    funObjAInicial = fo.funcionObjetivo(matrices,Ainicial,simetria)
    valsFuncObjetivo.append(funObjAInicial)
    mejoresFunObj = []
    mejoresFunObj.append(funObjAInicial)
    valsTemperaturas = []
    valsTemperaturas.append(t)
    funObjAprima = 0
    Aprima = copy.deepcopy(Ainicial)
    while(iters<=L-1):
        contador = 0
        for i in range(n):
            for j in range(i+1,n):
                aActual = copy.deepcopy(Aprima) #aActual es el que va cambiando
                anterior = Aprima[i] #Almacena el anterior
                posterior = Aprima[j] ##Almacena el posterior
                aActual[j] = anterior #Cambia el siguiente con el anterior
                aActual[i] = posterior #cambia el anterior con el siguiente
                contador = contador +1
                funObjAprima =fo.funcionObjetivo(matrices,Aprima,simetria)
                funObjAActual =fo.funcionObjetivo(matrices,aActual,simetria)
                delta = funObjAActual - funObjAprima
                if(delta<0):
                    #Si se cumple, haga el nuevo A en el que se hizo el cambio
                    Aprima = copy.deepcopy(aActual)
                else:
                    aleatorio = random.random()
                    exponencial = math.exp(-delta/t)
                    if (aleatorio<exponencial):
                        Aprima = copy.deepcopy(aActual)
                funcionObjABest = fo.funcionObjetivo(matrices,Abest,simetria)
                valsFuncObjetivo.append(funObjAprima)
                if(funObjAprima < funcionObjABest):
                    Abest = copy.deepcopy(Aprima)
                    mejoresA.append(Abest)
                    funcionObjABest = funObjAprima
                    mejoresFunObj.append(funcionObjABest)
                t = t/(1+beta*t)
                valsTemperaturas.append(t)       
        iters = iters+1
        print("iteracion: {}".format(iters))
    end = time.time()
    tiempoConsumido = end-start
    Abest = Abest.tolist()
    aFOBest = [Abest,funcionObjABest]
    valsFOTemps = [valsTemperaturas,valsFuncObjetivo]
    resultado = [aFOBest,valsFOTemps,tempInicialFinal,tiempoConsumido]
    return resultado
