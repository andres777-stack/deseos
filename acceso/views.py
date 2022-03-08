from django import forms
from django.shortcuts import render, HttpResponse, redirect
from acceso.forms import UserForm
from django.contrib import messages
from django.urls import reverse
import bcrypt
from acceso.models import User

class LoginForm(forms.Form):

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            self.add_error('password', 'El password debe contener más de 8 caracteres')
        return password

    email = forms.CharField(
        label = 'Email',
        required = True,
        widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder' : 'Correo electrónico'})
    )
    password = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : 'Contraseña'})
    )

def index(request):
    if request.method == 'GET':
        context = {
        'formModel': UserForm(),
        'formLogin': LoginForm(),
        }
        return render(request, 'access/index.html', context)

    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            #hasta aquí sólo se han aplicado las validaciones clean. La contraseña está en texto plano.
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(usuario.password.encode(), bcrypt.gensalt()).decode()
            #Se hashea la contraseña
            usuario.save()
            #Se guarda el usuario con la contraseña hasheada.
            #Mensaje de éxito
            messages.success(request, 'Usuario registrado con éxito')
            return redirect(reverse('acceso:index'))
        else:
            messages.error(request, 'Con errores, solucionar')
            return render(request, 'access/index.html', {'formModel': form})

def login(request):
    if 'usuario' in request.session:
        messages.error(request, 'Ya estás logeado!')
        return redirect(reverse('acceso:index'))
    else:
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid(): #se valida la información que viene del form
            print(form.cleaned_data)
            #aquí en más viene la comprobación de las contraseñas.
            user = User.objects.filter(email=form.cleaned_data['email']).first() #se va a buscar la instancia de usario
            print(user)                                         #Arroja un queryset, por eso no será vacío. 
            if user: #aquí se comprueba si el usuario existe en el queryset user. 
                form_password = form.cleaned_data['password'] #se aloja el password que llegó del form
                print(form_password)
                print(user.password) #si viene en un queryset vamos a tener problemas para acceder.Poner first()
                if bcrypt.checkpw(form_password.encode(), user.password.encode()):
                    request.session['usuario'] = {'nombre' : user.nombre, 'email' : user.email, 'apellido' : user.apellido, 'id': user.id}
                    messages.success(request, 'Contraseñas coinciden!') #si concuerdan, se crea var sesion
                    return redirect(reverse('deseos:index'))
                else: 
                    messages.error(request, 'Contraseñas no coinciden')
            else:
                messages.error(request, 'Usuario no está regitrado en la base de datos')        
            
            return redirect('/')
        else:
            context = {
                'formModel' : UserForm(), #el form de registro se manda vacio.
                'formLogin' : form, #el form de login se manda con los datos para su arreglo
                }
            return render(request, 'access/index.html', context)

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        return redirect(reverse('acceso:index'))

def mientras(request):
    return HttpResponse("hola desde nmientras")