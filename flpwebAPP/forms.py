from django import forms
from flpwebAPP.models import Matriz, Simulacion


class BaseMatrizForm(forms.ModelForm):

    class Meta:
        model = Matriz
        fields = (
            'nombre',
            'signoFOChar',
            'tipoMatriz',
            'isReindexMatriz',)


# class MatrizFormNoPeso(BaseMatrizForm):
class MatrizFormNoPesoData(BaseMatrizForm):
    data = forms.FileField(label="Archivo CSV de la Matriz")

# NO ES NECESARIO CREAR MatrizFormNoPesoNoData PORQUE
# ES EL MISMO BaseMatrizForm


class MatrizFormPesoData(BaseMatrizForm):
    data = forms.FileField(label="Archivo CSV de la Matriz")
    valorPeso = forms.FloatField(widget=forms.TextInput(attrs={'type': 'number','step':'any', 'onchange':'validateSum(this.value)'}),label="Valor peso de la Matriz",required=False)

    
class MatrizFormPesoNoData(BaseMatrizForm):
    valorPeso = forms.FloatField(label="Valor peso de la Matriz",required=False)


class SimulacionForm(forms.ModelForm):
    met_gmwm = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onclick':'toggleMessage()'}), label="Método Media Geométrica", required=False)
    class Meta:
        model = Simulacion
        fields = (
            'nombre',
            'met_manual',
            'met_gmwm',
            'met_sdwm',
            'met_criticm',
            'no_instalaciones',
            'cantidad_matrices',
            'lambda1',
            'lambda2',
            'iteraciones')
        