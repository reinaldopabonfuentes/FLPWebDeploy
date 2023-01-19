"""flpwebProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from flpwebAPP.views import inicio, singin, signup, upload, signout, simulations, restorepassword

from flpwebAPP.views import (
    nueva_sim, subir_matrices, validar_sim,
    editar_matrices, editar_sim, editar_mats_no_data,# crear_pesos, 
    editar_matriz, validar_pesos, editar_matrices_mostrar_todo, calculo_rtados_met, calculos
)

urlpatterns = [
    
    path('subir_matrices/<int:id>/<int:num_mats>/<str:usa_man>/<int:matriz_size>',subir_matrices,name="subir_matrices"),
    path('editar_matrices/<int:id_sim>/<int:num_mats>/<str:usa_man>/<int:matriz_size>', editar_matrices, name='editar_matrices'),
    path('editar_matrices_mostrar_todo/<int:id_sim>/<int:num_mats>/<str:usa_man>/<int:matriz_size>', editar_matrices_mostrar_todo, name='editar_matrices_mostrar_todo'),
    path('validar_sim/<int:id_sim>/', validar_sim, name="validar_sim"),
    path('validar_pesos/<int:id_sim>/', validar_pesos, name="validar_pesos"),
    path('editar_mats_no_data/<int:id_sim>',
    editar_mats_no_data, name="editar_mats_no_data"),
    path('editar_matriz/<int:id_matriz>/<int:id_sim>', editar_matriz, name="editar_matriz"),
    path('editar_sim/<int:id_sim>/', editar_sim, name="editar_sim"),
    path('calculo_rtados_met/<int:id_sim>/', calculo_rtados_met, name="calculo_rtados_met"),
    # path('crear_pesos/<int:id_sim>/', crear_pesos, name="crear_pesos"),
    path('calculos/<int:id_sim>/<int:pesos>', calculos, name="calculos"),

    path('admin/', admin.site.urls),
    
    path('inicio/', inicio, name='inicio'),
    path('', inicio),
    path('singin/', singin, name='singin'), 
    path('restorepassword/', restorepassword, name='restorepassword'), 
    path('signup/', signup, name='signup'), 
    path('logout/', signout, name='logout'),
    path('simulations/', simulations, name='simulations'),
    
    path('upload/', upload, name="upload"),
    # path('download/', download, name="exportar"),
    path('nueva_sim/', nueva_sim, name="nueva_sim"),
    
    # path('pruebaFormset/', pruebaFormset, name="pruebaFormset"),

]
