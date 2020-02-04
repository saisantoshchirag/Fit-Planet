from django import forms
from django.forms import ModelForm, Textarea
from .models import article


class postarticle(ModelForm):
    class Meta:
        model = article
        fields = [ 'title', 'image', 'content']
        #name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
        widgets = {
            'content': Textarea(attrs={'cols': 20, 'rows': 15})
        }


# class answerform(forms.Form):
#     name = forms.CharField(max_length=20)
#     answer = forms.Textarea(attrs={'cols': 20, 'rows': 15})








# class postarticle(forms.Form):
#     trainer_name = forms.CharField()
#     title = forms.CharField()
#     #slug = models.SlugField(null=True)
#     content = forms.CharField(widget=forms.Textarea)


# <p>
# Posted by: {{ object.trainer_name }} on {{ object.published_on }}<br><br>
# {{ object.content }}
# <br><hr>
# </p>



# <input type="text" name="trainer_name">
# <input type="text" name="title">
#     <textarea name="content"></textarea>