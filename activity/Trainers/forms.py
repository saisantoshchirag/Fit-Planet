from django import forms
from .models import Workouts,Trainerprofile
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.contrib.auth.models import User
from home.models import Video

choices1 = [
    ('bands','bands'),
    ('foamroll','foamroll'),
    ('barbell','barbell'),
    ('dumbbell','dumbbell'),
    ('machine','machine'),
    ('medicineball','medicineball'),
    ('exerciseball','exerciseball'),
    ('curlbar','curlbar'),
    ('kettlebell','kettlebell'),
]
class AddworkoutForm(forms.ModelForm):
    muscle_type = forms
    equipment = forms.ChoiceField(choices=choices1)
    class Meta:
        model=Video
        fields=["video","muscle_type","equipment","image1","image2","name","description"]

class LoginForm(forms.Form):
    username_login=forms.CharField(label='',min_length=1,max_length=150,widget=forms.TextInput(attrs={'placeholder':'username'}))
    password_login = forms.CharField(label='',
                                     widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    def clean(self):
        username=self.cleaned_data['username_login']
        username='_trainer_'+username
        password=self.cleaned_data['password_login']
        print("\nu & p cln : ",username,password)
        user=authenticate(username=username,password=password)
        print("auth user",user)

        if not user or not user.is_active:
            raise forms.ValidationError("invalid")
        return self.cleaned_data
    def login(self,request):
        username = self.cleaned_data['username_login']
        username = '_trainer_' + username
        password = self.cleaned_data['password_login']
        print("\nu & p lng : ", username, password)
        user = authenticate(username=username, password=password)
        print("auth user", user)
        return user

class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email'
    )


class ProfileForm(ModelForm):
    class Meta:
        model = Trainerprofile
        fields = ('Age', 'experience', 'address', 'phone_number', 'profile_pic','description')
