import numpy as np
import random as random
import copy 
from itertools import combinations 
import base64
try:
    import cPickle as pickle
except:
    import pickle

def hayMatrizFlujoDist(matrices): 
    """
    Averigua si hay alguna matriz de flujo o de distancia en las matrices

    Return:
    hayMatrFlujoDist :True si  existe, False si no la hay
    matrizFlujoDist: la matriz de Flujo y la de distanciade todo el vector
    index: retorna la posicion donde está la matriz de flujo

    """
    isMatrizFlujoDistArray = [x.isMatrizFlujoDist for x in matrices] #Almacena los true o false
    isMatrizFlujoDistArray = np.asarray(isMatrizFlujoDistArray)
    matrizFlujoDist = [x for x in matrices if x.isMatrizFlujoDist ==True] #Almacena la matriz de flujo)
    hayMatrFlujoDist = isMatrizFlujoDistArray.any()
    index = [ i for i,x in enumerate(matrices) if x.isMatrizFlujoDist ==True] #Almacena el índice
    if(hayMatrFlujoDist):
        return hayMatrFlujoDist, matrizFlujoDist, index
    else:
        return hayMatrFlujoDist, 0, 0


def hayMatricesReindex(matrices): 
    """
    Averigua si hay alguna matriz que necesite ser reindexada de acuerdo 
    al nuevo vector

    Return:
    hayMatricesReindex :True si  existe, False si no la hay
    matricesReindex: las matrices que se necesitan reindexar
    index: retorna la posicion donde están las matrices que se necesitan reindexar

    """
    isReindexMatrizArray = [x.isReindexMatriz for x in matrices] #Almacena los true o false
    isReindexMatrizArray = np.asarray(isReindexMatrizArray)
    matricesReindex = [x for x in matrices if x.isReindexMatriz ==True] #Almacena la matriz de flujo)
    hayMatricesReindex = isReindexMatrizArray.any()
    index = [ i for i,x in enumerate(matrices) if x.isReindexMatriz ==True] #Almacena el índice
    
    if(hayMatricesReindex):
        return hayMatricesReindex, matricesReindex, index
    else:
        return hayMatricesReindex, 0, 0


def reindexMatrix(matrixReindex, a):
    """
    Obtiene la matriz reindexada de acuerdo al nuevo vector solucion

    Parameters:
    matrixReindex: matriz a reindexar
    a: Vector solución modificado

    """ 
    n = a.size#Tamaño del problema
    matrizVarsDecision = np.zeros((n,n)) #Matriz que va a tener las variables de decisión del vector sln
    matrizReindexed = np.zeros_like(matrizVarsDecision)#Matriz reindexada
    listaDistancias = [] #Lista que tiene las distancias a colocar en la matriz reindexada
    a = a-1
    # a =       [2,6,5,1,3,4]
    # a-1 =     [1,5,4,0,2,3] v del siguiente for
    #indexes =  [0,1,2,3,4,5] i del siguiente for
    #Vars Decision
    #           X10,X51,X42,X03,X24,X35

    for i,v in enumerate(a):#coloca 1 en la posicion v,i de las vars de decision
        matrizVarsDecision[v,i] = 1
    #Despues de colocar 1 en la matriz, obtengo las vars de decision
    #para obtenerlas de forma ordenada
    indexVarsDecision = np.argwhere(matrizVarsDecision > 0)
    #En indexVarsDecision me quedan los indices de las vars de decision
    #ordenados desde la fila 0 hacia abajo, en este ejemplo, quedan:
    #X03,X10,X24,X35,X42,X51
    indexes = indexVarsDecision[:,1] #Todos los elementos de la columna 1
    #En indexes quedan guardados los elementos que se combinan para 
    #obtener los indices de la matriz de distancia reindexada
    #Esto es [3,0,4,5,2,1]
    comb = combinations(indexes, 2) #combina cada dos indices, siempre debe ser 2, porque son una posicion
    combinaciones = list(comb) #combinaciones de los indices para la matriz reindexada
    combs = np.array(combinaciones)
    #Combs es [[3,0].[3,4],[3,5].[3,2],[3,1],[0,4],[0,5],...,[5,2],[5,1],[2,1]]
    # Cada elemento de combs es la posicion de la matriz de distancia que debo colocar en orden en la matriz
    #de distancias reindexada
    for _,v in enumerate(combs):
        #Se crea una lista de las distancias con los indices de las combinaciones
        j = v[0]
        l = v[1]
        listaDistancias.append(matrixReindex[j,l])
    #Se utiliza una mascara con los indicies de la triangular sup 
    #Luego se asigna la listaDistancias que se obtuvo para que quede
    #la nueva matriz de distancias reindexada
    mascaraIndicesTriangSup = np.triu_indices(n, 1) #mascara de la matriz triangular sup sin la diag
    matrizReindexed[mascaraIndicesTriangSup] = listaDistancias #Se asigna la lista de las distancias en la nueva matriz
    matrizReindexed = matrizReindexed + matrizReindexed.T - np.diag(np.diag(matrizReindexed))#Copia la triangular superior en la inferior
    return matrizReindexed

def castByteToBase64(numpyMatrix):
    """
    Convierte una matrix numpy al buen valor
    para almacenarla en el fampo dataNumpy que es un BinaryField
    """
    np_data_bytes = pickle.dumps(numpyMatrix)
    return base64.b64encode(np_data_bytes)

def funcionObjetivo(matrices,a,simetria):
    """
    Calcula el valor de la función objetivo
    Parameters:
    a: Vector solución modificado
    matrices: np array de matriz con todas las matrices
    IMPORTANTE: SIEMPRE LA MATRIZ DE DISTANCIAS DEBE ESTAR EN LA POSICIÓN 0
    LA MATRIZ DE FLUJO DEBE ESTAR EN LA POSICIÓN 1
    """ 
    n = matrices[0].getNumpyMatrix().shape[0]#TAMAÑO DEL PROBLEMA
    # A = [x for x in range(1,n+1)]#SOLUCION INICIAL, n+1, para que llegue hasta el final del tamaño
    matrixes = copy.deepcopy(matrices) 
    existeMatrizFlujo, matricesFlujoDist, indexMatricesFlujoDist = hayMatrizFlujoDist(matrixes)
    indexMatricesReindex = hayMatricesReindex(matrixes)[2]
    #Con el siguiente for se reindexan las matrices que se necesiten reindexar
    for i,ele in enumerate(matrixes):
        if(i in indexMatricesReindex): #si i está en los indíces haga reindex
            temporal = reindexMatrix(ele.getNumpyMatrix(),a) #coja la matriz de la posición i y hagale reindex
            temporalString =  '\n'.join(','.join('%0.3f' %x for x in y) for y in temporal)
            matrixes[i].data = temporalString
            matrixes[i].dataNumpy = castByteToBase64(temporal)#Conviertala en el buen valor para guardarla
            indexMatricesReindex.remove(i) #elimine ese elemento de los index, porque ya no lo necesita

       
    valorFuncObj = 0
    if(simetria):
        if(existeMatrizFlujo): 
            #Si existe matriz de flujo
            #  se debe multiplicar matrizFlujo*matrizDistancias*signo*peso
            
            matricesFlujoDistCopy = copy.deepcopy(matricesFlujoDist)#hace una copia sin afectar el original
            #Datos de matriz de distancias
            matrizDistanciasReArray = matricesFlujoDistCopy[0].getNumpyMatrix()
            upperElsMatrizData = matrizDistanciasReArray[np.triu_indices(n,1)]#obtiene los elementos de la triangular superior en una lista, 

            signoMatrizDistancias = matricesFlujoDistCopy[0].signoFO
            pesoMatrizDistancias = matricesFlujoDistCopy[0].pesoObjetivo
            #Datos de matriz de flujo
            signoMatrizFlujo = matricesFlujoDistCopy[1].signoFO
            pesoMatrizFlujo = matricesFlujoDistCopy[1].pesoObjetivo
            matrizFlujo = matricesFlujoDistCopy[1].getNumpyMatrix()
            upperElsMatrizFlujo = matrizFlujo[np.triu_indices(n,1)]#obtiene los elementos de la triangular superior en una lista, 
            multipDistFlujo = (upperElsMatrizData*signoMatrizDistancias*pesoMatrizDistancias)*(signoMatrizFlujo*pesoMatrizFlujo*upperElsMatrizFlujo)
            valorFuncObj = sum(multipDistFlujo)
            #Se quitan las matrices de flujo y distancia, para poder calcular el aporte de la FO de las otras matrices
            restoMatrices = np.delete(matrixes,indexMatricesFlujoDist)
            if np.size(restoMatrices):
                #Si quedan matrices, haga el calculo para el resto 
                matrizObjFuncNoFlujo = 1
                for matrix in restoMatrices:
                    #Calcule la multiplicación del resto de matrices
                    matrizData = matrix.getNumpyMatrix()
                    upperElsMatrizData = matrizData[np.triu_indices(n,1)]#obtiene los elementos de la triangular superior en una lista, 

                    matrizPesoObjetivo = matrix.pesoObjetivo
                    matrizSignoFO = matrix.signoFO
                    matrizObjFuncNoFlujo = matrizObjFuncNoFlujo*(upperElsMatrizData*matrizPesoObjetivo*matrizSignoFO)
                valorFuncObj = valorFuncObj+sum(matrizObjFuncNoFlujo)
                return valorFuncObj
            else:
                #si no quedan matrices, sólo existen matriz de flujo y de distancias
                return valorFuncObj
        else:
            valorFuncObj = 0
            for matrix in matrixes:
                #Calcule la multiplicación de arribaS
                matrixx = matrix.getNumpyMatrix()
                upperElsMatrixx = matrixx[np.triu_indices(n,1)]#obtiene los elementos de la triangular superior en una lista, 
                valorFuncObj = valorFuncObj+sum(sum((upperElsMatrixx*matrix.pesoObjetivo*matrix.signoFO)))
            return valorFuncObj
    else:
        if(existeMatrizFlujo): 
            #Si existe matriz de flujo
            #  se debe multiplicar matrizFlujo*matrizDistancias*signo*peso
    
            matricesFlujoDistCopy = copy.deepcopy(matricesFlujoDist)#hace una copia sin afectar el original
            #Datos de matriz de distancias
            matrizDistanciasReArray = matricesFlujoDistCopy[0].getNumpyMatrix()
    
            signoMatrizDistancias = matricesFlujoDistCopy[0].signoFO
            pesoMatrizDistancias = matricesFlujoDistCopy[0].pesoObjetivo
            #Datos de matriz de flujo
            signoMatrizFlujo = matricesFlujoDistCopy[1].signoFO
            pesoMatrizFlujo = matricesFlujoDistCopy[1].pesoObjetivo
            matrizFlujo = matricesFlujoDistCopy[1].getNumpyMatrix()
            multipDistFlujo = (matrizDistanciasReArray*signoMatrizDistancias*pesoMatrizDistancias)*(signoMatrizFlujo*pesoMatrizFlujo*matrizFlujo)
            valorFuncObj = sum(multipDistFlujo)
            #Se quitan las matrices de flujo y distancia, para poder calcular el aporte de la FO de las otras matrices
            restoMatrices = np.delete(matrixes,indexMatricesFlujoDist)
            if np.size(restoMatrices):
                #Si quedan matrices, haga el calculo para el resto 
                matrizObjFuncNoFlujo = 1
                for matrix in restoMatrices:
                    #Calcule la multiplicación del resto de matrices
                    matrizData = matrix.getNumpyMatrix()

                    matrizPesoObjetivo = matrix.pesoObjetivo
                    matrizSignoFO = matrix.signoFO
                    matrizObjFuncNoFlujo = matrizObjFuncNoFlujo*(matrizData*matrizPesoObjetivo*matrizSignoFO)
                valorFuncObj = valorFuncObj+sum(matrizObjFuncNoFlujo)
                return np.sum(valorFuncObj)
            else:
                #si no quedan matrices, sólo existen matriz de flujo y de distancias
                return np.sum(valorFuncObj)
        else:
            valorFuncObj = 0
            for matrix in matrixes:
                #Calcule la multiplicación de arribaS
                matrixx = matrix.getNumpyMatrix()
                # upperElsMatrixx = matrixx[np.triu_indices(n,1)]#obtiene los elementos de la triangular superior en una lista, 
                valorFuncObj = valorFuncObj+sum(sum((matrixx*matrix.pesoObjetivo*matrix.signoFO)))
            return np.sum(valorFuncObj)