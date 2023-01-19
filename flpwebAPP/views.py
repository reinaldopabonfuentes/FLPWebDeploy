# import matplotlib
# matplotlib.use('TkAgg')
# from matplotlib import pyplot as plt

from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django import forms
from django.forms import modelformset_factory
from django.contrib import messages
#importaciones para login
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from flpwebAPP.models import Matriz, MetPesoObj, Simulacion, Solucion
from flpwebAPP.forms import MatrizFormPesoData, MatrizFormNoPesoData, SimulacionForm, BaseMatrizForm, MatrizFormPesoNoData
from flpwebProject.externals import PesosObjetivos  as po
from flpwebProject.externals import RecocidoSimulado  as sa
# from flpwebProject.externals.Matriz import Matriz
import csv, io, copy
import numpy as np
from urllib.parse import urlencode
from io import StringIO




#Imports from saving numpyMatrix in database
import base64
try:
    import cPickle as pickle
except:
    import pickle


# Create your views here.

# matrices.append(distanceMatrix)

NOMBRE_MET_MAN='Método Manual Ingresado por el usuario'
CODIGO_MET_MAN ='MAN'

NOMBRE_MET_GMWM='Método Media Geométrica'
CODIGO_MET_GMWM ='GMWM'

NOMBRE_MET_SDWM='Método Desviación Estándar'
CODIGO_MET_SDWM ='SDWM'

NOMBRE_MET_CRITICM='Método Matriz de Correlaciones'
CODIGO_MET_CRITICM ='CRITICM'

NOMBRE_MET_DIST = 'Método para Matriz Distancia'
CODIGO_MET_DIST ='DIST'

# class ObjetoVistas():
#     def __init__(
#         self,
#         metodosUsados=np.array([]),
#         matrices=np.array([]),
#         pesosMAN=np.array([])):
#         self.metodosUsados = metodosUsados
#         self.matrices = matrices
#         self.pesosMAN = pesosMAN


# objetoVista = ObjetoVistas()

def restorepassword(request):
    if request.method == 'GET':
        if "id_usuario" in request.session:
            return render(request, "inicio.html")
        else:
            return render(request, "restorepassword.html", {"error": ""})
    else:
        # user = authenticate(request, username=request.POST['nombreusuario'], email=request.POST['correousuario'])
        try:
            if request.POST['passwordusuario'] == request.POST['passwordusuario2']:
                user = User.objects.get(username=request.POST['nombreusuario'], email=request.POST['correousuario'])#Se trae el usuario creado
                # print(f"IGUALLLLLLLLLLLLLL ---------------------------------------------------- {user.id}")

                # metodo.password = request.POST['passwordusuario']
                # metodo.save()
                user.set_password(request.POST['passwordusuario'])
                user.save()
                return render(request,'singin.html', {"error": "Contraseña actualizada correctamente."})
            else:
                return render(request,'restorepassword.html', {"form": AuthenticationForm, "error": "Las contraseñas ingresadas no coinciden."})
            
        except:
            return render(request,'restorepassword.html', {"form": AuthenticationForm, "error": "No se encontró algún usuario con el nombre o el email introducidos. Intente nuevamente"})

def ordenarMatsDistFlujo(matrixes):

    """
    Coloca la matriz distancia en la posicion 0 y
    la matriz de flujo en la posición 1
    """
    matrices = copy.deepcopy(matrixes)
    #Revisa si hay matrices de flujo o distancia
    isMatrizFlujoDist = [x.isMatrizFlujoDist for x in matrices] #Almacena los true o false
    isMatrizFlujoDistarray = np.asarray(isMatrizFlujoDist)
    hayMatrFlujoDist = isMatrizFlujoDistarray.any()
    if hayMatrFlujoDist:
        for i,matrix in enumerate(matrices):
            if matrices[0].isMatrizDistance:
                break
            else:
                if matrix.isMatrizDistance:
                    temp = matrices[0]
                    matrices[0] = matrix
                    matrices[i] = temp

        for i,matrix in enumerate(matrices):
            if matrices[1].isMatrizFlujo:
                break
            else:
                if matrix.isMatrizFlujo:
                    temp = matrices[1]
                    matrices[1] = matrix
                    matrices[i] = temp
    return matrices

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'error': ''
        })
    else:
        if request.POST['passwordusuario'] == request.POST['passwordusuario2']:
            # register user
            try:
                # crea el usuario en base de datos y loguarda
                user = User.objects.create_user(
                    username=request.POST['nombreusuario'], password=request.POST['passwordusuario'], email=request.POST['correousuario'])
                user.save()
                login(request, user)
                usuario_creado = User.objects.get(username=request.POST['nombreusuario'])#Se trae el usuario creado
                print(f"ESTE ES EL USUARIOOOOOOO ---------------------------------------------------- {usuario_creado.id}")
                request.session["id_usuario"] = usuario_creado.id
                return redirect('inicio')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'error': 'Username already exist'
                })
        return render(request, 'signup.html', {
            'error': 'Password dont match'
        })

def singin(request):
    if request.method == 'GET':
        #del request.session["id_usuario"]
        if "id_usuario" in request.session:
            return render(request, "inicio.html")
        else:
            return render(request, "singin.html", {"form": AuthenticationForm, "error":" "})
    else:
        # print(f"DATA REQUEST --------------------------- {request.POST}")
        user = authenticate(request, username=request.POST['nombreusuario'], password=request.POST['passwordusuario'])
        if user is None:
            # print(f"NO es igual la contraseña ---------------------------------------------------- {user}")
            return render(request,'singin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})
        else:
            print(f"Si es igual la contraseña ---------------------------------------------------- {user}")
            login(request, user)
            request.session["id_usuario"] = user.id
            return redirect('inicio')
@login_required
def signout(request):
  logout(request)
  return redirect('inicio')

@login_required
def simulations(request):
    #trae todas la simulaciones de la BD
    simulations = Simulacion.objects.filter(user=request.user)
    bandera = ''
    if len(simulations) < 1:
        simulations = False
    
        
    return render(request, "list_simulation.html", {'simulations': simulations})



def inicio(request):
    return render(request, "inicio.html")

#
def upload(request):
    template = "upload.html"

    if request.method == 'GET':
        return render(request, template)

    csv_file = request.FILES['file'] #Toma el archivo que se envia

    if not csv_file.name.endswith('.csv'):
        messages.error(request,'El archivo no tiene la extensión .csv necesaria')




    data_set = csv_file.read().decode('UTF-8') #lee el archivo

    io_string = io.StringIO(data_set) #se convierte a un IOString

    numpyMatrix = np.genfromtxt(io_string, delimiter=",") #Convierto a numpy
    numpyMatrixString = np.array2string(numpyMatrix)

    data_bytes = pickle.dumps(numpyMatrix)
    data_base64 = base64.b64encode(data_bytes)

    numpyMatrixString = '\n'.join(','.join('%0.3f' %x for x in y) for y in numpyMatrix)



    creado = Matriz.objects.update_or_create(nombre ="Matriz Prueba", data=numpyMatrixString, dataNumpy =data_base64)
    # print(creado)
    numpyMatrixList = numpyMatrix.tolist()
    context = {
        'enviado' : numpyMatrixString,
        'numpyMatrix' : numpyMatrixList

        }
    print("\n")
    print("\n")

    # print("Lo que se creo {}".format(creado[0].data))
    dataBD =creado[0].dataNumpy
    data_bytesBD =  base64.b64decode(dataBD)
    data2 = pickle.loads(data_bytesBD)
    print(f"Recuperado de la BD {data2}")
    print(type(data2))

    return render(request, template, context)


@login_required
def nueva_sim(request):
    template = 'nueva_sim.html'

    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = SimulacionForm(request.POST)
        if form.is_valid():
            #TOMO LOS VALORES A PASAR A LA SGTE VISTA
            num_mats = form.cleaned_data.get("cantidad_matrices")
            matriz_size = form.cleaned_data.get("no_instalaciones")
            usa_man = form.cleaned_data.get("met_manual")
            new_simulation = form.save(commit=False)
            new_simulation.user = request.user
            new_simulation.save()
            
            

            id_sim = form.instance.id

            

            return redirect('subir_matrices',id_sim,num_mats,usa_man,matriz_size)
    else:
        # GET, generate unbound (blank) form
        # inicial = {}
        inicial = {
            'nombre':'Prueba',
            'met_manual' : True,
            # 'met_gmwm' : True,
            'met_sdwm' : True,
            'met_criticm' : True,
            'no_instalaciones' : 6,
            'cantidad_matrices' : 3,
            'lambda1' : 0.5,
            'lambda2' : 0.05,
            'iteraciones' : 1,
        }
        form = SimulacionForm(initial = inicial)
    context = {
        #nueva_sim = True, Si estoy trabajando con una nueva simulación
        #           False, si estoy editando una simulación
        'form':form,
        'nueva_sim':True,
    }
    return render(request,template,context)

def castNumpyToStringDB(numpyMatrix):
    """
    Convierte la matriz numpy en String para almacenar
    en el campo data que es un CharField
    """
    return '\n'.join(','.join('%0.3f' %x for x in y) for y in numpyMatrix)

def castByteToBase64(numpyMatrix):
    """
    Convierte una matrix numpy al buen valor
    para almacenarla en el fampo dataNumpy que es un BinaryField
    """
    np_data_bytes = pickle.dumps(numpyMatrix)
    return base64.b64encode(np_data_bytes)

def getMatricesBase64String(form,request):
    """
    Toma el archivo CSV y crea los valores que se van a agregar
    a los campos data y dataNumpy
    """
    csv_file = form.cleaned_data['data']#Toma el archivo que se envia del form
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'El archivo no tiene la extensión .csv necesaria')
    data_set = csv_file.read().decode('UTF-8') #lee el archivo
    io_string = io.StringIO(data_set) #se convierte a un IOString
    numpyMatrix = np.genfromtxt(io_string, delimiter=",") #Convierto a numpy
    numpyMatrixBase64 = castByteToBase64(numpyMatrix)
    numpyMatrixString = castNumpyToStringDB(numpyMatrix)#Para almacenar en data que es txt
    return numpyMatrixBase64, numpyMatrixString




def creacionPeso(sim,matriz,nombre,cod,peso):
    """
    Crea el método asegurandose que si ya existe, lo actualice
    """

    metodo = MetPesoObj(
        nombre = nombre,
        codigo = cod,
        valor_peso = peso
    )
    metodo.save()
    sim.metPesoObjs.add(metodo)
    matriz.metPesoObjs.add(metodo)


#
def crear_matricesBD(request,form,id_sim,usa_man,id_mat=0):
    """
    Cuando llamo esta funcion y no paso valor a id_mat
    Significa que estoy creando una matriz nueva
    Si id_mat trae valor, significa que voy a editar una matriz
    Crea la matriz y la retorna para añadir a BD
    """
    sim = Simulacion.objects.get(id=id_sim)#Toma la Simulacion
    #PRoceso para tomar el archivo csv y convertirlo en buenos datos

    #CREACION MATRIX NUMPY
    dataValid = True if 'data' in form.fields  else False #SI ESTOY UTILIZANDO DATA O NO
    numpyMatrixBase64, numpyMatrixString = 0,0
    if dataValid:
        numpyMatrixBase64, numpyMatrixString = getMatricesBase64String(form,request)


    if id_mat:
        try:
            matriz = Matriz.objects.get(id=id_mat)
        except Matriz.DoesNotExist:
            matriz = Matriz()
    else:
        matriz = form.instance


    if dataValid:
        matriz.data = numpyMatrixString
        matriz.dataNumpy = numpyMatrixBase64
    matriz.nombre = form.cleaned_data["nombre"]
    matriz.signoFOChar = form.cleaned_data["signoFOChar"]
    matriz.isReindexMatriz = form.cleaned_data["isReindexMatriz"]
    matriz.tipoMatriz = form.cleaned_data["tipoMatriz"]


    #Guardar la matriz en la BD
    matriz.save()
    #SIEMPRE SE CREA EL METODO DE LA MATRIZ DIST
    #LOS OTROS METODOS SE CREAN CUANDO SE USA MAN
    if matriz.isMatrizDistance:
        if matriz.metPesoObjs.filter(codigo='DIST').exists():
            #SI YA EXISTE UN METODO DIST, NO HAGA NADA
            pass
        else:
            #DE LO CONTRARIO CREE EL METODO DE DISTANCIA
            creacionPeso(sim, matriz,NOMBRE_MET_DIST,CODIGO_MET_DIST,peso=1.0)

    else:
        if usa_man:
            peso = form.cleaned_data['valorPeso']

            if matriz.metPesoObjs.filter(codigo='MAN').exists():
                #SI YA EXISTE EL METODO, ACTUALICE EL VALOR DEL PESO
                metodo = matriz.metPesoObjs.filter(codigo='MAN')[0]
                metodo.valor_peso = peso
                metodo.save()

            else:
                #SI NO EXISTE EL METODO, CREELO
                creacionPeso(sim, matriz,NOMBRE_MET_MAN,CODIGO_MET_MAN,peso)

    #Añadir la matriz a la simulacion
    sim.matrices.add(matriz)

@login_required
def subir_matrices(request,id,num_mats,usa_man,matriz_size):
    """
    Recibe las matrices de los forms para crearlas en RAM
    """
    id_sim = id
    #si usa metodo manual ?
    usa_man = True if usa_man == 'True' else False

    MatrizFormSetPeso = modelformset_factory (Matriz, form=MatrizFormPesoData, extra=num_mats)
    MatrizFormSetNoPeso = modelformset_factory(Matriz, form=MatrizFormNoPesoData, extra=num_mats)
    template='subir_matriz.html'
    if request.method == 'GET':
        if usa_man:
            formset = MatrizFormSetPeso(queryset=Matriz.objects.none(), initial=[{'nombre':'Distancia', 'isReindexMatriz': 1, 'isMatrizDistance': 1,'tipoMatriz': 'Distancia'}])
            # formset = MatrizFormSetPeso(initial = inicial)
            context = {'formset':formset}
            return render(request,template,context)
        else:
            formset = MatrizFormSetNoPeso(queryset=Matriz.objects.none(),  initial=[{'nombre':'Distancia', 'isReindexMatriz': 1, 'isMatrizDistance': 1,'tipoMatriz': 'Distancia'}])
            # formset = MatrizFormSetNoPeso(initial = inicial)
            context = {'formset':formset}
            return render(request,template,context)
    elif request.method == 'POST':
        if usa_man:
            # check if it's valid:
            formset = MatrizFormSetPeso(request.POST, request.FILES)
            if formset.is_valid():
                for form in formset:
                    #Tomar las matrices y los pesos
                    crear_matricesBD(request,form,id_sim,usa_man)
                return redirect('validar_sim',id_sim)
        else:
            formset = MatrizFormSetNoPeso(request.POST, request.FILES)
            if formset.is_valid():
                for form in formset:
                    crear_matricesBD(request,form,id_sim,usa_man)
                return redirect('validar_sim',id_sim)

#
def obtenerPesos(cod,idsMatrices):
    """
    Retorna los pesos de acuerdo al cod que se pasa
    matrices: numpy array
             Matrices ordenadas en un array
    cod: 'MAN'
         'GMWM'
         'SDWM'
         'CRITICM'

    """
    #CORRECCIÓN A SI HAY UN PESO CON ESE COD EN LA MATRIZ
    # idsMatrices = [matrix.id for matrix in matrices]
    valorPesosMatrices = []
    for ID in idsMatrices:
        matrix = Matriz.objects.get(id=ID)
        if matrix.isMatrizDistance:
            valorPesosMatrices.append(1.0)

        elif matrix.metPesoObjs.filter(codigo=cod).exists():
            #Si la matriz tiene ese método, agreguelo al final de la lista

            valorPeso = matrix.metPesoObjs.filter(codigo=cod).values("valor_peso")
            valorPesosMatrices.append(valorPeso[0].get('valor_peso'))
        else:
            valorPesosMatrices.append(0.0)
    existenPesos = True if valorPesosMatrices[0] else False
    return valorPesosMatrices, existenPesos


def validar_sim(request, id_sim):
    """
    Muestra los datos de la simulacion antes de
    calcular los pesos objetivos
    """
    #obtiene todos los datos de cada simulacion que recibio por el parametro id_sim
    sim = Simulacion.objects.get(id=id_sim)
    matrices = sim.matrices.all()

    context = alistarDatosMostrarSim(sim,matrices,True)


    return render(request,'validar_sim.html',context)



def alistarDatosMostrarSim(sim,matrices,es_val_sim=True):
    """
    Recibe un queryset de sim y matrices y devuelve el contexto para mostrar
    pesos: boolean,
        me dice si voy a querer los datos con pesos de todos los métodos objetivos
        o con solo los pesos manuales
        es_val_sim=True: Si es True, estoy validando la simulación, por lo tanto,
                         No muestro ningún peso
        es_val_sim=False: Estoy validando los pesos
    """
    matricesArray = np.asarray([matrix for matrix in matrices])#convierto las matrices que obtuve para ordenarlas
    matricesOrdenadas = ordenarMatsDistFlujo(matricesArray)
    id_sim =sim.id
    #SE OBTIENE SOLO LA DATA PARA CONVERTIRLAS EN NUMPY MATRIXES
    dataMatrices_np = np.asarray([matrix.getNumpyMatrix() for matrix in matricesOrdenadas])
    num_mats = sim.cantidad_matrices
    matriz_size = sim.no_instalaciones
    usa_man = sim.met_manual
    metodosUsados = sim.getMetodosUsados()
    soloMan = True if metodosUsados[0] and not metodosUsados[1] and not metodosUsados[2] and not metodosUsados[3] else False
    metodosUsadosString, _ = sim.convertirMetUsadosString(metodosUsados)
    nombresMatrices = [matrix.nombre for matrix in matricesOrdenadas]
    matricesRender = [matrix.tolist() for matrix in dataMatrices_np]
    signosMatrices = [matrix.signoFOChar for matrix in matricesOrdenadas]
    tiposMatrices = [matrix.tipoMatriz for matrix in matricesOrdenadas]
    reindexesMatrices = ['Si' if matrix.isReindexMatriz else 'No' for matrix in matricesOrdenadas]
    idsMatrices = [matrix.id for matrix in matricesOrdenadas]
    valorPesosManuales, existenMAN = obtenerPesos(CODIGO_MET_MAN,idsMatrices)
    checkPesosManuales = False
    if existenMAN:
        if valorPesosManuales[1]:
            checkPesosManuales = True

    if es_val_sim:
        datos = list(zip(
            idsMatrices,
            nombresMatrices,
            matricesRender,
            signosMatrices,
            tiposMatrices,
            reindexesMatrices,
            valorPesosManuales,

        ))
        context = {
            'sim': sim,
            'usa_man':usa_man,
            'metodosUsadosString': metodosUsadosString,
            'resultados':datos,
            'num_mats':num_mats,
            'matriz_size':matriz_size,
            'id_sim':id_sim,
            'es_val_sim':es_val_sim,
            'soloMan':soloMan,
            'checkPesosManuales':checkPesosManuales,



        }
        return context

    else:
        valorPesosSDWM, existenSDWM = obtenerPesos(CODIGO_MET_SDWM,idsMatrices)
        valorPesosGMWM, existenGMWM = obtenerPesos(CODIGO_MET_GMWM,idsMatrices)
        valorPesosCRITICM, existenCRITICM = obtenerPesos(CODIGO_MET_CRITICM,idsMatrices)

        checkPesosSDWM = False
        checkPesosGMWM = False
        checkPesosCRITICM = False


        if existenSDWM:
            if valorPesosSDWM[1]:
                checkPesosSDWM = True
        if existenGMWM:
            if valorPesosGMWM[1]:
                checkPesosGMWM = True
        if existenCRITICM:
            if valorPesosCRITICM[1]:
                checkPesosCRITICM = True

        datos = list(zip(
            idsMatrices,
            nombresMatrices,
            matricesRender,
            signosMatrices,
            tiposMatrices,
            reindexesMatrices,
            valorPesosManuales,
            valorPesosSDWM,
            valorPesosGMWM,
            valorPesosCRITICM
            ))

        context = {
            'sim': sim,
            'usa_man':usa_man,
            'resultados':datos,
            'num_mats':num_mats,
            'matriz_size':matriz_size,
            'id_sim':id_sim,
            'checkPesosManuales':checkPesosManuales,
            'checkPesosSDWM':checkPesosSDWM,
            'checkPesosGMWM':checkPesosGMWM,
            'checkPesosCRITICM':checkPesosCRITICM,
            'es_val_sim':es_val_sim,
            'soloMan':soloMan,


        }

        return context


def validar_pesos(request, id_sim):

    sim = Simulacion.objects.get(id=id_sim)
    matrices = sim.matrices.all()

    context = alistarDatosMostrarSim(sim,matrices,False)


    return render(request,'validar_pesos.html',context)

@login_required
def editar_sim(request,id_sim):
    try:
        sim = Simulacion.objects.get(id=id_sim)
    except Simulacion.DoesNotExist:
        return redirect('inicio')
    template = 'nueva_sim.html'
    sim_old = copy.deepcopy(sim)
    if request.method == 'POST':

        num_mats_old = sim.cantidad_matrices
        usa_man_old = sim.met_manual
        metodosUsados_old = sim.getMetodosUsados()
        no_instalaciones_old = sim.no_instalaciones
        form = SimulacionForm(request.POST or None, instance = sim)
        if form.is_valid():
            #NUEVOS PARAMETROS SENSIBLES
            #SI HAY CAMBIOS EN ALGUNOS DE ELLOS, REDIRIJA
            #editar_matrices, SINO REDIRIJA  validar_sim
            matriz_size = form.cleaned_data.get("no_instalaciones")
            num_mats = form.cleaned_data.get("cantidad_matrices")
            usa_man = form.cleaned_data.get("met_manual")
            form.save()
            sim_new= Simulacion.objects.get(id=id_sim)
            valid_sims = sim_old.__eq__(sim_new)
            if valid_sims:
                print(f'No ha realizado cambios en la simulación {sim_new.nombre}')
                print('Será redirigido a la ventana de validación de datos')

                return redirect('validar_sim',id_sim)
            else:

                metodosUsados_new = sim_new.getMetodosUsados()

                #SI ANTES SE USABA GMWM, SDWM O CRITICM Y EN LA EDICIÓN
                #YA NO SE USA, BORRE ESOS METODOS

                cambiosMetodos = metodosUsados_old != metodosUsados_new


                noInstValid = no_instalaciones_old != matriz_size #tamamños de matrices
                numMatsValid = num_mats_old != num_mats
                usaManValid = usa_man_old != usa_man
                validMatrices =  numMatsValid or noInstValid


                # if validMatrices and not usaManValid:
                validMetodos = any(cambiosMetodos)#Si alguno es true, entonces alguno cambió
                metsSinMan = cambiosMetodos[1:]
                validMetsSinMan = not any(metsSinMan) #True si ninguno cambió



                if usaManValid and  validMetsSinMan and not validMatrices:
                    #FIXME: ERROR CUANDO CAMBIA SOLO MAN
                    #SI SOLO MAN CAMBIA Y EL RESTO PERMANECE CONSTANTE
                    #LOS DOS SIGUIENTES CASOS SON PARA CUANDO SOLO
                    #SE EDITA EL usa_man Y NO SE CAMBIA NINGUNO
                    #DE LOS OTROS DOS PARAMETROS SENSIBLES
                    if usa_man_old and not usa_man:
                        #CASO UTILIZABA MANUAL, AHORA NO
                        #SI SOLO ELIMINO EL METODO MANAUL,
                        #ELIMINE LOS METODOS MANUALES Y REDIRIJA A VALIDAR PESOS
                        print('Ha eliminado el método manual')
                        print('Debe volver a obtener los pesos de los métodos selccionados')
                        metodos = metodos = sim_new.metPesoObjs.filter(codigo='MAN')
                        metodos.delete()
                        return redirect('validar_sim',id_sim)
                    elif not usa_man_old and usa_man:
                        #CASO NO UTILIZABA MANUAL, AHORA SI
                        print('Ha decidido utilizar los pesos manuales')
                        print('Deberá crear los pesos y luego volver a obtener los pesos')
                        print('De los otros métodos')

                        return redirect('editar_mats_no_data',id_sim)

                if validMetodos and not validMatrices:
                    #SI SOLO HACE CAMBIOS EN LOS METODOS Y NO EN LAS MATRICES

                    #SI HACE CAMBIO EN EL METODO
                    #DE TRUE A FALSE
                    eliminados = []
                    if metodosUsados_old[0] and not metodosUsados_new[0]:
                        metodos  = sim_new.metPesoObjs.filter(codigo='MAN')
                        eliminados.append('MANUAL')
                        metodos.delete()
                    if metodosUsados_old[1] and not metodosUsados_new[1]:
                        metodos  = sim_new.metPesoObjs.filter(codigo='GMWM')
                        eliminados.append('GMWM')
                        metodos.delete()
                    if metodosUsados_old[2] and not metodosUsados_new[2]:
                        metodos  = sim_new.metPesoObjs.filter(codigo='SDWM')
                        eliminados.append('SDWM')
                        metodos.delete()
                    if metodosUsados_old[3] and not metodosUsados_new[3]:
                        metodos  = sim_new.metPesoObjs.filter(codigo='CRITICM')
                        eliminados.append('CRITICM')
                        metodos.delete()
                    if eliminados:
                        print('Ha eliminado los siguientes métodos')
                        for metodo in eliminados:
                            print(metodo)
                    print('Ha cambiado los métodos a utilizar')
                    print('Debe volver a obtener los pesos')
                    if not usa_man_old and usa_man:
                        #CASO NO UTILIZABA MANUAL, AHORA SI

                        print('Ha decidio utilizar el método manual')
                        print('Por favor ingrese los valores de los pesos de cada matriz')
                        return redirect('editar_mats_no_data',id_sim)

                    #SI CAMBIA LOS METODOS DE FALSE A TRUE,
                    #TAN SOLO DEBE REDIRIGIR A VALIDAR SIM Y VOLVER A OBTENER
                    #LOS PESOS


                    return redirect('validar_sim',id_sim)


                if (validMatrices and validMetodos) or validMatrices:
                    print('Tenga en cuenta que si cambió el número de instalaciones')
                    print('debe volver a incluir los archivos CSV de las matrices')



                    #Revisar si solo cambió noInstalaciones o noMats


                    #de eliminar
                    #SI HACE CAMBIOS EN LAS MATRICES SOLAS,
                    #O CAMBIOS EN LAS MATRICES Y LA SIMULACIÓN
                    # if validMatrices and not usaManValid:
                    #     print('A pesar que no cambió usar el método Manual')
                    #     print('Debe volver a ingresa los valores manuales de cada Matriz')
                    #     print('Porque ha decidido cambiar las matrices, además, ')

                    if (num_mats_old > num_mats) and not noInstValid:
                        #si no_mats_old > no_mats_new es el unico que cambia de esa forma
                        #deberia dirigirse a editar matrices sin data dandole la opción
                        return redirect('editar_mats_no_data',id_sim)
                    if (num_mats_old > num_mats) and (not usa_man_old and usa_man) and not noInstValid:
                        print('Por favor escoja las matrices a eliminar e')
                        print('Ingrese el valor de los pesos de las matrices que quedan')
                    # if (no_mats_old > no_mats_new) and usa_man_old=False and usa_man_new =True

                    # if (num_mats_old < num_mats) and not noInstValid:
                    #     print('Ingrese las nuevas matrices por favor')
                    if (num_mats_old < num_mats) and not noInstValid and (not usa_man_old and usa_man):
                        #CASO 12
                        #AQUI DEBE MOSTRAR LAS num_mats NUEVAS MATRICES CON DATA Y ESPACIO PARA MAN
                        #JUNTO A LAS num_mats_old VIEJAS MATRICES
                        print('Debe ingresar todos los datos de las nuevas matrices')
                        print('E Incluir los archivos de las matrices antiguas')
                        return redirect('editar_matrices_mostrar_todo',id_sim,num_mats,usa_man,matriz_size)


                    if noInstValid:
                        #DEBO MOSTRAR TODAS LAS MATRICES SIN IMPORTAR NADA
                        return redirect('editar_matrices_mostrar_todo',id_sim,num_mats,usa_man,matriz_size)

                    print(f'Ha realizado cambios en las matrices de la simulación')
                    print('Por favor  ingrese los cambios deseados')
                    print('y obtenga los pesos objetivos')
                    return redirect('editar_matrices',id_sim,num_mats,usa_man,matriz_size)

                else:
                    #AQUI ENTRA SI HACE CAMBIOS EN LAMBDA 1, LAMBDA 2,
                    #NO. DE ITERACIONES Y NOMBRE DE LA SIMULACIÓN
                    print(f'Ha realizado cambios en parámetros que no afectan')
                    print('El cálculo de pesos objetivos')
                    print('Será dirigido a Validar Datos de Simulación')


                    return redirect('validar_sim',id_sim)


    else:
        # GET, generate unbound (blank) form
        form = SimulacionForm(instance = sim)
        context = {'form':form}
        return render(request,template,context)


def llenar_form_pesos_man(form):
    """
    Toma el form de un formset para mostrar el peso
    en la casilla del peso manual cuando se quiere
    editar la matriz
    """
    #OBTENGO LOS PESOS PARA PODERLOS MOSTRAR SI YA EXSTEN

    id_matriz = form.instance.id
    if Matriz.objects.filter(id=id_matriz).exists():
        matrix = Matriz.objects.get(id=id_matriz)
        if matrix.metPesoObjs.filter(codigo='DIST').exists():
            form.initial['valorPeso']= 1.0
        elif matrix.metPesoObjs.filter(codigo='MAN').exists():
            valorPeso = matrix.metPesoObjs.filter(codigo='MAN').values("valor_peso")
            peso = valorPeso[0].get('valor_peso')
            form.initial['valorPeso']= peso
        else:
            form.initial['valorPeso']= 0.0

@login_required
def editar_matrices_mostrar_todo(request,id_sim,num_mats,usa_man,matriz_size):
    """
    Edita las matrices cuando vienen de editar la simulación

    """
    #num_mats llega como el nuevo numero de matrices
    try:
        sim = Simulacion.objects.get(id=id_sim)
        matrices = sim.matrices.all()

    except Simulacion.DoesNotExist:
        return redirect('inicio')
    usa_man = True if usa_man == 'True' else False
    no_mats_old = matrices.count()
    dif_mats = no_mats_old - num_mats
    extra_mats=0
    eliminar_matrices = False
    if dif_mats>0:
        #COMO no_mats_old > num_mats
        #DEBO MOSTRARLE AL USUARIO CUAL MATRIZ QUIERE ELIMINAR
        #ESTO SE HACE CON EL can_delete del FORMSET
        eliminar_matrices = True

    elif dif_mats<0:
        #COMO no_mats_old < num_mats
        #MUESTRO LAS QUE YA TENGO Y HAGO
        #QUE SE MUESTREN MAS FORM COMO EXCEDENTE
        #EL EXCEDENTE ES LA DIF*-1
        extra_mats = dif_mats*-1



    #SI dif_mats=0 NO DEBO HACER NADA, PORQUE VOY A TENER POR DEFECTO
    #extra_mats=0 y además, en matrices se tiene las matrices
    #que se venian, en este caso no se pretende cambiar la cantidad
    #de mats, solo otros valores
    if eliminar_matrices:
        MatrizFormSetPeso = modelformset_factory (Matriz, form=MatrizFormPesoData, extra=extra_mats, can_delete=True)
        MatrizFormSetNoPeso = modelformset_factory(Matriz, form=MatrizFormNoPesoData, extra=extra_mats, can_delete=True)


    else:
        MatrizFormSetPeso = modelformset_factory (Matriz, form=MatrizFormPesoData, extra=extra_mats)
        MatrizFormSetNoPeso = modelformset_factory(Matriz, form=MatrizFormNoPesoData, extra=extra_mats)

    template='subir_matriz.html'
    if request.method == 'GET':
        if usa_man:
            formset = MatrizFormSetPeso(queryset=matrices)
            for form in formset.forms:
                #OBTENGO LOS PESOS PARA PODERLOS MOSTRAR SI YA EXSTEN
                llenar_form_pesos_man(form)
        else:
            formset = MatrizFormSetNoPeso(queryset=matrices)
            # print('Ingrese las matrices adicionales')
        context = {'formset':formset}
        # if eliminarMatrices:
        #     matrices.delete()
        return render(request,template,context)
    if request.method == 'POST':
        if usa_man:
            # check if it's valid:
            formset = MatrizFormSetPeso(request.POST, request.FILES)
            validacion = formset.is_valid()
            if validacion:
                #SI EL FORMSET ES VALIDO, ELIMINE TODOS LOS METODOS YA CREADOS
                #EN LA SIM Y ADEMÁS, ELIMINE LAS MATRICES SI POR SI ACASO PASÓ
                #POR EL CASO EN QUE NO HAY CAMBIOS EN LAS MATRICES O
                # dif_mats<0

                #SI NO ESTOY AGREGANDO NUEVAS MATRICES
                #NO BORRE LAS OTRAS MATRICES
                if sim.metPesoObjs.all().exists():
                    metodos = sim.metPesoObjs.all()
                    # metodos = sim.metPesoObjs.filter(codigo='MAN')

                    metodos.delete()
                matrices.delete()
                # if sim.metPesoObjs.all().exists():
                #     metodos = sim.metPesoObjs.all()
                #     # metodos = sim.metPesoObjs.filter(codigo='MAN')

                #     metodos.delete()
                # matrices.delete()
                # formset.save()#Para que pueda eliminar la matriz que el user envió

                if eliminar_matrices:
                    #COMO ELIMINÓ LAS MATRICES QUE ESCOGIÓ EL USER
                    #AHORA DEBE VOLVER A CREAR LAS QUE YA QUEDARON
                    #FIXME: CUANDO SOLO CAMBIA COMO SOLO SE

                    no_forms = formset.total_form_count()
                    no_deleted_forms = len(formset.deleted_forms)
                    no_forms_final = no_forms - no_deleted_forms
                    if no_forms_final == num_mats:
                        for form in formset:
                            if form not in formset.deleted_forms:
                                crear_matricesBD(request,form,id_sim,usa_man)
                        return redirect('validar_sim',id_sim)
                    else:
                        print('No coincide la cantidad de matrices con las que acabó de cargar')
                        print('Vuelva a intentarlo')
                        return redirect('editar_matrices',id_sim,num_mats,usa_man,matriz_size)
                else:
                    #AQUI ENTRA CUANDO CAMBIO EL NO DE INSTALACIONES
                    #AQUI TAMBIÉN ENTRA CUANDO INTENTO AÑADIR NUEVAS MATRICES
                    #TODO: DEBERIA ELIMINAR LOS METODOS ANTES DE ENTRAR AQUÍ
                    for form in formset:
                        crear_matricesBD(request,form,id_sim,usa_man)
                    return redirect('validar_sim',id_sim)


            else:
                context ={
                  'errores' : formset.errors,
                }
                return render(request,template,context)
        else:
            formset = MatrizFormSetNoPeso(request.POST, request.FILES)
            validacion = formset.is_valid()
            if validacion:

                if sim.metPesoObjs.all().exists():
                    #SI NO ESTOY AGREGANDO NUEVAS MATRICES
                    #NO BORRE LAS OTRAS MATRICES
                        if sim.metPesoObjs.all().exists():
                            metodos = sim.metPesoObjs.all()
                            # metodos = sim.metPesoObjs.filter(codigo='MAN')

                            metodos.delete()
                matrices.delete()
                #     metodos = sim.metPesoObjs.all()
                #     # metodos = sim.metPesoObjs.filter(codigo='MAN')
                #     metodos.delete()
                # matrices.delete()
                # # formset.save()#Para que pueda eliminar la matriz que el user envió

                if eliminar_matrices:
                    no_forms = formset.total_form_count()
                    no_deleted_forms = len(formset.deleted_forms)
                    no_forms_final = no_forms - no_deleted_forms
                    if no_forms_final == num_mats:
                        for form in formset:
                            if form not in formset.deleted_forms:
                                crear_matricesBD(request,form,id_sim,usa_man)
                        return redirect('validar_sim',id_sim)
                    else:
                        print('No coincide la cantidad de matrices con las que acabó de cargar')
                        print('Vuelva a intentarlo')
                        return redirect('editar_matrices',id_sim,num_mats,usa_man,matriz_size)
                else:
                    for form in formset:
                        crear_matricesBD(request,form,id_sim,usa_man)
                    return redirect('validar_sim',id_sim)
            else:
                context ={
                  'errores' : formset.errors,
                }
                return render(request,template,context)



@login_required
def editar_matrices(request,id_sim,num_mats,usa_man,matriz_size):
    """
    Edita las matrices cuando vienen de editar la simulación

    """
    #num_mats llega como el nuevo numero de matrices
    try:
        sim = Simulacion.objects.get(id=id_sim)
        matrices = sim.matrices.all()

    except Simulacion.DoesNotExist:
        return redirect('inicio')
    usa_man = True if usa_man == 'True' else False
    no_mats_old = matrices.count()
    dif_mats = no_mats_old - num_mats
    extra_mats=0
    eliminar_matrices = False
    dif_mats_flag = False
    if dif_mats>0:
        #COMO no_mats_old > num_mats
        #DEBO MOSTRARLE AL USUARIO CUAL MATRIZ QUIERE ELIMINAR
        #ESTO SE HACE CON EL can_delete del FORMSET
        eliminar_matrices = True

    elif dif_mats<0:
        #COMO no_mats_old < num_mats
        #MUESTRO LAS QUE YA TENGO Y HAGO
        #QUE SE MUESTREN MAS FORM COMO EXCEDENTE
        #EL EXCEDENTE ES LA DIF*-1
        extra_mats = dif_mats*-1
        dif_mats_flag = True #SI ES VERDAD SOLO MUESTRE LOS ESPACIOS PARA LAS NUEVAS MATRICES QUE QUIERE
        matrices = Matriz.objects.none()


    #SI dif_mats=0 NO DEBO HACER NADA, PORQUE VOY A TENER POR DEFECTO
    #extra_mats=0 y además, en matrices se tiene las matrices
    #que se venian, en este caso no se pretende cambiar la cantidad
    #de mats, solo otros valores
    if eliminar_matrices:
        MatrizFormSetPeso = modelformset_factory (Matriz, form=MatrizFormPesoData, extra=extra_mats, can_delete=True)
        MatrizFormSetNoPeso = modelformset_factory(Matriz, form=MatrizFormNoPesoData, extra=extra_mats, can_delete=True)


    else:
        MatrizFormSetPeso = modelformset_factory (Matriz, form=MatrizFormPesoData, extra=extra_mats)
        MatrizFormSetNoPeso = modelformset_factory(Matriz, form=MatrizFormNoPesoData, extra=extra_mats)

    template='subir_matriz.html'
    if request.method == 'GET':
        if usa_man:
            formset = MatrizFormSetPeso(queryset=matrices)
            for form in formset.forms:
                #OBTENGO LOS PESOS PARA PODERLOS MOSTRAR SI YA EXSTEN
                llenar_form_pesos_man(form)
        else:
            formset = MatrizFormSetNoPeso(queryset=matrices)
            # print('Ingrese las matrices adicionales')
        context = {'formset':formset}
        # if eliminarMatrices:
        #     matrices.delete()
        return render(request,template,context)
    if request.method == 'POST':
        if usa_man:
            # check if it's valid:
            formset = MatrizFormSetPeso(request.POST, request.FILES)
            validacion = formset.is_valid()
            if validacion:
                #SI EL FORMSET ES VALIDO, ELIMINE TODOS LOS METODOS YA CREADOS
                #EN LA SIM Y ADEMÁS, ELIMINE LAS MATRICES SI POR SI ACASO PASÓ
                #POR EL CASO EN QUE NO HAY CAMBIOS EN LAS MATRICES O
                # dif_mats<0
                if not dif_mats_flag:
                    #SI NO ESTOY AGREGANDO NUEVAS MATRICES
                    #NO BORRE LAS OTRAS MATRICES
                    if sim.metPesoObjs.all().exists():
                        metodos = sim.metPesoObjs.all()
                        # metodos = sim.metPesoObjs.filter(codigo='MAN')

                        metodos.delete()
                    matrices.delete()
                # if sim.metPesoObjs.all().exists():
                #     metodos = sim.metPesoObjs.all()
                #     # metodos = sim.metPesoObjs.filter(codigo='MAN')

                #     metodos.delete()
                # matrices.delete()
                # formset.save()#Para que pueda eliminar la matriz que el user envió

                if eliminar_matrices:
                    #COMO ELIMINÓ LAS MATRICES QUE ESCOGIÓ EL USER
                    #AHORA DEBE VOLVER A CREAR LAS QUE YA QUEDARON
                    #FIXME: CUANDO SOLO CAMBIA COMO SOLO SE

                    no_forms = formset.total_form_count()
                    no_deleted_forms = len(formset.deleted_forms)
                    no_forms_final = no_forms - no_deleted_forms
                    if no_forms_final == num_mats:
                        for form in formset:
                            if form not in formset.deleted_forms:
                                crear_matricesBD(request,form,id_sim,usa_man)
                        return redirect('validar_sim',id_sim)
                    else:
                        print('No coincide la cantidad de matrices con las que acabó de cargar')
                        print('Vuelva a intentarlo')
                        return redirect('editar_matrices',id_sim,num_mats,usa_man,matriz_size)
                else:
                    #AQUI ENTRA CUANDO CAMBIO EL NO DE INSTALACIONES
                    #AQUI TAMBIÉN ENTRA CUANDO INTENTO AÑADIR NUEVAS MATRICES
                    #TODO: DEBERIA ELIMINAR LOS METODOS ANTES DE ENTRAR AQUÍ
                    for form in formset:
                        crear_matricesBD(request,form,id_sim,usa_man)
                    return redirect('validar_sim',id_sim)


            else:
                context ={
                  'errores' : formset.errors,
                }
                return render(request,template,context)
        else:
            formset = MatrizFormSetNoPeso(request.POST, request.FILES)
            validacion = formset.is_valid()
            if validacion:
                if not dif_mats_flag:
                    if sim.metPesoObjs.all().exists():
                        #SI NO ESTOY AGREGANDO NUEVAS MATRICES
                        #NO BORRE LAS OTRAS MATRICES
                            if sim.metPesoObjs.all().exists():
                                metodos = sim.metPesoObjs.all()
                                # metodos = sim.metPesoObjs.filter(codigo='MAN')

                                metodos.delete()
                    matrices.delete()
                #     metodos = sim.metPesoObjs.all()
                #     # metodos = sim.metPesoObjs.filter(codigo='MAN')
                #     metodos.delete()
                # matrices.delete()
                # # formset.save()#Para que pueda eliminar la matriz que el user envió

                if eliminar_matrices:
                    no_forms = formset.total_form_count()
                    no_deleted_forms = len(formset.deleted_forms)
                    no_forms_final = no_forms - no_deleted_forms
                    if no_forms_final == num_mats:
                        for form in formset:
                            if form not in formset.deleted_forms:
                                crear_matricesBD(request,form,id_sim,usa_man)
                        return redirect('validar_sim',id_sim)
                    else:
                        print('No coincide la cantidad de matrices con las que acabó de cargar')
                        print('Vuelva a intentarlo')
                        return redirect('editar_matrices',id_sim,num_mats,usa_man,matriz_size)
                else:
                    for form in formset:
                        crear_matricesBD(request,form,id_sim,usa_man)
                    return redirect('validar_sim',id_sim)
            else:
                context ={
                  'errores' : formset.errors,
                }
                return render(request,template,context)


@login_required
def editar_matriz(request, id_matriz, id_sim):
    template = 'subir_matriz.html'
    id_sim = id_sim
    try:
        matriz = Matriz.objects.get(id = id_matriz)
        sim = Simulacion.objects.get(id = id_sim)
    except (Matriz.DoesNotExist, Simulacion.DoesNotExist):
        return redirect('inicio')
    usa_man = sim.met_manual
    # usa_man = True if usaMan =='True' else False

    if request.method == 'GET':

        if usa_man:
            form = MatrizFormPesoData(instance = matriz)
            llenar_form_pesos_man(form)
        else:
            form = MatrizFormNoPesoData(instance = matriz)
        context = {'form': form}
        return render(request,template,context)
    if request.method == 'POST':
        if usa_man:
            form = MatrizFormPesoData(request.POST, request.FILES)
            if form.is_valid():
                crear_matricesBD(request,form,id_sim,usa_man,id_mat=id_matriz)
                return redirect('validar_sim',id_sim)
            else:
                context ={
                  'errores' : form.errors,
                }
                return render(request,template,context)
        else:
            form = MatrizFormNoPesoData(request.POST, request.FILES)
            if form.is_valid():
                crear_matricesBD(request,form,id_sim,usa_man,id_mat=id_matriz)
                return redirect('validar_sim',id_sim)

            else:
                context ={
                    'errores' : form.errors,
                }
                return render(request,template,context)




@login_required()
def editar_mats_no_data(request,id_sim):
    """
    Edita las matrices cuando se cumple el único caso
    en que usa_man ha sido cambiado
    usa_man_old = False
    usa_man_new = True
    Se llama no_data porque como es solo el caso
    en el que usa_man ha sido editado en la sim,
    no es necesario volver a pedir el CSV de la matriz
    """
    #TODO: COLOCAR UN MENSAJE CUANDO ENTRA A ESTA PÁGINA
    #QUE DEBE INGRESAR LOS PESOS MANUALES SOLAMENTE
    #O BLOQUEAR EL RESTO DE DATOS
    try:
        sim = Simulacion.objects.get(id=id_sim)
        matrices = sim.matrices.all()
    except Simulacion.DoesNotExist:
        return redirect('inicio')

    no_mats_new = sim.cantidad_matrices
    no_mats_old = matrices.count()
    extra_mats=0#no se cambió ese campo, entonces no necesito nuevas matrices
    dif_mats = no_mats_old - no_mats_new
    extra_mats=0
    dif_mats_flag = False
    usa_man = sim.met_manual
    eliminar_matriz = False

    #  = True if usaMan =='True' else False
    if dif_mats>0:
        #COMO no_mats_old > num_mats
        #DEBO MOSTRARLE AL USUARIO CUAL MATRIZ QUIERE ELIMINAR
        #ESTO SE HACE CON EL can_delete del FORMSET
        eliminar_matriz = True

    elif dif_mats<0:
        #COMO no_mats_old < num_mats
        #MUESTRO LA CANTIDAD DE MATRICES EXCEDENTE
        #PARA QUE LAS INGRESE
        extra_mats = dif_mats*-1
        dif_mats_flag = True #SI ES VERDAD SOL
    if eliminar_matriz:
        #VIENE PARA ELIMINAR
        if usa_man:
            MatrizFormSetPesoNoData = modelformset_factory (Matriz, form=MatrizFormPesoNoData, extra=extra_mats, can_delete=True)
        else:
            MatrizFormSetNoPesoNoData = modelformset_factory (Matriz, form=BaseMatrizForm, extra=extra_mats, can_delete=True)

    else:
        if usa_man:
            MatrizFormSetPesoNoData = modelformset_factory (Matriz, form=MatrizFormPesoNoData, extra=extra_mats)
        else:
            MatrizFormSetNoPesoNoData = modelformset_factory (Matriz, form=BaseMatrizForm, extra=extra_mats)


    template='subir_matriz.html'
    if request.method == 'GET':
        if usa_man:
            formset = MatrizFormSetPesoNoData(queryset=matrices)
            for form in formset.forms:
                #OBTENGO LOS PESOS PARA PODERLOS MOSTRAR SI YA EXSTEN
                llenar_form_pesos_man(form)
        else:
            formset = MatrizFormSetNoPesoNoData(queryset=matrices)

        context = {'formset':formset}
        return render(request,template,context)
    if request.method == 'POST':
        if usa_man:
            formset = MatrizFormSetPesoNoData(request.POST)
        else:
            formset = MatrizFormSetNoPesoNoData(request.POST)

        validacion = formset.is_valid()
        if validacion:
            # formset.save()

            if eliminar_matriz:

                no_forms = formset.total_form_count()
                no_deleted_forms = len(formset.deleted_forms)
                no_forms_final = no_forms - no_deleted_forms

                #NECESITO ELIMINAR SOLO LAS MATRICES QUE VIENEN EN
                #EN EL formset.deleted_forms JUNTO A SUS MÉTODOS
                if no_forms_final == no_mats_new:
                    for form in formset.deleted_forms:
                        #TOMO LOS METODOS DE LAS MATRICES QUE VOY A ELIMINAR
                        matriz = form.instance
                        if matriz.metPesoObjs.all().exists():
                            metodos = matriz.metPesoObjs.all()
                            metodos.delete()
                    formset.save()#CON ESTO ELIMINO LAS INSTANCIAS DE LAS MATRICES PARA ELEMI
                    for form in formset:

                        #POR SI ACASO VUELVA A CREAR LAS MATRICES,
                        #ESTO ES NECESARIO CUANDO VENGO DE NO_MAN A MAN Y
                        #ADEMÁS, CAMBIO DE no_mats_old > no_mats_new
                        #ENTONCES EL USUARIO ESCOGE LA MATRIZ A ELIMINAR
                        #Y ADEMÁS DEBE COLOCAR LOS PESOS MANUALES
                        if form not in formset.deleted_forms:
                            #SE DEBE ELIMINAR LOS METODOS PORQUE SE PUEDE QUEDAR PEGADO ALGUNO
                            matriz = form.instance
                            if matriz.metPesoObjs.all().exists():
                                metodos = matriz.metPesoObjs.all()
                                metodos.delete()
                            crear_matricesBD(request,form,id_sim,usa_man)

                    return redirect('validar_sim',id_sim)
                else:
                    print('No coincide la cantidad de matrices con las que acabó de cargar')
                    print('Vuelva a intentarlo')
                    return redirect('editar_mats_no_data',id_sim)
            else:
                if sim.metPesoObjs.all().exists():
                    metodos = sim.metPesoObjs.all()
                    # metodos = sim.metPesoObjs.filter(codigo='MAN')
                    metodos.delete()
                matrices.delete()
                for form in formset:

                    crear_matricesBD(request,form,id_sim,usa_man)

                    # if form.cleaned_data.get('tipoMatriz') == 'Distancia':
                    #     #SI ES MATRIZ DISTANCIA NO CREE METODO PORQUE
                    #     #YA SE CREÓ AL PRINCIPIO
                    #     pass
                    # else:
                    #     valor_peso = form.cleaned_data.get('valorPeso')
                    #     matriz = form.instance
                    #     creacionPeso(sim, matriz,NOMBRE_MET_MAN,CODIGO_MET_MAN,valor_peso)
            return redirect('validar_sim',id_sim)
        else:
            context ={
                'errores' : formset.errors,
            }
            return render(request,template,context)

            
    #ANTIGUO  
    # if request.method == 'POST':
    #     formset = MatrizFormSetPesoNoData(request.POST)
    #     validacion = formset.is_valid()
    #     if validacion:
    #         formset.save()
    #         for form in formset:
    #             if form.cleaned_data.get('tipoMatriz') == 'Distancia':
    #                 #SI ES MATRIZ DISTANCIA NO CREE METODO PORQUE
    #                 #YA SE CREÓ AL PRINCIPIO
    #                 pass
    #             else:
    #                 valor_peso = form.cleaned_data.get('valorPeso')
    #                 matriz = form.instance
    #                 creacionPeso(sim, matriz,NOMBRE_MET_MAN,CODIGO_MET_MAN,valor_peso)
    #         return redirect('validar_sim',id_sim)
    #     else:
    #         context ={
    #             'errores' : formset.errors,
    #         } 
    #         return render(request,template,context)
        


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

#()
def actualizar_crear_peso(todosPesos, indice, cod, sim, matriz):
    pesos = todosPesos.get(cod)[1]
    valor_peso = pesos[indice]
    metodo_query = matriz.metPesoObjs.filter(codigo=cod)
    if metodo_query.exists():
        metodo = metodo_query[0]
        metodo.valor_peso = valor_peso
        metodo.save()
    else:
        if cod == 'SDWM':
            creacionPeso(sim,matriz,NOMBRE_MET_SDWM,CODIGO_MET_SDWM,valor_peso)
        if cod == 'GMWM':
            creacionPeso(sim,matriz,NOMBRE_MET_GMWM,CODIGO_MET_GMWM,valor_peso)
        if cod == 'CRITICM':
            creacionPeso(sim,matriz,NOMBRE_MET_CRITICM,CODIGO_MET_CRITICM,valor_peso)

#()
def calculos(request, id_sim, pesos):
    """
    Esta función es llamada después de que se
    aprueban las matrices y los parámetros de la simulación
    para calcular los pesos de cada matriz de acuerdo a
    los métodos escogidos en la simulación

    pesos = 1 Si necesito calcular pesos
            0 Si necesito calcular resultados de la metaheurística
    """

    try:
        sim = Simulacion.objects.get(id=id_sim)
        matrices = sim.matrices.all()

    except (Simulacion.DoesNotExist, Matriz.DoesNotExist):
        return redirect('inicio')

    casos_sim = sim.getMetodosUsados()
    casoEntero = binaryListToInt(casos_sim)

    matricesArray = np.asarray([matrix for matrix in matrices])#convierto las matrices que obtuve para ordenarlas
    matricesOrdenadas = ordenarMatsDistFlujo(matricesArray)
    idsMatrices = [matrix.id for matrix in matricesOrdenadas]
    # dataMatrices_np = np.asarray([pickle.loads(base64.b64decode(matrix.dataNumpy)) for matrix in matricesOrdenadas])

    pesosManuales = obtenerPesos('MAN',idsMatrices)[0]
    pesosManuales.pop(0)
    if not pesosManuales[1] and casos_sim[0]:
        #TODO: MOSTRAR MENSAJE ALGO HA OCURRIDO, UD DESEA UTILIZAR
        #PESOS INGRESADOS POR UD MIMSMO (MÉTODO MANUAL)
        #PERO NO EXISTEN PESOS, POR FAVOR, INGRESE LOS VALORES DE LOS PESOS
        #E INTENTE CALCULAR LOS PESOS NUEVAMENTE

        print('ALGO HA OCURRIDO, UD DESEA UTILIZAR ESOS INGRESADOS POR UD MIMSMO (MÉTODO MANUAL)')
        print('PERO NO EXISTEN PESOS, POR FAVOR, INGRESE LOS VALORES DE LOS PESOS')
        print('E INTENTE CALCULAR LOS PESOS NUEVAMENTE')
        # pesosManuales = [0 for matrix in matricesOrdenadas if not matrix.isMatrizDistance]
        return redirect('editar_mats_no_data',id_sim)
    todosPesos = po.caseSelection(matricesOrdenadas, casoEntero, pesosManuales)
    if pesos == 1:
        for indice,ID in enumerate(idsMatrices):
            #Como hay tantos pesos como matrices hay en la simulacion
            #recorro el vector idsMatrices para tomar la matriz
            #y luego crear el método y relacionarlo de una en
            #la tabla M2M

            matriz = Matriz.objects.get(id=ID)#Obtengo la matriz

            if todosPesos.get('MAN'):
                #LOS PESO MANUALES YA ESTÁN CREADOS
                pass

            if todosPesos.get('SDWM'):
                #Tomo los resultados
                #Luego tomo el peso que corresponde al índice de la matriz
                #Esto funciona porque ya tengo las matrices ordenadas
                #en el vector matricesOrdenadas
                if indice != 0:

                    #Si no estoy en el índice de la matriz distancia
                    actualizar_crear_peso(todosPesos, indice, 'SDWM', sim, matriz)


            if todosPesos.get('GMWM'):
                if indice != 0:
                    actualizar_crear_peso(todosPesos, indice, 'GMWM', sim, matriz)



            if todosPesos.get('CRITICM'):
                if indice != 0:
                    actualizar_crear_peso(todosPesos, indice, 'CRITICM', sim, matriz)


        return redirect('validar_pesos',id_sim)
    elif pesos ==0:
        parametros = sim.lambda1, sim.lambda2, sim.iteraciones
        simetria = todosPesos.get('symetria')
        rtadosMAN = []
        rtadosSDWM = []
        rtadosCRITICM = []
        rtadosGMWM = []
        resulManText = []
        resulSdwmext = []
        resulCritiText = []
        resulgmwmText = []
        
        # resulManText = resulManText = funcionResultado(rtados[0][0])
        
        
        if todosPesos.get('MAN'):
            print('============================================')
            print('=====CALCULOS RESULTADOS PESOS MANUALES=====')
            print('============================================')
            print("\n")
            print("\n")

            matrices = todosPesos.get('MAN')[0]

            rtados = sa.recocidoSimulado(parametros,matrices,simetria)

            # print(rtados)
            if(rtados[0]):
                aFOBest = rtados[0]
                valsFOTemps= rtados[1]
                tempInicialFinal = rtados[2]
                print("Mejor solución Abest MANUAL: {} \n".format(aFOBest[0]))
                # f.write("Mejor solución Abest MANUAL: %d\r\n" % aFOBest[0])
                print("Mejor funcion objetivo MANUAL {} \n".format(aFOBest[1]))


            rtadosMAN = {
                'mejorFO' : rtados[0][1],
                'mejorSLN': rtados[0][0],
            }
            resulManText = funcionResultado(rtados[0][0])



        if todosPesos.get('SDWM'):
            print('============================================')
            print('=====CALCULOS RESULTADOS PESOS SDWM=====')
            print('============================================')
            print("\n")
            print("\n")

            matrices = todosPesos.get('SDWM')[0]
            rtados = sa.recocidoSimulado(parametros,matrices,simetria)
            if(rtados[0]):
                aFOBest = rtados[0]
                valsFOTemps= rtados[1]
                tempInicialFinal = rtados[2]
                print("Mejor solución Abest SDWM: {} \n".format(aFOBest[0]))
                print("Mejor funcion objetivo SDWM {} \n".format(aFOBest[1]))
               
            rtadosSDWM = {
                'mejorFO' : rtados[0][1],
                'mejorSLN': rtados[0][0],
            }
            resulSdwmext = funcionResultado(rtados[0][0])
        
            # print(resultados)

        if todosPesos.get('GMWM'):
            print('============================================')
            print('=====CALCULOS RESULTADOS PESOS GMWM=====')
            print('============================================')
            print("\n")
            print("\n")

            matrices = todosPesos.get('GMWM')[0]
            rtados = sa.recocidoSimulado(parametros,matrices,simetria)
            if(rtados[0]):
                aFOBest = rtados[0]
                valsFOTemps= rtados[1]
                tempInicialFinal = rtados[2]
                print("Mejor solución Abest GM: {} \n".format(aFOBest[0]))
                print("Mejor funcion objetivo GM {} \n".format(aFOBest[1]))
               
            else:
                print("No se puede utilizar GMWM")
                print("resultads[1] {}".format(rtados[1]))
                print("\n")
                # print(resultados)
            rtadosGMWM = {
                'mejorFO' : rtados[0][1],
                'mejorSLN': rtados[0][0],
            }
            
            resulgmwmText = funcionResultado(rtados[0][0])
            
        if todosPesos.get('CRITICM'):
            print('============================================')
            print('=====CALCULOS RESULTADOS PESOS CRITICM=====')
            print('============================================')
            print("\n")
            print("\n")

            matrices = todosPesos.get('CRITICM')[0]
            rtados = sa.recocidoSimulado(parametros,matrices,simetria)

            # print(rtados)
            if(rtados[0]):
                aFOBest = rtados[0]
                valsFOTemps= rtados[1]
                tempInicialFinal = rtados[2]
                print("Mejor solución Abest CRITICM: {} \n".format(aFOBest[0]))
                print("Mejor funcion objetivo CRITICM {} \n".format(aFOBest[1]))

            rtadosCRITICM = {
                'mejorFO' : rtados[0][1],
                'mejorSLN': rtados[0][0],
            }
            resulCritiText = funcionResultado(rtados[0][0])
        template = 'mostrar_rtados.html'
        
        cantidad = list(range(1, sim.no_instalaciones + 1))
        
        
        
        context = {
            'id_sim': id_sim,
            'rtados' : 'rtados',
            'rtadosMAN' : rtadosMAN,
            'rtadosSDWM' : rtadosSDWM,
            'rtadosCRITICM' : rtadosCRITICM,
            'rtadosGMWM' : rtadosGMWM,
            'resulManText': resulManText,
            'resulSdwmext': resulSdwmext,
            'resulCritiText': resulCritiText,
            'resulgmwmText': resulgmwmText,
            

        }
        return render(request, template, context)

#funcion para procesar los resultados e imprimirlos en el texto deseando como una lista
def funcionResultado(data):
    result = []
    myContador = 1
    for i in data:
        texto = f'Ubique la instalación {i} en la ubicación {myContador}'
        myContador += 1
        result.append(texto)
    return result


#()
def calculo_rtados_met(request,id_sim):
    template = 'mostrar_rtados.html'
    casos_sim = sim.getMetodosUsados()
    casoEntero = binaryListToInt(casos_sim)
    matricesArray = np.asarray([matrix for matrix in matrices])#convierto las matrices que obtuve para ordenarlas
    matricesOrdenadas = ordenarMatsDistFlujo(matricesArray)
    idsMatrices = [matrix.id for matrix in matricesOrdenadas]

    context = {
        'rtados' : 'rtados'
    }
    return render(request, template, context)


