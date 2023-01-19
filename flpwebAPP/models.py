from django.db import models
from django.core.validators import MinValueValidator

import csv, io, copy
import numpy as np

from django.contrib.auth.models import User
from io import StringIO
from django.contrib import messages
import base64
try:
    import cPickle as pickle
except:
    import pickle
# Create your models here.


class MetPesoObj(models.Model):
    nombre = models.CharField(
        max_length=50,
        verbose_name="Nombre Método Cómputo Matrices Objetivos"
        )
    # usa_met = models.BooleanField(default=False, editable=False)
    codigo = models.CharField(max_length=7, editable=False, null=True)
    valor_peso = models.FloatField(verbose_name="Valor Peso Objetivo",null=True)
 

    class Meta:
        verbose_name = "Método Cómputo de Matrices Objetivos"
        verbose_name_plural = "Métodos Cómputo de Matrices Objetivos"

    def __str__(self):
        return f"Código Metodo: {self.codigo}\nNombre Método: {self.nombre}\nValor: {self.valor_peso}"

class Matriz(models.Model):
    """
        nombre: nombre de la matriz
        data: numpy array que contiene la matriz
        signoFOChar: char
            signo de la matriz en la FO recibida desde el Form
        pesoObjetivo: float
            valor del peso de la matriz ya sea Manual o Calculado con los Métodos
        tipoMatriz:char
            Recibe solo tres opciones:
                -'Distancia'
                -'Flujo de Materiales'
                -'Otra' Default
            Recibido desde el form y dependiendo de esto marca True en isMatrizFlujo, isMatrizDistance
        isReindexMatriz: bool True si la matriz objetivo tiene que ser reindexada con el nuevo vector solución,
                         ejm: matriz de distancia, matriz de tiempo de manejo de materiales
                         False caso contrario
        signoFO: Float
            signo que debería ir en la función objetivo al multiplicar esta matriz, lo da el usuario
            , solo puede ser 1 o -1 asignado con la funcion set...
        isMatrizDistance: Bool
        True si es una matriz de distancia, asignada con el  set
            False caso contrario
        isMatrizFlujo: Bool
            True si es una matriz de flujo, asignada con el set
            False caso contrario
        isMatrizFlujoDist: bool True si es la matriz de las distancias entre instalaciones o la matriz de Flujo de materiales,
                           False si es una matriz objetivo diferente 
        
        """
    #CHOICES
    POSITIVO = '+'
    NEGATIVO = '-'
    SIGNO_FO_CHAR_CHOICES = [
        (POSITIVO,'+'),
        (NEGATIVO,'-'),
    ]
    MATFLUJO = 'Flujo de Materiales'
    MATDISTANCIA = 'Distancia'
    OTRA = 'Otra'
    TIPO_MATRIX_CHOICES = [
        (MATDISTANCIA,'Distancia'),
        (MATFLUJO,'Flujo de Materiales'),
        (OTRA,'Otra'),
    ]

    #FIELDS
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la matriz/objetivo"
        )
    data = models.TextField(
        editable=False,
        verbose_name="Datos de la Matriz (Archivo CSV)"
        )
    dataNumpy = models.BinaryField(editable=False)
    isMatrizFlujoDist = models.BooleanField(
        default=False,
        verbose_name="¿Es una matriz de Flujo o de Distancia?",
        editable=False
        )
    signoFOChar = models.CharField(
        max_length=1,
        choices = SIGNO_FO_CHAR_CHOICES,
        default = POSITIVO,
        verbose_name="Signo en la Función Objetivo"
        )
    signoFO = models.FloatField(
        null=True,
        editable=False,#No lo puede editar en un form el user
        )
    isReindexMatriz = models.BooleanField(
        default=False,
        verbose_name="¿La Matriz debe ser reindexada?"
        )
    isMatrizDistance = models.BooleanField(
        default=False,
        verbose_name="¿Es Matriz de Distancia?"
        )
    isMatrizFlujo= models.BooleanField(
        default=False,
        verbose_name="¿Es Matriz de Flujo?",
        editable=False
        )
    pesoObjetivo = models.FloatField(
        null=True,
        default=1.0,
        editable=False
    )
    tipoMatriz = models.CharField(
        max_length=20,
        choices = TIPO_MATRIX_CHOICES,
        default = OTRA,
        verbose_name="¿Qué tipo de Matriz es?"
    )

    #related_name es para reverse relationship references and queries
    #see https://www.webforefront.com/django/setuprelationshipsdjangomodels.html
    #se utiliza related_name = 'foreignKey_tablaDondeEsta'
    metPesoObjs = models.ManyToManyField(
        MetPesoObj,
        editable=False,
        related_name='pesos_matrices'
        )


    def __str__(self):
        multiline = (
            f'Nombre: {self.nombre} \n'
            f'Data:\n {self.data} \n'
            f'DataByte:\n {self.dataNumpy} \n'
            f'isMatrizFlujoDist: {self.isMatrizFlujoDist}\n'
            f'signoFOChar: {self.signoFOChar}\n'
            f'signoFO: {self.signoFO}\n'
            f'isReindexMatriz: {self.isReindexMatriz}\n'
            f'isMatrizDistance: {self.isMatrizDistance}\n'
            f'isMatrizFlujo: {self.isMatrizFlujo}\n'
            f'tipoMatriz: {self.tipoMatriz}\n'
            f'pesoObjetivo: {self.pesoObjetivo}\n'
        )
        return multiline

    def setIsReindexMatriz(self):
        if self.isMatrizDistance or self.isReindexMatriz:
            self.isReindexMatriz = True
        else:
            self.isReindexMatriz = False



    def getNumpyMatrix(self):
        """
        Retorna la dataNumpy que son Bytes
        en una matriz numpy
        """
        return pickle.loads(base64.b64decode(self.dataNumpy))

    def setIsMatrizDist(self,tipoMatriz):
        """
        Dependiento del texto que se recibe,
        marca como True o False si es Matriz Distancia
        """
        if 'Distancia' == tipoMatriz:
            self.isMatrizDistance=True
        else:
            self.isMatrizDistance=False


    def setIsMatrizFlujo(self,tipoMatriz):
        """
        Dependiento del texto que se recibe,
        marca como True o False si es Matriz Flujo
        """

        if 'Flujo de Materiales' == tipoMatriz:
            self.isMatrizFlujo = True
        else:
            self.isMatrizFlujo = False



    
    def setIsMatrizFlujoDist(self, isMatrizFlujo, isMatrizDistance):
        if isMatrizFlujo or isMatrizDistance:
            self.isMatrizFlujoDist = True
        else:
            self.isMatrizFlujoDist = False
            


    def setSignoFO(self, signoFO):
        if(signoFO == "+"):
            self.signoFO = 1
        elif(signoFO == "-"):
            self.signoFO = -1

    def save(self, *args, **kwargs):
        """
        Modifico los valores de los campos dependientes tanto en el objeto
        como en la BD antes de guardarlos
        """

        self.setSignoFO(self.signoFOChar)
        self.setIsMatrizDist(self.tipoMatriz)
        self.setIsMatrizFlujo(self.tipoMatriz)
        self.setIsMatrizFlujoDist(self.isMatrizFlujo,self.isMatrizDistance)
        self.setIsReindexMatriz()
        super(Matriz,self).save(*args, **kwargs)



    class Meta:
        verbose_name_plural = "Matrices"


class Solucion(models.Model):
    mejor_sln = models.TextField(editable=False)
    mejor_fo = models.FloatField(editable=False)
    vals_x = models.TextField(editable=False)
    vals_y = models.TextField(editable=False)
    metPesoObjs = models.ManyToManyField(
        MetPesoObj,
        editable=False,
        related_name='pesos_slns'
    )
    
    class Meta:
        verbose_name_plural = "Soluciones Simulacion"

    def __str__(self):
        return f"Mejor sln {self.mejor_sln}"

class Simulacion(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre de la Simulación")
    #LOS METODOS A UTILIZAR VAN A HACER UN 1 o 0 DEPENDIENDO DE LO 
    #QUE SE MANDE EN EL FORMULARIO
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)
    met_manual = models.BooleanField(
        verbose_name="Método Manual",
        default=False
        )
    met_gmwm = models.BooleanField(
        verbose_name="Método Media Geométrica",
        default=False
        )
    met_sdwm = models.BooleanField(
        verbose_name="Método Desviación Estándar",
        default=False
        )
    met_criticm = models.BooleanField(
        verbose_name="Método Matriz de Correlaciones",
        default=False
        )
    no_instalaciones = models.PositiveSmallIntegerField(
        verbose_name="Cantidad de instalaciones")    
    cantidad_matrices = models.PositiveSmallIntegerField(
        verbose_name="Cantidad de Matrices")    
    lambda1 = models.FloatField(
        verbose_name="Parámetro Lambda 1",
        validators=[MinValueValidator(0.0000001)]
        )
    lambda2 = models.FloatField(
        verbose_name="Parámetro Lambda 2",
        validators=[MinValueValidator(0.0000001)]
        )
    iteraciones = models.PositiveSmallIntegerField(verbose_name="Parámetro Cantidad Iteraciones")
    matrices = models.ManyToManyField(
        Matriz,
        editable=False,
        related_name='matrices_sims'
        )
    metPesoObjs = models.ManyToManyField(
        MetPesoObj,
        editable=False,
        related_name='pesos_sims'
        )
    soluciones = models.ManyToManyField(
        Solucion,
        editable=False,
        related_name='sols_sims'
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False,
        related_name='user_sims'
    )


    class Meta:
        verbose_name_plural = "Simulaciones"

    def __eq__(self, other):
        excluir = ['_state', 'ultima_modificacion', '_django_version']
        values = [(k,v) for k,v in self.__dict__.items() if k not in excluir]
        other_values = [(k,v) for k,v in other.__dict__.items() if k not in excluir]
        return values == other_values


    def __str__(self):
        return f"Simulacion Nombre: {self.nombre} fecha {self.fecha_creacion}"


    def getMetodosUsados(self):
        """
        Devuelve una lista de 1 o 0, dependiendo del metodo que se va a utilizar en la
        simulación
        """
        metodos = [
                self.met_manual,
                self.met_gmwm,
                self.met_sdwm,
                self.met_criticm]

        return np.asarray([1 if i else 0 for i in metodos])

    def convertirMetUsadosString(self,metodosUsados):
        """
        Convierte la lista metodosUsados que es [0,0,0,0]
        Con 1 donde si se utilice el método
        el orden es [MAN,GMWM,SDWM,CRITICM]
        """
        codigosMetodosUsados = []
        metodosUsadosString = []
        if metodosUsados[0]:
            metodosUsadosString.append('Método Manual')
            codigosMetodosUsados.append('MAN')
        if metodosUsados[1]:
            metodosUsadosString.append('Método de la Media Geométrica')
            codigosMetodosUsados.append('GMWM')
        if metodosUsados[2]:
            metodosUsadosString.append('Método de la Desviación Estándar')
            codigosMetodosUsados.append('SDWM')
        if metodosUsados[3]:
            metodosUsadosString.append('Método de Matriz de Correlaciones')
            codigosMetodosUsados.append('CRITICM')
        return metodosUsadosString, codigosMetodosUsados
