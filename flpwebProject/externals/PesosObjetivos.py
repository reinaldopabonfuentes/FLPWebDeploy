import numpy as np 
import copy 



# ~~~~~~~ PYTHON TERMINAL IMPORTS ~~~~~~ #
import flpwebProject.externals.NormalMethods as nm
# import NormalMethods as nm

    
def objWeights(criticalValues):
    """

    Calcula los pesos ponderados de la lista que se pasa como parametro
    Ya sea los Gt, SDt o Ct

    Inputs:
    criticalValues : np array que puede ser los Gt, SDt o Ct

    Outputs:
    Pesos ponderados
    """
    criticalVals=np.copy(criticalValues)
    if criticalVals[0] == 0:
        return 0
    else:
        return np.asarray([x/np.sum(criticalVals) for x in criticalVals])

def binaryListToInt(binaryList):
    """
    Convierte una lista binaria en un entero

    Parameters
    ----------
    binaryList: list
        Lista de 4 posiciones binaria
     
    Returns
    -------
    res   :  int
        Valor entero de la lista
    """
    binList = np.copy(binaryList)
    res = 0
    for ele in binList: 
        res = (res << 1) | ele
    return res

def validarPesosManuales(matrices,pesosManuales):
    """
    Revisa y asigna los buenos valores de pesosManuales
    Si los pesosManuales tienen la misma cantidad de elementos como tantas matrices hay
    Parameters
    matrices: las matrices objetivo a trabajar
    pesosManuales: los pesos objetivos que se ingresan manualmente
    """
    matrixes = np.copy(matrices)
    # matrixes = [x.data for x in matrixes]
    matricesSize = matrixes.shape[0]
    pesosManualesSize = pesosManuales.shape[0]
    MAN = []
    if pesosManuales.size == 0:
        MAN =0
    else:
        if(matricesSize==pesosManualesSize):
            MAN=pesosManuales
        else:
            print("No existen la cantidad de pesos objetivos como matrices hay")
            MAN = ["ERROR"]*matricesSize
    return MAN

def poblarMatsPO(valsCrit,matrixesSA,manual=False):
    """
    Se encarga de llenar la matriz que va a ir al SA
    con los pesos que se calculan o se pasan
    En el caso que sea manual, se pasa como valsCrit
    Los pesos manuales que se introdujeron
    Parameters:
    valsCrit: numpy array 
        Tiene los valores criticos para calcular los pesos

    matrixesSA: numpy array
        Tiene las matrices que necesitan que sean llenadas con
        los pesos objetivos, aquí viene la matriz Distancia
        en la posición 0
    
    man: bool
        Si se va a poblar con pesos manuales o no
    """
    if manual:
        pesos = valsCrit
    else:
        pesos = objWeights(valsCrit)
    pesos = np.insert(pesos,0,1,axis=0)#Se adiciona el peso de la Matriz Distancia
    for i,matriz in enumerate(matrixesSA):
        #Aqui se coloca el peso a las matrices que van a SA
        if not(matriz.isMatrizDistance):
            matriz.pesoObjetivo = pesos[i]  
    return matrixesSA,pesos





def calcularSymMatricesNormal(matrices, gmwm=False):
    """
    Esta función acorta la cantidad de código en los casos,
    debido a que era necesario hacer lo mismo con las matricesOW,
    matricesNoDist y matricesNoDistData para obtener
    symetria, normalMatricesSym y normalMatricesAsym
    
    Parametros:
    matrices: numpy array 
        Contiene todas las matrices 
    gmwm: bool
        True si en el caso utiliza el método gmwm

    return:
    symetria: Bool
        True si las matrices son simétricas
    normalMatricesSym: numpy array
        Devuelve las matrices normalizadas simétricas,
        sin contener en la posición 0, la matriz de distancias
    normalMatricesAsym: numpy array
        Devuelve las matrices normalizadas asimétricas,
        sin contener en la posición 0, la matriz de distancias
    cerosToda: bool
        True si hay por lo menos una matriz que tenga un 0 en una posición
        diferente a la diagonal
    """
    matricesOW = copy.deepcopy(matrices)#copia matrices para el calculo de los pesos objetivo (no incluye matriz distancias)
    matricesNoDist = [x for x in matricesOW if not(x.isMatrizDistance)]#obtiene solo las matrices objetivo
    matricesNoDistData = [x.getNumpyMatrix() for x in matricesNoDist ]#obtiene solo la data de las matrices objetivo
    symetria= nm.areSym(matricesNoDistData)[0] #Revisa si todas las matrices son Simetricas
    normalMatricesSym = nm.normalMatrixesSym(matricesNoDistData)#Normaliza las matrices simétricas
    normalMatricesAsym = nm.normalMatrixesAsym(matricesNoDistData)
    if gmwm:
        cerosTodas = nm.hayCeros(matricesNoDist)[0] #Revisa si hay ceros en las matrices
        return symetria, normalMatricesSym, normalMatricesAsym, cerosTodas
    else:
        return symetria, normalMatricesSym, normalMatricesAsym



def uno(matrices,pesosManuales):
    # --------- CASO 1 --------- #
    # --------- CRITICM -------- #
    symetria, normalMatricesSym, normalMatricesAsym = calcularSymMatricesNormal(matrices)
    SD = [] #Lista de SDi
    CRITICM = [] #Lista de Ci
    WCRITICM = []
    matrixesSACRITICM = copy.deepcopy(matrices)
    if symetria:
        # ------- SYMETRICAS ------- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
        CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
        matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
    else:
        # ------ NO SYMETRICAS ----- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
        CRITICM = nm.criticm(symetria,SD,normalMatricesAsym) 
        matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
    
    resultados = {
        'symetria'  :   symetria,
        'CRITICM'   :   [matrixesSACRITICM, WCRITICM]
    }
    return resultados 


def dos(matrices,pesosManuales):
    # --------- CASO 2 --------- #
    # ---------- SDWM ---------- #
    symetria, normalMatricesSym, normalMatricesAsym = calcularSymMatricesNormal(matrices)
    SD = [] #Lista de SDi
    WSD = []
    matrixesSASD = copy.deepcopy(matrices)
    if symetria:
        # ------- SYMETRICAS ------- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
        matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)
    else:
        # ------ NO SYMETRICAS ----- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
        matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)
    resultados = {
        'symetria'  :   symetria,
        'SDWM'      :   [matrixesSASD, WSD],
        }
    return resultados 

def tres(matrices,pesosManuales):
    # --------- CASO 3 --------- #
    # ------ SDWM,CRITICM ------ #
    symetria, normalMatricesSym, normalMatricesAsym = calcularSymMatricesNormal(matrices)
    SD = [] #Lista de SDi
    WSD = []
    CRITICM = [] #Lista de Ci
    WCRITICM = []
    matrixesSASD = copy.deepcopy(matrices)
    matrixesSACRITICM = copy.deepcopy(matrices)

    if symetria:
        # ------- SYMETRICAS ------- #
        #Se tiene que crear copias de matrices para cada método de computo de objetivo
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
        matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

        CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
        matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
    else:
        # ------ NO SYMETRICAS ----- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
        matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)
  
        CRITICM = nm.criticm(symetria,SD,normalMatricesAsym)
        matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

    resultados = {
        'symetria'  :   symetria,
        'SDWM'      :   [matrixesSASD, WSD],
        'CRITICM'   :   [matrixesSACRITICM, WCRITICM],
    }
    return resultados 

def cuatro(matrices,pesosManuales):
    # --------- CASO 4 --------- #
    # ---------- GMWM ---------- #
    symetria, normalMatricesSym, normalMatricesAsym, cerosTodas = calcularSymMatricesNormal(matrices,True)
    GM = [] #Lista de Gi
    WGM= []
    
    matrixesSAGM = copy.deepcopy(matrices)

    if symetria:
        # ------- SYMETRICAS ------- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0
        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesSym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)
    else:
        # ------ NO SYMETRICAS ----- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0
        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesAsym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)
    
    resultados = {
        'symetria'  :   symetria,
        'GMWM'      :   [matrixesSAGM, WGM],
    }
    return resultados 

def cinco(matrices,pesosManuales):
    # --------- CASO 5 --------- #
    # ------ GMWM,CRITICM ------ #
    symetria, normalMatricesSym, normalMatricesAsym, cerosTodas = calcularSymMatricesNormal(matrices,True)
    GM = [] #Lista de Gi
    WGM= []
    SD = [] #Lista de SDi
    WSD = []
    CRITICM = [] #Lista de Ci
    WCRITICM = []
    matrixesSAGM = copy.deepcopy(matrices)
    matrixesSACRITICM = copy.deepcopy(matrices)

    if symetria:
        # ------- SYMETRICAS ------- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesSym)   
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

            
    else:
        # ------ NO SYMETRICAS ----- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0


            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

            

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesAsym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)
           

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            CRITICM = nm.criticm(symetria,SD,normalMatricesAsym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
    
    resultados = {
        'symetria'  :   symetria,
        'GMWM'      :   [matrixesSAGM, WGM],
        'CRITICM'   :   [matrixesSACRITICM, WCRITICM]
    }
    return resultados    



def seis(matrices,pesosManuales):
    #  # --------- CASO 6 --------- #  #
    # -------- GMWM,SDWM ------- #
    symetria, normalMatricesSym, normalMatricesAsym, cerosTodas = calcularSymMatricesNormal(matrices,True)
    GM = [] #Lista de Gi
    WGM= []
    SD = [] #Lista de SDi
    WSD = []
    matrixesSAGM = copy.deepcopy(matrices)
    matrixesSASD = copy.deepcopy(matrices)

    if symetria:
        # ------- SYMETRICAS ------- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesSym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

    else:
        # ------ NO SYMETRICAS ----- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesAsym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

    resultados = {
        'symetria'  :   symetria,
        'GMWM'      :   [matrixesSAGM, WGM],
        'SDWM'      :   [matrixesSASD, WSD],

    }

    return resultados    


def siete(matrices,pesosManuales):
    # --------- CASO 7 --------- # 
    # ---- GMWM,SDWM,CRITICM --- #
    symetria, normalMatricesSym, normalMatricesAsym, cerosTodas = calcularSymMatricesNormal(matrices,True)
    GM = [] #Lista de Gi
    WGM= []
    SD = [] #Lista de SDi
    WSD = []
    CRITICM = [] #Lista de Ci
    WCRITICM = []
    matrixesSAGM = copy.deepcopy(matrices)
    matrixesSASD = copy.deepcopy(matrices)
    matrixesSACRITICM = copy.deepcopy(matrices)
    if symetria:
        # ------- SYMETRICAS ------- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0
            
            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

            CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

            
        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesSym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

            CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

    else:

        # ------ NO SYMETRICAS ----- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

            CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesAsym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

            CRITICM = nm.criticm(symetria,SD,normalMatricesAsym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
    resultados = {
        'symetria'  :   symetria,
        'GMWM'      :   [matrixesSAGM, WGM],
        'SDWM'      :   [matrixesSASD, WSD],
        'CRITICM'   :   [matrixesSACRITICM, WCRITICM]
    }


    return resultados        


    
def ocho(matrices,pesosManuales):
    """
    Aqui se espera que lleguen los pesos objetivos de forma manual
    """
    # --------- CASO 8 --------- #
    # --------- MANUAL --------- #
    symetria = calcularSymMatricesNormal(matrices,False)[0]
    matrixesSAMAN = copy.deepcopy(matrices)
    matrixesSAMAN, WMAN = poblarMatsPO(pesosManuales,matrixesSAMAN,True)

    resultados = {
        'symetria'  :   symetria,
        'MAN'       :   [matrixesSAMAN, WMAN],
    }

    return resultados

def nueve(matrices,pesosManuales):
    # --------- CASO 9 --------- #
    # ----- MANUAL,CRITICM ----- #
    symetria, normalMatricesSym, normalMatricesAsym = calcularSymMatricesNormal(matrices)
    SD = [] #Lista de SDi
    CRITICM = [] #Lista de Ci
    WCRITICM = []

    matrixesSAMAN = copy.deepcopy(matrices)
    matrixesSACRITICM = copy.deepcopy(matrices)

    matrixesSAMAN, WMAN = poblarMatsPO(pesosManuales,matrixesSAMAN,True)


    if symetria:
        # ------- SYMETRICAS ------- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
        CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
        matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
        
    else:
        # ------ NO SYMETRICAS ----- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
        CRITICM = nm.criticm(symetria,SD,normalMatricesAsym)
        matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
        
    resultados = {
        'symetria'  :   symetria,
        'MAN'       :   [matrixesSAMAN, WMAN], 
        'CRITICM'   :   [matrixesSACRITICM, WCRITICM]
    }
    return resultados

def diez(matrices,pesosManuales):
    # --------- CASO 10 -------- #
    # ------- MANUAL,SDWM ------ #
    symetria, normalMatricesSym, normalMatricesAsym = calcularSymMatricesNormal(matrices)

    SD = [] #Lista de SDi
    WSD = []

    matrixesSAMAN = copy.deepcopy(matrices)
    matrixesSASD = copy.deepcopy(matrices)


    matrixesSAMAN, WMAN = poblarMatsPO(pesosManuales,matrixesSAMAN,True)


    if symetria:
        # ------- SYMETRICAS ------- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
        matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

        
        
    else:
        # ------ NO SYMETRICAS ----- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
        matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

    resultados = {
        'symetria'  :   symetria,
        'MAN'       :   [matrixesSAMAN, WMAN],
        'SDWM'      :   [matrixesSASD, WSD],
    }


    return resultados

def once(matrices,pesosManuales):
    # --------- CASO 11 -------- #
    # --- MANUAL,SDWM,CRITICM -- #
    symetria, normalMatricesSym, normalMatricesAsym = calcularSymMatricesNormal(matrices)
    SD = [] #Lista de SDi
    WSD = []
    CRITICM = [] #Lista de Ci
    WCRITICM = []
    
    matrixesSAMAN = copy.deepcopy(matrices)
    matrixesSASD = copy.deepcopy(matrices)
    matrixesSACRITICM = copy.deepcopy(matrices)

    matrixesSAMAN, WMAN = poblarMatsPO(pesosManuales,matrixesSAMAN,True)


    if symetria:
        # ------- SYMETRICAS ------- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
        matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

        CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
        matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

    else:
        # ------ NO SYMETRICAS ----- #
        SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
        matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

        CRITICM = nm.criticm(symetria,SD,normalMatricesAsym)  
        matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)


    resultados = {
        'symetria'  :   symetria,
        'MAN'       :   [matrixesSAMAN, WMAN], 
        'SDWM'      :   [matrixesSASD, WSD], 
        'CRITICM'   :   [matrixesSACRITICM, WCRITICM]
    }

    return resultados

def doce(matrices,pesosManuales):
    # --------- CASO 12 -------- #
    # ------- MANUAL,GMWM ------ #
    symetria, normalMatricesSym, normalMatricesAsym, cerosTodas = calcularSymMatricesNormal(matrices,True)

    GM = [] #Lista de Gi
    WGM= []
    matrixesSAGM = copy.deepcopy(matrices)
    matrixesSAMAN = copy.deepcopy(matrices)

    matrixesSAMAN, WMAN = poblarMatsPO(pesosManuales,matrixesSAMAN,True)

    if symetria:
        # ------- SYMETRICAS ------- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesSym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

    else:
        # ------ NO SYMETRICAS ----- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesAsym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

    resultados = {
        'symetria'  :   symetria,
        'MAN'       :   [matrixesSAMAN, WMAN], 
        'GMWM'      :   [matrixesSAGM, WGM],
    }
    return resultados

def trece(matrices,pesosManuales):
    # --------- CASO 13 -------- #
    # --- MANUAL,GMWM,CRITICM -- #
    symetria, normalMatricesSym, normalMatricesAsym, cerosTodas = calcularSymMatricesNormal(matrices,True)
    GM = [] #Lista de Gi
    WGM= []
    SD = [] #Lista de SDi
    WSD = []
    CRITICM = [] #Lista de Ci
    WCRITICM = []
    matrixesSAMAN = copy.deepcopy(matrices)
    matrixesSAGM = copy.deepcopy(matrices)
    matrixesSACRITICM = copy.deepcopy(matrices)

    matrixesSAMAN, WMAN = poblarMatsPO(pesosManuales,matrixesSAMAN,True)


    if symetria:
        # ------- SYMETRICAS ------- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0
            
            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            CRITICM = nm.criticm(symetria,SD,normalMatricesAsym) 
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesSym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            CRITICM = nm.criticm(symetria,SD,normalMatricesAsym) 
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

    else:
        # ------ NO SYMETRICAS ----- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            CRITICM = nm.criticm(symetria,SD,normalMatricesAsym) 
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesAsym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            CRITICM = nm.criticm(symetria,SD,normalMatricesAsym) 
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

    resultados = {
        'symetria'  :   symetria,
        'MAN'       :   [matrixesSAMAN, WMAN], 
        'GMWM'      :   [matrixesSAGM, WGM],
        'CRITICM'   :   [matrixesSACRITICM, WCRITICM]
    }


    return resultados

def catorce(matrices,pesosManuales):
    # --------- CASO 14 -------- #
    # ---- MANUAL,GMWM,SDWM ---- #
    symetria, normalMatricesSym, normalMatricesAsym, cerosTodas = calcularSymMatricesNormal(matrices,True)

    GM = [] #Lista de Gi
    WGM= []
    SD = []
    WSD = []


    matrixesSAMAN = copy.deepcopy(matrices)
    matrixesSAGM = copy.deepcopy(matrices)
    matrixesSASD = copy.deepcopy(matrices)

    matrixesSAMAN, WMAN = poblarMatsPO(pesosManuales,matrixesSAMAN,True)


    if symetria:
        # ------- SYMETRICAS ------- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesSym)    
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)
        
            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

    else:
        # ------ NO SYMETRICAS ----- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesAsym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)
    
    resultados = {
        'symetria'  :   symetria,
        'MAN'       :   [matrixesSAMAN, WMAN], 
        'GMWM'      :   [matrixesSAGM, WGM],
        'SDWM'      :   [matrixesSASD, WSD],
    }

    return resultados


def quince(matrices,pesosManuales):
    # --------- CASO 15 -------- #
    #  MANUAL,GMWM,SDWM,CRITICM  #
    symetria, normalMatricesSym, normalMatricesAsym, cerosTodas = calcularSymMatricesNormal(matrices,True)

    GM = [] #Lista de Gi
    WGM= []
    SD = [] #Lista de SDi
    WSD = []
    CRITICM = [] #Lista de Ci
    WCRITICM = []

    matrixesSAMAN = copy.deepcopy(matrices)
    matrixesSAGM = copy.deepcopy(matrices)
    matrixesSASD = copy.deepcopy(matrices)
    matrixesSACRITICM = copy.deepcopy(matrices)

    matrixesSAMAN, WMAN = poblarMatsPO(pesosManuales,matrixesSAMAN,True)

    if symetria:
        # ------- SYMETRICAS ------- #
        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

            CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
            matrixesSACRITICM, CRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesSym) 
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesSym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

            CRITICM = nm.criticm(symetria,SD,normalMatricesSym)
            matrixesSACRITICM, WCRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
    else:

        if cerosTodas:
            WGM= 0
            matrixesSAGM = 0



            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

            CRITICM = nm.criticm(symetria,SD,normalMatricesAsym) 
            matrixesSACRITICM, CRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)

        else:
            GM = nm.calcularCriticalValues(nm.gmwm,symetria,normalMatricesAsym)
            matrixesSAGM, WGM = poblarMatsPO(GM,matrixesSAGM,False)

            SD = nm.calcularCriticalValues(nm.sdwm,symetria,normalMatricesAsym)
            matrixesSASD, WSD = poblarMatsPO(SD,matrixesSASD,False)

            CRITICM = nm.criticm(symetria,SD,normalMatricesAsym)  
            matrixesSACRITICM, CRITICM = poblarMatsPO(CRITICM,matrixesSACRITICM,False)
    



    resultados = {
        'symetria'  :   symetria,
        'MAN'       :   [matrixesSAMAN, WMAN], 
        'GMWM'      :   [matrixesSAGM, WGM],
        'SDWM'      :   [matrixesSASD, WSD],
        'CRITICM'   :   [matrixesSACRITICM, WCRITICM]
    }


    return resultados

def caseSelection(matrices,case,manual=np.array([])):
    """
        Simula el comportamiento de un switch case

        Dependiendo del case que se le pase (1-15), que son las llaves del dict, retorna la 
        función que se necesita

        PARAMETERS:
        matrices: las matrices objetivo que se van a trabajar
        case: int, el caso convertido del vector binario
        manual: los pesos objetivos escritos manualmente
    """
    switcher = {
        1: uno,
        2: dos,
        3: tres,
        4: cuatro,
        5: cinco,
        6: seis,
        7: siete,
        8: ocho,
        9: nueve,
        10: diez,
        11: once,
        12: doce,
        13: trece,
        14: catorce,
        15: quince
    }
    func = switcher.get(case, lambda: "Invalid")
    return func(matrices,manual)