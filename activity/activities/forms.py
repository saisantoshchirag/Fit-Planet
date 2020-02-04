from django import forms
from . import models
import pandas as pd

file = pd.read_csv(r'C:\sem-5\SOAD\project\activity\activities\exercises.csv',header=0,encoding = 'unicode_escape')
choices = [(i,i) for i in file['Activity']]

class CreateActivity(forms.ModelForm):
    widgets = {'from_time': forms.DateInput(format='%d-%m-%Y')}
    title = forms.CharField(label='Title', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'title'}))
    type = forms.ChoiceField(label='Type',choices=choices)
    from_time = forms.CharField(label='Start time',widget=forms.widgets.TimeInput(attrs={"type":"time"}))
    to_time = forms.CharField(label='End time',widget=forms.widgets.TimeInput(attrs={"type":"time"}))
    #calories = forms.IntegerField(label='Calories',widget=forms.NumberInput(attrs={'placeholder': 'Calories','type':'number'}))

    class Meta:
        model = models.Activity
        fields = ['title','type','from_time','to_time','calories']
