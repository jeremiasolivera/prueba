from django.forms import ModelForm
from .models import Room
from django import forms
from .models import Messages


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'area-control'}),
        }

        labels = {
            'description': '',
        }
        # Establece label_suffix en una cadena vacía para mover la etiqueta hacia arriba
        label_suffix = ''



class MessageForm(forms.ModelForm):
    body = forms.CharField(required=True)

    class Meta:
        model = Messages
        fields = ('body',)

    def save(self, user, room):
        message = super().save(commit=False)
        message.user = user
        message.room = room
        message.save()
        room.participants.add(user)
        return message