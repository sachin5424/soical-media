from django import forms
from django.forms import ModelForm, Textarea, TextInput,Select,FileInput,HiddenInput
from insta.models import Profile,User_Post,AddFriend,User_Post_commt

class User_Postform(forms.ModelForm):
    class Meta:
        model = User_Post
        # fields = '__all__'
        fields = ['subject','msg','pic']

class AddFriend_form(forms.ModelForm):
    class Meta:
        model =AddFriend
        fields= ['add_by','add','confirmn']
        # widgets = {
        #     'add': HiddenInput(attrs={
        #         'autocomplete': 'off'}),
        #     'add_by': HiddenInput(attrs={
        #         "class": "bg-white rounded border border-red-400 focus:outline-none focus:border-indigo-500 text-base px-4 py-2 mb-4 mt-0"}),
        #     'confirmn': HiddenInput(attrs={
        #         "class": "bg-white rounded border border-red-400 focus:outline-none focus:border-indigo-500 text-base px-4 py-2 mb-4 mt-0"}),
        # }

class User_Post_commtform(forms.ModelForm):
    class Meta:
        model =User_Post_commt
        fields= ['you_msg']