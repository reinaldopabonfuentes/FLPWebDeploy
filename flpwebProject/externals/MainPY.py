from matplotlib import pyplot as plt
import numpy as np

import json
# ~~~~~~~ PYTHON INTERACTIVE IMPORTS ~~~~~~ #
# import project.src.NormalMethods as nm 
# from project.src.Matriz import Matriz


# ~~~~~~~ PYTHON TERMINAL IMPORTS ~~~~~~ #
import NormalMethods as nm 
from Matriz import Matriz
import FuncionObjetivo as fo
# # 
# 



# # -------- PRECISION EN np -------- #
np.set_printoptions(precision=4)#cantidad de decimales en las matrices de float



distanceMatrix = np.array([[0,1,2,3,1,2,3,4],
                           [1,0,1,2,2,1,2,3],
                           [2,1,0,1,3,2,1,2], 
                           [3,2,1,0,4,3,2,1], 
                           [1,2,3,4,0,1,2,3], 
                           [2,1,2,3,1,0,1,2], 
                           [3,2,1,2,2,1,0,1], 
                           [4,3,2,1,3,2,1,0]])
matrizDistancias = Matriz(
    nombre="Matriz de distancias",
    data=distanceMatrix,
    isMatrizFlujoDist=True,
    signoFOChar="+",
    isReindexMatriz =True,
    pesoObjetivo=1.0,
    tipoMatriz = 'Distancia',

    isMatrizDistance =True,
    isMatrizFlujo=False)

flowMatrix = np.array([[0,6,1,1,8,2,4,4],
                       [6,0,1,2,3,3,6,2], 
                       [1,1,0,5,2,3,1,10], 
                       [1,2,5,0,2,8,3,3], 
                       [8,3,2,2,0,4,10,10], 
                       [2,3,3,8,4,0,8,8], 
                       [4,6,1,3,10,8,0,2], 
                       [4,2,10,3,10,8,2,0]])

matrizFlujo = Matriz(
    nombre="Matriz de flujo",
    data=flowMatrix,
    isMatrizFlujoDist=True,
    signoFOChar="+",
    isReindexMatriz =False,
    pesoObjetivo=1.0,
    tipoMatriz = 'Flujo de Materiales',

    isMatrizDistance =False,
    isMatrizFlujo=True,)

closenessRatingMatrix = np.array([[0,6,5,5,6,4,5,2],
                                  [6,0,3,5,3,2,6,2],
                                  [5,3,0,6,3,1,2,2],
                                  [5,5,6,0,2,2,3,1],
                                  [6,3,3,2,0,5,6,6],
                                  [4,2,1,2,5,0,6,6],
                                  [5,6,2,3,6,6,0,4],
                                  [2,2,2,1,6,6,4,0]])
matrizTasaCercania = Matriz(
    nombre="Matriz de tasa de cercanía",
    data=closenessRatingMatrix,
    isMatrizFlujoDist=False,
    signoFOChar="-",
    isReindexMatriz =False,
    pesoObjetivo=1.0,
    tipoMatriz = 'Otra',

    isMatrizDistance =False,
    isMatrizFlujo=False,)


simetria=True
a = np.array([[3, 8, 5, 1, 4, 6, 7, 2]])
matrices = np.array([matrizDistancias,matrizFlujo,matrizTasaCercania])


for matriz in matrices:
    print(matriz)

funcionObjetivo = fo.funcionObjetivo(matrices,a,simetria)
print(f'Valor funcion Objetivo {funcionObjetivo}')
###########################################################################
################################ MAIN CODE ################################
###########################################################################

# ~~~~~~~~~~~~ 1. OBTENER MATRICES ~~~~~~~~~~~ #
# # -------- MATRICES -------- #
##########################################################################
################### INSTANCIA PEQUEÑA 6X6 2 OBJETIVOS ####################
##########################################################################


# flowMatrix = np.array([[0,4,6,2,4,4],
#                        [4,0,4,2,2,8], 
#                        [6,4,0,2,2,6], 
#                        [2,2,2,0,6,2], 
#                        [4,2,2,6,0,10], 
#                        [4,8,6,2,10,0]])
# matrizFlujo = Matriz("Matriz de flujo", flowMatrix, True, "+",False)

# closenessRatingMatrix = np.array([[0,5,3,2,6,4],
#                                   [5,0,5,2,6,2],
#                                   [3,5,0,1,2,1],
#                                   [2,2,1,0,2,2],
#                                   [6,6,2,2,0,6],
#                                   [4,2,1,2,6,0]])
# matrizTasaCercania = Matriz("Matriz de tasa de cercanía", closenessRatingMatrix, 
#                             False,"-",False)

# distanceMatrix = np.array([[0,1,2,1,2,3],
#                            [1,0,1,2,1,2],
#                            [2,1,0,3,2,1], 
#                            [1,2,3,0,1,2], 
#                            [2,1,2,1,0,1], 
#                            [3,2,1,2,1,0]])
# matrizDistancias = Matriz("Matriz de distancias", distanceMatrix, True,"+",True,1.0,True)

# matrices = np.array([matrizDistancias,matrizFlujo,matrizTasaCercania])


###########################################################################
#################### INSTANCIA MEDIANA 8X8 4 OBJETIVOS ####################
###########################################################################


# flowMatrix = np.array([[0,6,1,1,8,2,4,4],
#                        [6,0,1,2,3,3,6,2], 
#                        [1,1,0,5,2,3,1,10], 
#                        [1,2,5,0,2,8,3,3], 
#                        [8,3,2,2,0,4,10,10], 
#                        [2,3,3,8,4,0,8,8], 
#                        [4,6,1,3,10,8,0,2], 
#                        [4,2,10,3,10,8,2,0]])
# matrizFlujo = Matriz("Matriz de flujo", flowMatrix, True, "+",False)

# closenessRatingMatrix = np.array([[0,6,5,5,6,4,5,2],
#                                   [6,0,3,5,3,2,6,2],
#                                   [5,3,0,6,3,1,2,2],
#                                   [5,5,6,0,2,2,3,1],
#                                   [6,3,3,2,0,5,6,6],
#                                   [4,2,1,2,5,0,6,6],
#                                   [5,6,2,3,6,6,0,4],
#                                   [2,2,2,1,6,6,4,0]])
# matrizTasaCercania = Matriz("Matriz de tasa de cercanía", closenessRatingMatrix, 
#                             False,"-",False)#

# materialHandling = np.array([[0,1.5,0.5,1.4,1.5,0.5,1,0.6],
#                              [1.5,0,1.5,1.6,1.5,1,2,1.8],
#                              [0.5,1.5,0,2,0.7,3,1.5,1.6],
#                              [1.4,1.6,2,0,2.2,1,0.3,2],
#                              [1.5,1.5,0.7,2.2,0,1.5,2,0.8],
#                              [0.5,1,3,1,1.5,0,1.4,2.2],
#                              [1,2,1.5,0.3,2,1.4,0,2.5],
#                              [0.6,1.8,1.6,2,0.8,2.2,2.5,0]])
# matrizTiempoManejMaters = Matriz("Matriz de tiempo de manejo de materiales", materialHandling, 
#                             False,"+",True)#

# hazardousMovement = np.array([[0,4,0,0,4,0,0,0],
#                               [4,0,1,0,0,0,4,2],
#                               [0,1,0,0,0,3,0,3],
#                               [0,0,0,0,3,6,2,0],
#                               [4,0,0,3,0,0,0,5],
#                               [0,0,3,6,0,0,2,0],
#                               [0,4,0,2,0,2,0,2],
#                               [0,2,3,0,5,0,2,0]])


# matrizMovsPeligros = Matriz("Matriz de movimientos peligrosos", hazardousMovement, 
#                             False,"+",False)

# distanceMatrix = np.array([[0,1,2,3,1,2,3,4],
#                            [1,0,1,2,2,1,2,3],
#                            [2,1,0,1,3,2,1,2], 
#                            [3,2,1,0,4,3,2,1], 
#                            [1,2,3,4,0,1,2,3], 
#                            [2,1,2,3,1,0,1,2], 
#                            [3,2,1,2,2,1,0,1], 
#                            [4,3,2,1,3,2,1,0]])
# matrizDistancias = Matriz("Matriz de distancias", distanceMatrix, True,"+",True,1.0,True)


# matrices = np.array([matrizDistancias,matrizFlujo,matrizTasaCercania,matrizTiempoManejMaters,matrizMovsPeligros])


# # ###########################################################################
# # # ################## INSTANCIA MEDIANA 15x15 DOS OBJETIVOS ##################
# # # # ###########################################################################

# # flowMatrix = np.array([[0,4,5,8,12,16,3,7,2,6,8,9,12,17,12],
# #                        [15,0,6,8,12,0,9,35,4,7,3,6,9,8,12], 
# #                        [15,16,0,9,2,0,15,6,17,6,12,3,5,8,9], 
# #                        [1,25,9,0,2,6,5,8,0,0,0,0,3,2,9], 
# #                        [5,0,15,6,0,2,0,8,0,9,0,6,6,3,2], 
# #                        [8,5,0,6,9,0,5,8,8,0,6,0,3,5,8], 
# #                        [0,3,5,0,8,9,0,9,9,8,7,12,0,13,15], 
# #                        [16,17,0,16,15,11,14,0,1,4,12,2,15,15,13], 
# #                        [17,6,9,11,25,6,12,12,0,5,7,8,9,2,6], 
# #                        [3,8,9,6,0,0,0,0,0,0,0,5,6,0,7], 
# #                        [8,9,0,12,15,16,0,0,2,4,0,5,0,5,7], 
# #                        [6,7,2,8,9,12,15,5,5,0,0,0,7,0,5], 
# #                        [6,4,3,8,9,0,11,5,15,15,10,10,0,5,10], 
# #                        [12,6,9,8,10,11,15,5,16,12,10,10,5,0,7], 
# #                        [2,3,4,8,0,12,15,16,12,0,0,0,0,2,0]])

# # closenessRatingMatrix = np.array([[0,2,0,3,0,-1,2,0,3,1,4,-1,2,2,0],
# #                                  [2,0,3,1,2,3,2,4,0,3,0,1,1,0,1], 
# #                                  [0,3,0,0,3,1,0,2,-1,0,4,0,2,1,0], 
# #                                  [3,1,0,0,-1,0,1,0,4,4,0,1,2,0,2], 
# #                                  [0,2,3,-1,0,0,1,3,0,2,1,0,1,0,0], 
# #                                  [-1,3,1,0,0,0,2,0,0,3,0,1,3,3,0], 
# #                                  [2,2,0,1,1,2,0,0,0,0,-1,2,1,0,1], 
# #                                  [0,4,2,0,3,0,0,0,1,4,3,2,3,3,2], 
# #                                  [3,0,-1,4,0,0,0,1,0,3,0,2,1,0,3], 
# #                                  [1,3,0,4,2,3,0,4,3,0,1,0,1,0,1], 
# #                                  [4,0,4,0,1,0,-1,3,0,1,0,3,2,1,1], 
# #                                  [-1,1,0,1,0,1,2,2,2,0,3,0,-1,1,1], 
# #                                  [2,1,2,2,1,3,1,3,1,1,2,-1,0,0,1], 
# #                                  [2,0,1,0,0,3,0,3,0,0,1,1,0,0,0], 
# #                                  [0,1,0,2,0,0,1,2,3,1,1,1,1,0,0]])


# # distanceMatrix = np.array([[0,1,2,3,4,1,2,3,4,5,2,3,4,5,6],
# #                            [1,0,1,2,3,2,1,2,3,4,3,2,3,4,5], 
# #                            [2,1,0,1,2,3,2,1,2,3,4,3,2,3,4], 
# #                            [3,2,1,0,1,4,3,2,1,2,5,4,3,2,3], 
# #                            [4,3,2,1,0,5,4,3,2,1,6,5,4,3,2], 
# #                            [1,2,3,4,5,0,1,2,3,4,1,2,3,4,5], 
# #                            [2,1,2,3,4,1,0,1,2,3,2,1,2,3,4], 
# #                            [3,2,1,2,3,2,1,0,1,2,3,2,1,2,3], 
# #                            [4,3,2,1,2,3,2,1,0,1,4,3,2,1,2], 
# #                            [5,4,3,2,1,4,3,2,1,0,5,4,3,2,1], 
# #                            [2,3,4,5,6,1,2,3,4,5,0,1,2,3,4], 
# #                            [3,2,3,4,5,2,1,2,3,4,1,0,1,2,3], 
# #                            [4,3,2,3,4,3,2,1,2,3,2,1,0,1,2], 
# #                            [5,4,3,2,3,4,3,2,1,2,3,2,1,0,1], 
# #                            [6,5,4,3,2,5,4,3,2,1,4,3,2,1,0]])

# # 
# # 
# # 

# # matrizFlujo = Matriz("Matriz de flujo", flowMatrix, True, "+",False)
# # matrizTasaCercania = Matriz("Matriz de tasa de cercanía", closenessRatingMatrix, 
# #                             False,"-",False)
# # matrizDistancias = Matriz("Matriz de distancias", distanceMatrix, True,"+",True,1,isMatrixDistance=True)
# # matrices = np.array([matrizDistancias,matrizFlujo,matrizTasaCercania])


# # ======================================================== #
# # ===================== BINARY CASES ===================== #
# # ======================================================== #
# #BinaryList = [MANUAL,GMWM,SDWM,CRITICM]
# # metsObjWeights1 = [0,0,0,1] #uno CRITICM
# # metsObjWeights2 = [0,0,1,0] #dos SDWM
# # metsObjWeights3 = [0,0,1,1] #tres SDWM,CRITICM
# # metsObjWeights4 = [0,1,0,0] #cuatro GMWM
# # metsObjWeights5 = [0,1,0,1] #cinco GMWM,CRITICM
# # metsObjWeights6 = [0,1,1,0] #seis GMWM,SDWM
# # metsObjWeights7 = [0,1,1,1] #siete GMWM,SDWM,CRITICM
# # metsObjWeights8 = [1,0,0,0] #ocho MANUAL
# # metsObjWeights9 = [1,0,0,1] #nueve MANUAL,CRITICM
# # metsObjWeights10 = [1,0,1,0] #diez MANUAL,SDWM
# # metsObjWeights11 = [1,0,1,1] #once MANUAL,SDWM,CRITICM
# # metsObjWeights12 = [1,1,0,0] #doce MANUAL,GMWM
# # metsObjWeights13 = [1,1,0,1] #trece MANUAL,GMWM,CRITICM
# # metsObjWeights14 = [1,1,1,0] #catorce MANUAL,GMWM,SDWM 
# metsObjWeights15 = [1,1,1,1] #quince MANUAL,GMWM,SDWM,CRITICM




# # pesosManuales1 = np.array([0.5,0.5])
# pesosManuales2 = np.array([0.25,0.25,0.25,0.25])
# # pesosManuales3 = np.array([0.5,0.5])
# entero = nm.binaryListToInt(metsObjWeights15)


# lambda1 = 0.5
# lambda2 = 0.05 
# # lambdas = np.array([0.5,0.05])
# # Q = 50 #NUMERO DE ITERACIONES
# Q = 1 #NUMERO DE ITERACIONES

# # resultados = nm.caseSelection(matrices,entero,pesosManuales1)
# resultados = nm.caseSelection(matrices,entero,pesosManuales2)
# # resultados = nm.caseSelection(lambda1,lambda2,Q,matrices,entero,pesosManuales3)



# with open("data_file.json", "w") as write_file:
#     json.dump(resultados, write_file)

# # print(resultados)


# if(resultados[0][0]):
#     aFOBest = resultados[0][0]
#     valsFOTemps= resultados[0][1]
#     tempInicialFinal = resultados[0][2]
#     print("Mejor solución Abest MANUAL: {} \n".format(aFOBest[0]))
#     # f.write("Mejor solución Abest MANUAL: %d\r\n" % aFOBest[0])
#     print("Mejor funcion objetivo MANUAL {} \n".format(aFOBest[1]))
#     # f.write("Mejor funcion objetivo MANUAL {} \n".format(aFOBest[1]))
#     plt.plot(valsFOTemps[0],valsFOTemps[1])
#     plt.title("Funcion Objetivo vs. Temp. MANUAL", fontsize=20,fontweight='bold')
#     plt.xlabel("Temp.", fontsize=18,fontweight='bold')
#     plt.ylabel("Cost", fontsize=18,fontweight='bold')
#     plt.xlim(tempInicialFinal[0]+2,tempInicialFinal[1]-1)
#     plt.savefig("resultados Manual.png")
#     plt.show()


# if(resultados[1][0]):
#     aFOBest = resultados[1][0]
#     valsFOTemps= resultados[1][1]
#     tempInicialFinal = resultados[1][2]
#     print("Mejor solución Abest GM: {} \n".format(aFOBest[0]))
#     print("Mejor funcion objetivo GM {} \n".format(aFOBest[1]))
#     plt.plot(valsFOTemps[0],valsFOTemps[1])
#     plt.title("Funcion Objetivo vs. Temp. GM", fontsize=20,fontweight='bold')
#     plt.xlabel("Temp.", fontsize=18,fontweight='bold')
#     plt.ylabel("Cost", fontsize=18,fontweight='bold')
#     plt.xlim(tempInicialFinal[0]+2,tempInicialFinal[1]-1)
#     plt.savefig("resultados GMWM.png")
#     plt.show()
# else:
#     print("No se puede utilizar GMWM")
#     print("resultads[1] {}".format(resultados[1]))
#     print("\n")

# if(resultados[2][0]):
#     aFOBest = resultados[2][0]
#     valsFOTemps= resultados[2][1]
#     tempInicialFinal = resultados[2][2]
#     print("Mejor solución Abest SDWM: {} \n".format(aFOBest[0]))
#     print("Mejor funcion objetivo SDWM {} \n".format(aFOBest[1]))
#     plt.plot(valsFOTemps[0],valsFOTemps[1])
#     plt.title("Funcion Objetivo vs. Temp. SDWM", fontsize=20,fontweight='bold')
#     plt.xlabel("Temp.", fontsize=18,fontweight='bold')
#     plt.ylabel("Cost", fontsize=18,fontweight='bold')
#     plt.xlim(tempInicialFinal[0]+2,tempInicialFinal[1]-1)
#     plt.savefig("resultados SDWM.png")
#     plt.show()


# if(resultados[3][0]):
#     aFOBest = resultados[3][0]
#     valsFOTemps= resultados[3][1]
#     tempInicialFinal = resultados[3][2]
#     print("Mejor solución Abest CRITICM: {} \n".format(aFOBest[0]))
#     print("Mejor funcion objetivo CRITICM {} \n".format(aFOBest[1]))
#     plt.plot(valsFOTemps[0],valsFOTemps[1])
#     plt.title("Funcion Objetivo vs. Temp. CRITICM", fontsize=20,fontweight='bold')
#     plt.xlabel("Temp.", fontsize=18,fontweight='bold')
#     plt.ylabel("Cost", fontsize=18,fontweight='bold')
#     plt.xlim(tempInicialFinal[0]+2,tempInicialFinal[1]-1)
#     plt.savefig("resultados CRITICM.png")
#     plt.show()



