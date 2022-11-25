from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    # password1 = forms.CharField(
    #     widget = forms.PasswordInput(
    #         attrs={
    #         "class":"form-control"
    #         }
    #         )
    #     )
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #         "class":"form-control"
    #         }))
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]


class ArchitectForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ArchitectForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Architect
        fields = CustomUserForm.Meta.fields + \
            ['mobile']


class ClientForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Client
        fields = CustomUserForm.Meta.fields


class EngineerForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(EngineerForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Engineer
        fields = CustomUserForm.Meta.fields + \
        ['mobile']



# class FeedbackStaffForm(FormSettings):

#     def __init__(self, *args, **kwargs):
#         super(FeedbackStaffForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = FeedbackStaff
#         fields = ['feedback']

class ConstructionForm(forms.ModelForm):  
    class Meta:  
        model = ConstructionProjects
        fields = ['project_architect','project_eng','project', 'descrition','project_type'] #https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = { 'project': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'descrition': forms.TextInput(attrs={ 'class': 'form-control' }),
            'project_type': forms.TextInput(attrs={ 'class': 'form-control' }),
            'project_architect': forms.TextInput(attrs={ 'class': 'form-control' }),
            'project_eng': forms.TextInput(attrs={ 'class': 'form-control' }),
            # 'project_plans': forms.FileInput(attrs={ 'class': 'form-control' }),

      }
class AdminRequestForm(forms.Form):
    # fields = []
    #to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown there in html
    project_architect=forms.ModelChoiceField(queryset=Architect.objects.all(),empty_label="Architect Name",to_field_name='id')
    project_eng=forms.ModelChoiceField(queryset=Engineer.objects.all(),empty_label="Engineer Name",to_field_name='id')

class ConstructionProjectsForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(ConstructionProjectsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ConstructionProjects
        fields = ['project_type','project','descrition']


class TaskArchitectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(TaskArchitectForm, self).__init__(*args, **kwargs)

    # constructionproject = forms.ModelChoiceField(queryset=ConstructionProjects.objects.all(),empty_label="Project Name",to_field_name='id')    

    class Meta:
        model = ArchitectTask
        fields = ['constructionproject','archictect_plan','progress','status']


class TaskEngineerForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(TaskEngineerForm, self).__init__(*args, **kwargs)

    # constructionproject = forms.ModelChoiceField(queryset=ConstructionProjects.objects.all(),empty_label="Project Name",to_field_name='id')    

    class Meta:
        model = EngineerTask
        fields = ['constructionproject','eng_report','eng_images','phases']




class ArchitectEditForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(ArchitectEditForm, self).__init__(*args, **kwargs)
    admin = forms.ModelChoiceField(queryset=CustomUser.objects.all(),empty_label="User",to_field_name="id")    
    class Meta:
        model = Architect
        fields = ['admin','mobile','project_type','project_plans',]


class EngineerEditForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(EngineerEditForm, self).__init__(*args, **kwargs)
    # admin = forms.ModelChoiceField(queryset=CustomUser.objects.all(),empty_label="User",to_field_name="id")    
    class Meta:
        model = Engineer
        fields = ['mobile','project_type','project_images','budget']




# class StaffEditForm(CustomUserForm):
#     def __init__(self, *args, **kwargs):
#         super(StaffEditForm, self).__init__(*args, **kwargs)

#     class Meta(CustomUserForm.Meta):
#         model = Staff
#         fields = CustomUserForm.Meta.fields
