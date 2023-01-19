from Matriz import Matriz
import numpy as np
import PesosObjetivos as po





def funcion_fuera():
    x=0
    return x+1



# flowMatrix = np.array([[0,4,6,2,4,4],
#                        [4,0,4,2,2,8], 
#                        [6,4,0,2,2,6], 
#                        [2,2,2,0,6,2], 
#                        [4,2,2,6,0,10], 
#                        [4,8,6,2,10,0]])
# matrizFlujo = Matriz(
#     nombre="Matriz de flujo",
#     data=flowMatrix,
#     signoFOChar="+",
#     pesoObjetivo=0.2,
#     tipoMatriz='Flujo de Materiales',
#     isReindexMatriz=False)

# closenessRatingMatrix = np.array([[0,5,3,2,6,4],
#                                   [5,0,5,2,6,2],
#                                   [3,5,0,1,2,1],
#                                   [2,2,1,0,2,2],
#                                   [6,6,2,2,0,6],
#                                   [4,2,1,2,6,0]])
# matrizTasaCercania = Matriz(
#     nombre="Matriz Tasa de Cercanía",
#     data=closenessRatingMatrix,
#     signoFOChar="-",
#     pesoObjetivo=0.6,
#     tipoMatriz='Otra',
#     isReindexMatriz=True)


                        

# distanceMatrix = np.array([[0,1,2,1,2,3],
#                            [1,0,1,2,1,2],
#                            [2,1,0,3,2,1], 
#                            [1,2,3,0,1,2], 
#                            [2,1,2,1,0,1], 
#                            [3,2,1,2,1,0]])

# matrizDistancias = Matriz(
#     nombre="Matriz de distancias",
#     data=distanceMatrix,
#     signoFOChar="+",
#     pesoObjetivo=1,
#     tipoMatriz='Distancia',
#     isReindexMatriz=True)
    

# # matrizMovsPelig = Matriz(
# #     nombre="Matriz Movimientos Riesgosos",
# #     data=distanceMatrix,
# #     signoFOChar="-",
# #     pesoObjetivo=0.2,
# #     tipoMatriz='Otra',
# #     isReindexMatriz=True)

# # matrices = np.array([matrizDistancias,matrizTasaCercania,matrizFlujo,matrizMovsPelig])
# matrices = np.array([matrizDistancias,matrizTasaCercania,matrizFlujo])
# # ======================================================== #
# # ===================== BINARY CASES ===================== #
# # ======================================================== #
# #BinaryList = [MANUAL,GMWM,SDWM,CRITICM]
# metsObjWeights1 = [0,0,0,1] #uno CRITICM
# metsObjWeights2 = [0,0,1,0] #dos SDWM
# metsObjWeights3 = [0,0,1,1] #tres SDWM,CRITICM
# metsObjWeights4 = [0,1,0,0] #cuatro GMWM
# metsObjWeights5 = [0,1,0,1] #cinco GMWM,CRITICM
# metsObjWeights6 = [0,1,1,0] #seis GMWM,SDWM
# metsObjWeights7 = [0,1,1,1] #siete GMWM,SDWM,CRITICM
# metsObjWeights8 = [1,0,0,0] #ocho MANUAL
# metsObjWeights9 = [1,0,0,1] #nueve MANUAL,CRITICM
# metsObjWeights10 = [1,0,1,0] #diez MANUAL,SDWMs
# metsObjWeights11 = [1,0,1,1] #once MANUAL,SDWM,CRITICM
# metsObjWeights12 = [1,1,0,0] #doce MANUAL,GMWM
# metsObjWeights13 = [1,1,0,1] #trece MANUAL,GMWM,CRITICM
# metsObjWeights14 = [1,1,1,0] #catorce MANUAL,GMWM,SDWM 
# metsObjWeights15 = [1,1,1,1] #quince MANUAL,GMWM,SDWM,CRITICM





# casos = np.array([metsObjWeights1,metsObjWeights2,metsObjWeights3,metsObjWeights4,metsObjWeights5,metsObjWeights6,metsObjWeights7,metsObjWeights8,metsObjWeights9,metsObjWeights10,metsObjWeights11,metsObjWeights12,metsObjWeights13,metsObjWeights14,metsObjWeights15])







# pesosManuales1 = np.array([0.5,0.5])


# def binaryListToInt(binaryList):
#     """
#     Convierte una lista binaria en un entero

#     Parameters
#     ----------
#     binaryList: list
#         Lista de 4 posiciones binaria
     
#     Returns
#     -------
#     res   :  int
#         Valor entero de la lista
#     """
#     binList = np.copy(binaryList)
#     res = 0
#     for ele in binList: 
#         res = (res << 1) | ele
#     return res

# for caso in casos:
#     entero = binaryListToInt(caso)

#     print('=========================================')
#     print(f'Caso No: {entero}')
#     print('=========================================')

#     pesos = po.caseSelection(matrices,entero, pesosManuales1)
#     if pesos.get('MAN'):
#         weightsMAN = pesos.get('MAN')[1]
#         print(f'weightsMAN {weightsMAN}')
    
#     if pesos.get('SDWM'):
#         weightsSDWM = pesos.get('SDWM')[1]
#         print(f'weightsGMWM {weightsSDWM}')

#     if pesos.get('GMWM'):
#         weightsGMWM = pesos.get('GMWM')[1]
#         print(f'weightsSDWM {weightsGMWM}')

#     if pesos.get('CRITICM'):
#         weightsCRITICM = pesos.get('CRITICM')[1]
#         print(f'weightsCRITICM {weightsCRITICM}')
#     print('=========================================')
    
#     print("\n")

















# casos = [0,0,0,1] #uno CRITICM
# # casos = [0,0,1,0] #dos SDWM
# # casos = [0,0,1,1] #tres SDWM,CRITICM
# # casos = [0,1,0,0] #cuatro GMWM
# # casos = [0,1,0,1] #cinco GMWM,CRITICM
# # casos = [0,1,1,0] #seis GMWM,SDWM
# # casos = [0,1,1,1] #siete GMWM,SDWM,CRITICM
# # casos = [1,0,0,0] #ocho MANUAL
# # casos = [1,0,0,1] #nueve MANUAL,CRITICM
# # casos = [1,0,1,0] #diez MANUAL,SDWMs
# # casos = [1,0,1,1] #once MANUAL,SDWM,CRITICM
# # casos = [1,1,0,0] #doce MANUAL,GMWM
# # casos = [1,1,0,1] #trece MANUAL,GMWM,CRITICM
# # casos = [1,1,1,0] #catorce MANUAL,GMWM,SDWM 
# # casos = [1,1,1,1] #quince MANUAL,GMWM,SDWM,CRITICM
# # 

# #TODO: CODIGO PARA LOS CASOS, SIN UTILIZAR EL SWITCH

# if casos[0]:
#     print("CASO METODO MANUAL")
# if casos[1]:    
#     print("CASO METODO GMWM")    
# if casos[2]:
#     print("CASO METODO SDWM")
# if casos[3]:
#     print("CASO METODO CRITICM")
    

# def __numpy_to_string(A):
#     return A.tostring().hex()

# def __string_to_numpy(S):
#     return np.frombuffer(bytes.fromhex(S), dtype=np.float32)


# distanceMatrix = np.array([[0,1,2,1,2,3],
#                            [1,0,1,2,1,2],
#                            [2,1,0,3,2,1], 
#                            [1,2,3,0,1,2], 
#                            [2,1,2,1,0,1], 
#                            [3,2,1,2,1,0]])



# stringArray = __numpy_to_string(distanceMatrix)


# print(stringArray)

# arrayString = __string_to_numpy(stringArray)
# print("\n")

# print(arrayString)



# try:
#     import cPickle as pickle
# except:
#     import pickle
# import pprint

# # data1 = [ { 'a':'A', 'b':2, 'c':3.0 } ]
# print(f'BEFORE: {distanceMatrix}')

# data1_string = pickle.dumps(distanceMatrix)
# print(data1_string)

# data2 = pickle.loads(data1_string)
# print(f'AFTER: {data2}')
# print(f'AFTER: {type(data2)}')

# # print( f'SAME?: {data1 is data2}')
# # print( f'EQUAL?: {data1 == data2}')








# matrices = [matrix.data.tolist() for matrix in matrixes]
# for matrix in matrices:
#     print(matrix)
#     print("\n")
    
# def convertirMetUsadosString(metodosUsados):
#     """
#     Convierte la lista metodosUsados que es [0,0,0,0]
#     Con 1 donde si se utilice el método
#     el orden es [MAN,GMWM,SDWM,CRITICM]
#     """
#     metodosUsadosString = []
#     if metodosUsados[0]:
#         metodosUsadosString.append('Método Manual')
#     if metodosUsados[1]:
#         metodosUsadosString.append('Método de la Media Geométrica')
#     if metodosUsados[2]:
#         metodosUsadosString.append('Método de la Desviación Estándar')
#     if metodosUsados[3]:
#         metodosUsadosString.append('Método de Matriz de Correlaciones')
#     return metodosUsadosString
    
# metodosUsados = convertirMetUsadosString([,,1,1])
# for matrix in metodosUsados:
#     print(matrix)
#     print("\n")

# metodosUsados=[0,0,1,1]
# metodosUsadosString = convertirMetUsadosString(metodosUsados)

# # # #FIXME:MOSTRANDO LA INFO EN validar_sim.html
# nombresMatrices = [matrix.nombre for matrix in matrices]
# matricesRender = [matrix.data.tolist() for matrix in matrices]
# signosMatrices = [matrix.signoFOChar for matrix in matrices]
# tiposMatrices = [matrix.tipoMatriz for matrix in matrices]
# reindexesMatrices = ['Si' if matrix.isReindexMatriz else 'No' for matrix in matrices]
# valorPesosMatrices = [matrix.pesoObjetivo for matrix in matrices]

# # datos = np.column_stack((nombresMatrices,matricesRender))

# datos = list(zip(nombresMatrices,matricesRender,signosMatrices,tiposMatrices,reindexesMatrices,valorPesosMatrices))
# for dato in datos:
#     print(dato)    
# print(f'nombresMatrices.shape {nombresMatrices.shape}')
# print(f'matricesRender.shape {matricesRender.shape}')

# print(matricesRender)

# mostrarDatos = np.column_stack((nombresMatrices,matricesRender,signosMatrices,tiposMatrices,reindexesMatrices,valorPesosMatrices))

# print(datos)
# for ele in mostrarDatos:

#     print(ele)
# size = len(matricesRender)

# print(mostrarDatos[:])


# # lista1 = []
# listaMayor = []
# # for j in range(size):
# for i,val in enumerate(mostrarDatos):
#     print("\n")
#     #TODO:s SE INTENTA CONVERTIR PARA QUE SE GENERE LA LISTA DE OTRA FORMA
#     for j,dat in enumerate(val):
#         print(f'i: {i}')
#         print(f'j: {j}')
#         print(dat)
#         lista1.append(dat)
#        # print(val)

#     # print(val[0])
#     # lista1.append(val[0])
#     # val.pop(0)
#     # listaMayor.append(lista1)

#     # lista1.append(val[i])
    

# print(lista1)
# # print("\n")
# print("\n")

# for l in listaMayor:
#     print(l)
# # #     ##REDIRECCIONAR A 
# # table = [
# #     ['', 'Foo', 'Bar', 'Barf'],
#     ['Spam', 101, 102, 103],
#     ['Eggs', 201, 202, 203],
# ]
# print("\n")
# print("Table")
# print(table)



# lista = ['x']*10
# print(lista)













# matrices = np.array([matrizTasaCercania,amatrizDistancias,matrizFlujo,matrizMovsPelig])
# matrixes = np.array([matrizFlujo,matrizTasaCercania,matrizDistancias,matrizMovsPelig])
# matrices = np.array([matrizMovsPelig,matrizTasaCercania,matrizFlujo,matrizDistancias])

# matrices = np.array([matrizFlujo,matrizTasaCercania,matrizDistancias,matrizMovsPelig])
# matrices = np.array([matrizTasaCercania,matrizFlujo,matrizDistancias,matrizMovsPelig])
# matrices = np.array([matrizDistancias,matrizTasaCercania,matrizFlujo,matrizMovsPelig])
# matrices = np.array([matrizMovsPelig,matrizTasaCercania,matrizFlujo,matrizDistancias])

# print("=======================================")
# print("MATRICES ANTES DE ORDENAR")
# print("=======================================")

# for matrix in matrixes:
#     print(matrix.nombre)

# print("\n")
# print("\n")

# import copy
# def ordenarMatsDistFlujo(matrixes):
    
#     """
#     Coloca la matriz distancia en la posicion 0 y
#     la matriz de flujo en la posición 1
#     """
#     matrices = copy.deepcopy(matrixes)
#     #Revisa si hay matrices de flujo o distancia
#     isMatrizFlujoDist = [x.isMatrizFlujoDist for x in matrices] #Almacena los true o false
#     isMatrizFlujoDistarray = np.asarray(isMatrizFlujoDist)
#     hayMatrFlujoDist = isMatrizFlujoDistarray.any()
#     if hayMatrFlujoDist:
#         for i,matrix in enumerate(matrices):
#             if matrices[0].isMatrizDistance:
#                 break
#             else:
#                 if matrix.isMatrizDistance:
#                     temp = matrices[0]
#                     matrices[0] = matrix
#                     matrices[i] = temp

#         for i,matrix in enumerate(matrices):
#             if matrices[1].isMatrizFlujo:
#                 break
#             else:
#                 if matrix.isMatrizFlujo:
#                     temp = matrices[1]
#                     matrices[1] = matrix
#                     matrices[i] = temp
#     return matrices





# # print("\n")


# print("=======================================")
# print("MATRICES DESPUES DE ORDENAR")
# print("=======================================")

# matrices = ordenarMatsDistFlujo(matrixes)
# for matrix in matrices:
#     print(matrix.nombre)












# # for i,matrix in enumerate(matrices):
# #     if matrix.isMatrizDistance:
# #         print('Matriz Distancia posicion 0')
# #     else:
# #         if matrix.isMatrizDistance:
# #             input_seq[ix1], input_seq[ix2] = input_seq[ix2], input_seq[ix1]
# #             matrix, matrices[-1] = matrices[0], matrix
        


# #         if matrix.isMatrizFlujo:
# #             print('Matriz Flujo posicion 1')

# #         if matrix.isMatrizFlujo:
# #             matrix, matrices[-2] = matrices[0], matrices[index[0]]
    