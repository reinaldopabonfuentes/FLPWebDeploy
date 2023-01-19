import numpy as np
class Matriz:
    

    # Initializer / Instance Attributes
    def __init__(
        self,
        idSim=1,
        nombre="Nombre de Matriz",
        data=np.array([]),
        signoFOChar="",
        pesoObjetivo=1.0,
        tipoMatriz = 'Otra',
        isReindexMatriz=False,
        isMatrizFlujoDist=False,
        signoFO=1.0,
        isMatrizDistance = False,
        isMatrizFlujo=False,
        ):
        """
        idSim = id de la matriz en la simulacion que se subió
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
        self.idSim = idSim
        self.nombre = nombre
        self.data = data
        self.signoFOChar = signoFOChar
        self.pesoObjetivo = pesoObjetivo
        self.tipoMatriz = tipoMatriz
        self.isReindexMatriz = isReindexMatriz
        self.signoFO = self.setSignoFO(signoFOChar)
        self.isMatrizDistance = self.setIsMatrizDist(self.tipoMatriz)
        self.isMatrizFlujo = self.setIsMatrizFlujo(self.tipoMatriz)
        self.isMatrizFlujoDist = self.setIsMatrizFlujoDist(self.isMatrizFlujo,self.isMatrizDistance)



    def setIsMatrizDist(self,tipoMatriz):
        """
        Dependiento del texto que se recibe,
        marca como True o False si es Matriz Distancia
        """
        if 'Distancia' == tipoMatriz:
            return True
        else:
            return False

    def setIsMatrizFlujo(self,tipoMatriz):
        """
        Dependiento del texto que se recibe,
        marca como True o False si es Matriz Flujo
        """

        if 'Flujo de Materiales' == tipoMatriz:
            return True
        else:
            return False


    
    def setIsMatrizFlujoDist(self, isMatrizFlujo, isMatrizDistance):
        if isMatrizFlujo or isMatrizDistance:
            return True
        else:
            return False
            


    def setSignoFO(self, signoFO):
        if(signoFO == "+"):
           return 1
        elif(signoFO == "-"):
            return -1
        else:
            print("Debe ingresar + o - para el signo de la matriz ")
            print(self.nombre)
            return "ERROR"
            
    def setPesoObjetivo(self, pesoObjetivo):
        self.pesoObjetivo = pesoObjetivo
    
    def __str__(self):


        multiline = (
            'Matriz con: \n'
            f'idSim: {self.idSim} \n'
            f'Nombre: {self.nombre} \n'
            f'Data:\n {self.data} \n'
            f'isMatrizFlujoDist: {self.isMatrizFlujoDist}\n'
            f'signoFOChar: {self.signoFOChar}\n'
            f'signoFO: {self.signoFO}\n'
            f'isReindexMatriz: {self.isReindexMatriz}\n'
            f'isMatrizDistance: {self.isMatrizDistance}\n'
            f'isMatrizFlujo: {self.isMatrizFlujo}\n'
            f'Peso: {self.pesoObjetivo}\n'
            f'tipoMatriz: {self.tipoMatriz}\n'
        )
        return multiline


        
# <!--
# {% if usa_man %}
#     <table>
#         <tr>
#             <th>Nombre</th>
#             <th>Matriz</th>
#             <th>Signo en la Función Objetivo</th>
#             <th>Tipo de Matriz</th>
#             <th>¿Se debe reindexar la Matriz?</th>
#             <th>Peso Manual</th>
#         </tr>
#         <tr>
#             {% for nombre in nombresMatrices%}
#             {% for matrix in matrices %}
#             {% for signo in signosMatrices %}
#             {% for tipo in tiposMatrices %}
#             {% for reindex in reindexesMatrices %}
#             {% for pesoObjetivo in valorPesosMatrices %}


#                                     <td>{{nombre}}</td>
#                                     <td>
#                                         {% for row in matrix %}
#                                             <tr>
#                                             {% for cell in row %}
#                                                 <td> 
#                                                     {{ cell }}
#                                             </td>
#                                             {% endfor %}
#                                             </tr>
#                                         {% endfor %}
#                                     </td>
#                                     <td>{{signo}}</td>
#                                     <td>{{tipo}}</td>
#                                     <td>{{reindex}}</td>
#                                     <td>{{pesoObjetivo}}</td>

#             {% endfor %}
#             {% endfor %}
#             {% endfor %}
#             {% endfor %}
#             {% endfor %}
#             {% endfor %}

#         </tr>
#     </table>
# {% else %}
#         <table>
#             <tr>
#                 <th>Nombre</th>
#                 <th>Matriz</th>
#                 <th>Signo en la Función Objetivo</th>
#                 <th>Tipo de Matriz</th>
#                 <th>¿Se debe reindexar la Matriz?</th>
#             </tr>
#             <tr>
#                 {% for nombre in nombresMatrices%}
#                 {% for matrix in matrices %}
#                 {% for signo in signosMatrices %}
#                 {% for tipo in tiposMatrices %}
#                 {% for reindex in reindexesMatrices %}


#                                         <td>{{nombre}}</td>
#                                         <td>
#                                             {% for row in matrix %}
#                                                 <tr>
#                                                 {% for cell in row %}
#                                                     <td> 
#                                                         {{ cell }}
#                                                 </td>
#                                                 {% endfor %}
#                                                 </tr>
#                                             {% endfor %}
#                                         </td>
#                                         <td>{{signo}}</td>
#                                         <td>{{tipo}}</td>
#                                         <td>{{reindex}}</td>

#                 {% endfor %}
#                 {% endfor %}
#                 {% endfor %}
#                 {% endfor %}
#                 {% endfor %}
#             </tr>
#         </table>
# {% endif %}


 
# -->