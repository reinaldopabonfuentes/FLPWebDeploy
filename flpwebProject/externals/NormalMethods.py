import numpy as np 
import copy 



def isSimmetryc(matrix):
    """Revisa si una matriz es simétrica
    
    Parameters
    ----------
    matrix : np matrix
        La matriz objetivo que se va a utilizar
    
    Returns
    -------
    boolean : True or False
        Si la matriz es simétrica True, False de lo contrario
        
    Para saber si la matriz es simétrica, se toma la triangular superior y 
    la inferior, luego alguna de las dos se transpone para comparar si 
    ambas matrices quedan iguales, si ambas son iguales (cada elemento de 
    ambas matrices son iguales), son simétricas devuelve True; 
    si no son iguales, devuelve False
    """

    matriz = np.copy(matrix)
    #Se obtienen la triangular superior e inferior y deja el resto en 0s
    upper = np.triu(matriz,1) # 1 es el desfase para no incluir la diagonal
    lower = np.tril(matriz,-1) # -1 es el desfase para no incluir la diagonal 
    mBools = lower == upper.T  #crea una matriz de Booleanos
    return mBools.all() 

def hayCerosDiag(matrix):
    """Revisa si la matriz tiene ceros en elementos diferentes a la diagonal
        
    Parameters
    ----------
    matrix : np matrix
        La matriz objetivo que se va a utilizar
    
    Returns
    -------
    hayCeros : True or False
        True si la matriz tiene 0s en lugares diferentes a la diagonal,
        False en caso contrario
    indicesCeros : np array
        Array con los posiciones [i,j] de los elementos que son cero en 
        la matriz
        Si no hay 0s, retorna 0

    La matriz se rellena de unos porque la diagonal siempre va a tener 0s,
    entonces no es necesario evaluarla
    argwhere toma los indices de la matriz que cumplen la condición
    """

    hayCeros = False 
    matriz = np.copy(matrix)
    np.fill_diagonal(matriz,1)#rellena la diagonal con 1s,
    indicesCeros = np.argwhere(matriz == 0)#devuelve los indices donde los elementos son  cero
    if np.size(indicesCeros): #si indices tiene tamaño, significa que sie contró ceros
        hayCeros = True #True si np.size=1, False si da 0
        return hayCeros, indicesCeros
    else:
        return hayCeros, 0

def hayCeros(matrices):
    """
    Mira si hay ceros en alguna de todas las matrices objetivo
    que se van a trabajar

    Parameters
    ----------
    matrices : np array de la clase Matriz
        Las matrices objetivo que se van a utilizar
    
    Returns
    -------
    resulCeros : boolean
        True si alguna matriz tiene un cero, 
        False de lo contrario
    
    matricesCeros : np matrix
        Matrices que tienen algun cero
    
    matricesNoCeros : np matrix
        Matrices que no tienen ceros

    """
    matrixes = np.copy(matrices)
    # matrixes = [x.getNumpyMatrix() for x in matrixes]
    matrixesCeros = []
    nombresMatricesCeros = []
    matrixesNoCeros = []
    resulCeros = False
    for i,matrix in enumerate(matrixes):
        matriz=matrixes[i].getNumpyMatrix()
        nombreMatriz = matrixes[i].nombre
        if hayCerosDiag(matriz)[0]:
            resulCeros = True 
            matrixesCeros.append(matriz)
            nombresMatricesCeros.append(nombreMatriz)
        else:
            matrixesNoCeros.append(matrix)
    matricesCeros = np.asarray(matrixesCeros)
    matricesNoCeros = np.asarray(matrixesNoCeros)
    nombresMatricesCeros = np.asarray(nombresMatricesCeros)
    return resulCeros, matricesCeros, nombresMatricesCeros, matricesNoCeros


def areSym(matrices):
    """Revisa si todas las matrices de la lista son simétricas
 
    Parameters
    ----------
    matrices : np list
        Lista de matrices tipo np con todas las matrices objetivo
    
    Returns
    -------
    resultSymmetric : boolean
        True si todas las matrices son simétricas, de lo contrario False
    
    indices : np array
        Posiciones dónde hay matrices no simétricas


    (resultSymmetric, indices) : boolean Tuple

        
    Nota:
        Si una matriz es asimétrica se deben tratar todas como asimétricas
    """

    symetrics = []
    matrixes = np.copy(matrices)
    # matrixes = [x.getNumpyMatrix() for x in matrixes]
    for matrix in matrixes:
        #se guardan ceros para que nonzero guarde las posiciones de los 1s
        #que son los que no son simétricos

        if isSimmetryc(matrix):
            symetrics.append(0)
        else:
            symetrics.append(1)
    symetrices = np.asarray(symetrics)
    indices = np.nonzero(symetrices)
    resultSymmetric = (symetrices == 0).all()
    if resultSymmetric:
        return resultSymmetric, 0
    else:
        return  resultSymmetric, indices[0]

def normalMatrix(symetria, matrix):
    """
    Devuelve la matriz normalizada dependiendo si es simétrica o no


    Parameters
    ----------
    symetria : boolean
        Condicion de si matrix es simétrica o no
        True si todas las matrices son simétricas, False de lo contrario

    matrix : np matriz
        Matriz objetivo a normalizar
    
    Returns
    -------
    matrix/s : matriz noramlizada
    """
    matriz = np.copy(matrix)
    matriz = np.absolute(matriz) #se saca valor absoluto la matrix
    m = matriz.shape[0] #tamaño de la matriz
    if(symetria):
        upperEls = matriz[np.triu_indices(m,1)]#obtiene los elementos de la triangular superior en una lista, 
        #1 es el desfase para no incluir la diagonal, saca valor absoluto de los elementos
        s = np.sum(upperEls)#obtiene la suma de la matriz superior     
        return  matriz / s #Devuelve la matriz normalizada
    else:
        s = np.sum(matriz) #obtiene la suma de toda la matriz 
        return  matriz / s  #Devuelve la matriz normalizada

def normalMatrixesSym(matrices):
    """

    Normaliza las matrices que se le pasan como parametro cuando son simétricas 

    Parameters
    ----------

    matrices : np list
       Lista de matrices tipo np con todas las matrices objetivo
    
    Returns
    -------
    np.asarray(normalMatrixes) : np list de matrices normalizadas
    """
    matrixes = np.copy(matrices)
    # matrixes = [x.getNumpyMatrix() for x in matrixes]
    matrixes = np.absolute(matrixes) #se saca valor absoluto la matrix
    normalMatrixes = []
    for matriz in matrixes:
        m = matriz.shape[0] #tamaño de la matriz
        upperEls = matriz[np.triu_indices(m,1)]#obtiene los elementos de la triangular superior en una lista, 
        #1 es el desfase para no incluir la diagonal, saca valor absoluto de los elementos
        s = np.sum(upperEls)#obtiene la suma de la matriz superior     
        normalMatrixes.append(matriz / s) #Devuelve la matriz normalizada
    return np.asarray(normalMatrixes)


def normalMatrixesAsym(matrices):
    """
    Normaliza las matrices  que se le pasan como parametro cuando son asimétricas


    Parameters
    ----------

    matrices : np list
       Lista de matrices tipo np con todas las matrices objetivo
    
    Returns
    -------
    np.asarray(normalMatrixes) : np list de matrices normalizadas
    """
    matrixes = np.copy(matrices)
    # matrixes = [x.getNumpyMatrix() for x in matrixes]
    matrixes = np.absolute(matrixes) #se saca valor absoluto la matrix
    normalMatrixes = []
    for matriz in matrixes:
        s = np.sum(matriz)  
        normalMatrixes.append(matriz / s) #Devuelve la matriz normalizada
    return np.asarray(normalMatrixes)

def mostrarMatricesCeros(matricesCeros, nombresMatricesCeros):
    """
    Imprime en pantalla cuáles matrices tienen ceros
    en posiciones diferentes a la diagonal de la matriz


    Parameters
    ----------

    matricesCeros : np list
       Lista de matrices tipo np con las matrices que tienen ceros
       en lugares diferentes a la diagonal
    nombresMatricesCeros: 
    
    Returns
    -------
    Imprime en pantalla la info de las matrices que contienen ceros
    """
    print("El Método GMWM, no se puede utilizar, ")
    print("existen {} matrices no aptas para este método \n".format(matricesCeros.shape[0]))
    for i,matrix in enumerate(matricesCeros):
        indicesCeros = hayCerosDiag(matrix)[1]
        print("La Matriz:  {} \n".format(nombresMatricesCeros[i]))
        print(matrix)
        print("\n Contiene ceros en las posiciones \n")
        print(indicesCeros)
        print("\n----------------------------------------------\n")  

def gmwm(symetria,normalMatrix):
    """

    Calcula un Gt de la matriz objetivo que se le ingrese

    Parameters
    ----------
    symetria : boolean
        Condicion de si matrix es simétrica o no
        True si todas las matrices son simétricas, False de lo contrario
    
    normalMatrix: np matriz
        Matriz objetivo normalizada
    
    Returns
    -------
    GM   : 
        Valor de la Media Geométrica para una matriz
    
    """
    GM = 0
    normalizedMatrix= np.copy(normalMatrix)  
    m = normalizedMatrix.shape[0]#obtiene el tamaño de la matriz
    g = lambda x,y : (np.product(x))**(1/y) #expresion para calcular el G
    absMatrix = np.absolute(normalizedMatrix) #saca el valor absoluto de cada elemento de toda la matriz
    #verifica si en la matriz en los elementos donde i != j hay 0s, si los hay no sirve este método
    if symetria:#Verifica si la matriz es simétrica
        n = (m * (m-1))/2 #calcula la raiz
        upperEls = absMatrix[np.triu_indices(m,1)] #obtiene la triangular superior de la matriz normalizada
        GM = g(upperEls,n) #calculo del g
    else:
        n = m*(m-1) #calcula la raiz
        #la diagonal siempre va a tener ceros debido al FLP porque no hay relaciones entre cada mismo dpto, por lo tanto,
        #se llena con 1s la diagonal para no obtener 0 en el resultado de la productoria
        np.fill_diagonal(absMatrix,1) #rellenar de 1s la diagonal
        GM = g(absMatrix,n) #calcula el g
    return GM





def sdwm(symetria, normalMatrix):
    """

    Calcula un SD de la matriz objetivo que se le ingrese

    Parameters
    ----------
    symetria : boolean
        Condicion de si matrix es simétrica o no
        True si todas las matrices son simétricas, False de lo contrario
    
    normalMatrix: np matriz
        Matriz objetivo normalizada
    
    Returns
    -------
    SD   : 
        Valor de la Desviación Estándar para una matriz
    
    """
    #Calcula el SD de la matriz normalizada que se le ingresa
    SD= 0
    normalizedMatrix = np.copy(normalMatrix)
    m = normalizedMatrix.shape[0]#obtiene el tamaño de la matriz
    sd = lambda num,den : (num/den)**(1/2) #expresion para calcular SD
    # maskUpper = np.mask_indices(m, np.triu, 1) #Máscara para poder obtener los elementos de la diagonal superior
    # maskLower = np.mask_indices(m, np.tril, -1) #Máscara para poder obtener los elementos de la diagonal inferior
    upper = normalizedMatrix[np.triu_indices(m,1)] # Obtiene elementos diagonal superior
    lower = normalizedMatrix[np.tril_indices(m,-1)] # Obtiene elementos diagonal superior
    upperAbs = np.abs(upper)
    if(symetria):#Verifica si la matriz es simétrica
        media = np.absolute(np.mean(upper))#obtiene la media
        num = np.sum((upperAbs - np.mean(media))**2) #calcula el numerador
        den = ((m * (m-1))/2)-1 #calcula el denominador
        SD = sd(num,den) #calculo del SD
    else:
        # lower = np.tril(normalizedMatrix,-1) # Obtiene elementos diagonal inferior
        matrixNoDiag = np.append(upper,lower)
        matrixNoDiagAbs = np.abs(matrixNoDiag)
        mean = np.absolute(np.mean(matrixNoDiag))
        num = np.sum((matrixNoDiagAbs - mean)**2) #calcula el numerador
        den = (m*(m-1))-1 #calcula el denominador
        SD = sd(num,den) #calcula el SD
    return SD

def calcularCriticalValues(funcion, symetria, normalMatrixes, SD=None):
    """
    Crea la lista de los valores críticos (GMs, SDs, Cs) utlizando funcion
    que puede ser gmwm(symetria,normalMatrixes), sdwm(symetria,normalMatrixes)
    o criticm(symetria,normalMatrixes)
    """
    
    normalMatrices = np.copy(normalMatrixes)
    criticalValules = []
    for normalMatriz in normalMatrices:
        criticalValules.append(funcion(symetria,normalMatriz))
    return np.asarray(criticalValules)
    
def remove_diag(x):
    """
    Elimina la diagonal de la matriz x
    Copiado de 
    """
    
    x_no_diag = np.ndarray.flatten(x)
    x_no_diag = np.delete(x_no_diag, range(0, len(x_no_diag), len(x) + 1), 0)
    x_no_diag = x_no_diag.reshape(len(x), len(x) - 1)
    return x_no_diag


def criticm(symetria, SD, normalMatrixes):
    """

    Calcula un CRITICM de la matriz objetivo que se le ingrese

    Parameters
    ----------
    symetria : boolean
        Condicion de si matrix es simétrica o no
        True si todas las matrices son simétricas, False de lo contrario

    
    normalMatrixes: np matriz
        Matrices objetivo normalizadas
    
    SD   : Vector de Desviaciones Estándar para las matrices normalizadas
    
    Returns
    -------
    C   : np array Vector de CRITICMs para las matrices normalizadas
    
    """
    normalMatrices = np.copy(normalMatrixes)
    m=len(normalMatrices) #cantidad de matrices
    R= np.zeros((m,m))
    C = []
    n = len(normalMatrices[0]) #tamaño de cada matriz (cantidad de instalaciones)
    for i,matrix in enumerate(normalMatrices):
        upperI = matrix[np.triu_indices(n,1)] # Obtiene elementos diagonal superior
        meanI = np.absolute(np.mean(upperI))
        upperIAbs = np.abs(upperI)
        for j in range(i+1,m):
            matrixJ = normalMatrices[j]
            upperJ = matrixJ[np.triu_indices(n,1)] # Obtiene elementos diagonal superior
            meanJ = np.absolute(np.mean(upperJ))
            upperJAbs = np.abs(upperJ)
            if symetria:
                num = np.sum((upperIAbs - meanI)*(upperJAbs - meanJ))
                npp = ((n*(n-1))/2)-1 #n''
                den = npp*SD[i]*SD[j]
                r = num/den
                R[i][j] = r
            else:
                lowerI = matrix[np.tril_indices(n,-1)] # Obtiene elementos diagonal superior
                matrixNoDiagI = np.append(upperI,lowerI)
                meanI = np.absolute(np.mean(matrixNoDiagI))
                matrixNoDiagIAbs = np.abs(matrixNoDiagI)
                matrixJ = normalMatrices[j]
                lowerJ = matrixJ[np.tril_indices(n,-1)] # Obtiene elementos diagonal superior
                matrixNoDiagJ = np.append(upperJ,lowerJ)
                meanJ = np.absolute(np.mean(matrixNoDiagJ))
                matrixNoDiagJAbs = np.abs(matrixNoDiagJ)
                num = np.sum((matrixNoDiagIAbs - meanI)*(matrixNoDiagJAbs - meanJ))
                npp = (n*(n-1))-1 #n''
                den = npp*SD[i]*SD[j]
                r = num/den 
                R[i][j] = r
    R = R + R.T
    #superior en la triangular inferior de una forma corta y sin tanta asignación de vars
    rNoDiag = remove_diag(R)
    for i, row in enumerate(rNoDiag):
        sd = SD[i]
        rowResta = (1-row)
        suma = np.sum(rowResta)
        valor =  sd * suma
        C.append(valor)

    return np.asarray(C)

  

    
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
    # matrixes = [x.getNumpyMatrix() for x in matrixes]
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
