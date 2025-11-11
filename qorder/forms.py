from django import forms
from django.forms import extras
from django.forms.fields import IntegerField

from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, ButtonHolder, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.bootstrap import TabHolder, Tab
from datetime import date,datetime



class contactoForm(forms.ModelForm):
    class Meta:
        model = ContactoCliente
        fields = '__all__'
        widgets = {
            'notas': forms.Textarea(attrs={'cols': 23, 'rows': 4})
        }

    email_1 = forms.EmailField(required=False)
    email_2 = forms.EmailField(required=False)

    helper = FormHelper()

    helper.layout = Layout(
             Div(
                 Div(
                     Field('cliente', type="hidden"),
                  ),
               Div('nombre', css_class='col-xs-5 '),
               Div('apellido_1', css_class='col-xs-5 col-xs-offset-2'),
               Div('apellido_2', css_class='col-xs-5 '),
               Div('direccion', css_class='col-xs-5 col-xs-offset-2'),
              
               Div('telefono_fijo', css_class='col-xs-5'),
               Div('telefono_movil', css_class='col-xs-5 col-xs-offset-2'),
               Div('email_1', css_class='col-xs-5'),
               Div('email_2', css_class='col-xs-5  col-xs-offset-2'),
               Div('notas', css_class='col-xs-5'),
               css_class='panel-body'
               ))

class clienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields =  ('codigo', 'nombre', 'apellido_1', 'apellido_2','calle','numero_puerta','piso','duplicador','localidad',
                   'municipio','barrio','departamento','codigo_postal','estado_cliente','fecha_alta','observacion')
       
        
        
        widgets = {
            'observacion': forms.Textarea(attrs={'cols': 23, 'rows': 4})
            #'estado_cliente': forms.CheckboxInput(check_test=my_check_test)
         
        }

    fecha_alta = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=('%d/%m/%Y',))

    helper = FormHelper()
    helper.layout = Layout(
             Div(

               Div(Field('codigo', readonly=True), css_class='col-xs-5 '),
               Div('nombre', css_class='col-xs-5 col-xs-offset-2'),
              
               Div('apellido_1', css_class='col-xs-5 '),
               Div('apellido_2', css_class='col-xs-5 col-xs-offset-2'),
               Div('calle', css_class='col-xs-5 '),
               Div('numero_puerta', css_class='col-xs-5 col-xs-offset-2'),
               Div('piso', css_class='col-xs-5 '),
               Div('duplicador', css_class='col-xs-5 col-xs-offset-2'),
               Div('localidad', css_class='col-xs-5 '),
               Div('municipio', css_class='col-xs-5 col-xs-offset-2'),
               Div('barrio', css_class='col-xs-5 '),
               Div('departamento', css_class='col-xs-5 col-xs-offset-2'),
               Div('codigo_postal', css_class='col-xs-5 '),
               
               Div(Field('fecha_alta', readonly=True), css_class='col-xs-5 col-xs-offset-2'),
               Div('estado_cliente', css_class='col-xs-5 '),
               Div('observacion', css_class='col-xs-5 col-xs-offset-2'),
             
               css_class='panel-body'
               ))


class tpFormInactivable(forms.ModelForm):
    class Meta:
        model = TerminalPortatil

        fields = '__all__'
    

    alias = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    oficina = forms.CharField(label='Contratista',widget = forms.TextInput(attrs={'readonly':'readonly'})) 

    helper = FormHelper()

    helper.layout = Layout(
             Div(

               Div('alias', css_class='col-xs-5 '),
               Div('oficina',css_class='col-xs-5 col-xs-offset-2'),
               Div('estado', css_class='col-xs-5 '),
               Div('numero_serie', css_class='col-xs-5 col-xs-offset-2'),              
               Div('email', css_class='col-xs-5 '),
               Div('imei', css_class='col-xs-5 col-xs-offset-2'),
               Div('androidID', css_class='col-xs-5 '),
               Div('num_telefono', css_class='col-xs-5 col-xs-offset-2'),
               css_class='panel-body'
               ))



class tpForm(forms.ModelForm):
    class Meta:
        model = TerminalPortatil

        fields = '__all__'
        
    alias = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))

    helper = FormHelper()

    helper.layout = Layout(
             Div(

               Div('alias', css_class='col-xs-5'),
               Div('oficina',name='contratistas', css_class='col-xs-5 col-xs-offset-2'),
               Div('estado', css_class='col-xs-5 '),
               Div('numero_serie', css_class='col-xs-5 col-xs-offset-2'),                
               Div('email', css_class='col-xs-5 '),
               Div('imei', css_class='col-xs-5 col-xs-offset-2'),
               Div('androidID', css_class='col-xs-5 '),
               Div('num_telefono', css_class='col-xs-5 col-xs-offset-2'),
               css_class='panel-body'
               ))



class codigoForm(forms.ModelForm):
    class Meta:
         model = Codigo
         fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(codigoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            print('instance{}'.format(instance))
            self.fields['codigo'].widget.attrs['readonly'] = True    
    helper = FormHelper()

    helper.layout = Layout(
             Div(
               Div('codigo', css_class='col-xs-5 '),
               Div('descripcion', css_class='col-xs-5 col-xs-offset-2'),
               Div(
                     Field('activo', type="hidden"),
                     Field('prefijo', type="hidden"),
                  ),
               css_class='panel-body'
               ))

class tecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        self.edit = kwargs.pop('edit')
        super(tecnicoForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        print(instance.terminal_portatil)
        if instance and instance.pk:
            self.fields['codigo'].widget.attrs['readonly'] = True
            if self.edit == False:
               self.fields['terminal_portatil'].widget.attrs['disabled'] = True

    def clean_terminal_portatil(self):
      print('clean_terminal_portatil_field')
      instance = getattr(self, 'instance', None)
      if instance and instance.pk:
        print('Instancia self.edit={}'.format(self.edit))
        if self.edit == False:
          return instance.terminal_portatil
        else:
          return self.cleaned_data['terminal_portatil']
      else:
        return self.cleaned_data['terminal_portatil']


    helper = FormHelper()

    helper.layout = Layout(
             Div(
               Div('codigo', css_class='col-xs-5 '),
               Div('legajo', css_class='col-xs-5 col-xs-offset-2'),
               Div('nombre_1', css_class='col-xs-5 '),
               Div('apellido_1', css_class='col-xs-5 col-xs-offset-2'),
               Div('apellido_2', css_class='col-xs-5 '),
               Div('terminal_portatil', css_class='col-xs-5 col-xs-offset-2'),
              
               Div('tipo_personal', css_class='col-xs-5'),
               Div('activo', css_class='col-xs-5 col-xs-offset-2'),
               Div('password', css_class='col-xs-5 '),
               css_class='panel-body'
               ))

class semanaForm(forms.ModelForm):
    class Meta:
        model = SemanaXUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(semanaForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].widget.attrs['readonly'] = True

    helper = FormHelper()

    helper.layout = Layout(
             Div(
                 Div(
                     Field('usuario', type="hidden"),
                 ),

               Div('semana', css_class='col-xs-12')))



class parametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(parametroForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['parametro'].widget.attrs['readonly'] = True

    helper = FormHelper()

    helper.layout = Layout(
             Div(
               Div('parametro', css_class='col-xs-5 '),
               Div('descripcion', css_class='col-xs-5 col-xs-offset-2'),
               Div('valor_1', css_class='col-xs-5 '),
               Div('valor_2', css_class='col-xs-5 col-xs-offset-2'),
               Div('parametro_movil', css_class='col-xs-5 '),
                        css_class='panel-body'
               ))


class anomaliaForm(forms.ModelForm):
    class Meta:
        model = Anomalia

        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(anomaliaForm, self).__init__(*args, **kwargs)
        anomalia = self.fields['tipo_resultado'] #This is a ModelChoiceField

        if self.instance and self.instance.pk:
            self.fields['tipo_resultado'].queryset= \
                Codigo.objects.filter(prefijo='CL' )
            self.fields['id_anomalia'].widget.attrs['readonly'] = True    
        else: 
            self.fields['tipo_resultado'].queryset= \
                Codigo.objects.filter(prefijo='CL' )

    helper = FormHelper()

    helper.layout = Layout(
             Div(

               Div('id_anomalia', css_class='col-xs-5 '),
               Div('descripcion', css_class='col-xs-5 col-xs-offset-2'),
              
               Div('prioridad', css_class='col-xs-5 '),
               Div('tipo_resultado', css_class='col-xs-5 col-xs-offset-2'),
               Div('activo', css_class='col-xs-5 '),
               css_class='panel-body'
               ))

class problemaForm(forms.ModelForm):
    class Meta:
        model = Problema

        fields = ('id_problema', 'descripcion')

    helper = FormHelper()
    helper.layout = Layout(
             Div(

               Div('id_problema', css_class='col-xs-5 '),
               Div('descripcion', css_class='col-xs-5 col-xs-offset-2'),
              
             

               css_class='panel-body'
               ))
def ciclo():
    return '{}{}'.format(datetime.today().year, datetime.today().month)  

def fecha():
    return datetime.date(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)


class generacionForm(forms.Form):
    Ciclo = forms.CharField(max_length=20,initial=ciclo)
    Fecha_estimada = forms.DateField(initial=datetime.today())
    #self.fields['a'].widget.attrs['class'] = 'datepicker'
    def __init__(self, *args, **kwargs):
        super(generacionForm, self).__init__(*args, **kwargs)
        self.fields['Ciclo'].required = False
        self.fields['Fecha_estimada'].required = False
        self.helper = FormHelper()
        self.fields['Fecha_estimada'].widget.attrs['class'] = 'datepicker'
        self.helper.layout = Layout(
                       Div(

               Div('Ciclo', css_class='col-xs-5 '),
               Div('Fecha_estimada', css_class='col-xs-5 col-xs-offset-2'),
              
             

               css_class='panel-body'
               ))
     
        
class encuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta

        fields = ('nombre', 'descripcion')
    def __init__(self, *args, **kwargs):
        super(encuestaForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['nombre'].widget.attrs['readonly'] = True
    helper = FormHelper()
    helper.layout = Layout(
             Div(

               Div('nombre', css_class='col-xs-5 '),
               Div('descripcion', css_class='col-xs-5 col-xs-offset-2'),
              
             

               css_class='panel-body'
               ))

class preguntaForm(forms.ModelForm):
    class Meta:
        model = EncuestaDetalle
        fields = '__all__'
    helper = FormHelper()

    helper.layout = Layout(
             Div(
               Div('titulo', css_class='col-xs-5 '),
               Div('tipo', css_class='col-xs-5 col-xs-offset-2'),
              
               Div('texto_pregunta', css_class='col-xs-12'),
               Div('opciones', css_class='col-xs-12 '),
             
               Div(
                     Field('encuesta', type="hidden"),
                     Field('orden', type="hidden"),
                  ),
               css_class='panel-body'
               ))
  
    
class geofencingForm(forms.ModelForm):
    class Meta:
        model = Geofencing

        fields = ('descripcion',)

    helper = FormHelper()
    helper.layout = Layout(
             Div(
               Div('descripcion'),
               css_class='panel-body'
               ))

class geofencingDetalleForm(forms.ModelForm):
      class Meta:
         model = GeofencingDetalle
         fields = '__all__'
      
      helper = FormHelper()
      helper.form_class = 'form-inline'
      helper.form_tag = False

        
      helper.layout = Layout(
        TabHolder(
            Tab(
                'Notificaciones al entrar',
                 Div('notifica_email_ingreso', style="background: #FAFAFA;"),
                 Div('emails_ingreso', rows="3", css_class='input-xlarge'),
                'mensaje_email_ingreso',
                Div('notifica_ws_ingreso', style="background: #FAFAFA;"),
                'mensaje_ws_ingreso',
                Div('notifica_pantalla_ingreso', style="background: #FAFAFA;"),
                'mensaje_pantalla_ingreso',
                Div('notifica_sonido_ingreso', style="background: #FAFAFA;")
            ),
            Tab(
                'Notificaciones al salir',
                Div('notifica_email_egreso', style="background: #FAFAFA;"),
                'emails_egreso',
                'mensaje_email_egreso',
                Div('notifica_ws_egreso', style="background: #FAFAFA;"),
                'mensaje_ws_egreso',
                Div('notifica_pantalla_egreso', style="background: #FAFAFA;"),
                'mensaje_pantalla_egreso',
                Div('notifica_sonido_egreso', style="background: #FAFAFA;")
            )
          )
      )

      def __init__(self, *args, **kwargs):
        super(geofencingDetalleForm, self).__init__(*args, **kwargs)
        self.fields['notifica_email_ingreso'].label = "Notificar por eMail"
        self.fields['notifica_email_egreso'].label = "Notificar por eMail"
        self.fields['emails_ingreso'].label = "eMails"
        self.fields['emails_egreso'].label = "eMails"

     
class rutasumForm(forms.ModelForm):
    class Meta:
         model = RutaSum
         fields = ('rutasum','itinerario','oficina')

    def __init__(self, *args, **kwargs):
        super(rutasumForm, self).__init__(*args, **kwargs)
        self.fields['rutasum'].label= "Ruta"
        print('llego1')

        instance = getattr(self, 'instance', None)
        print(instance)
        if instance and instance.pk:
            print('instance {}'.format(instance))
            print('aca')
            self.fields['rutasum'].widget.attrs['readonly'] = False     
    helper = FormHelper()

    helper.layout = Layout(
             Div(
               Div('rutasum', css_class='col-xs-5  '),
               Div('itinerario', css_class='col-xs-5 col-xs-offset-2'),
               Div(
                     Field('oficina', type="hidden"),
                  ),
               css_class='panel-body'
               ))

