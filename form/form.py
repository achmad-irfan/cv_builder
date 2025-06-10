# form/forms.py

from django import forms
from .models import CV, Education, Skill, Experience, Certificate
from django.forms import modelformset_factory

# Form Header
class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['photo_profile','name', 'roles', 'location', 'email', 'telp', 'web', 'summary']
        widgets = {
            'name': forms.TextInput(attrs={'required': False}),
            'email': forms.EmailInput(attrs={'required': False}),
            'summary': forms.Textarea(attrs={'required': False, 'class': 'text-area'}),
        }

# Form Education
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school_name', 'location', 'degree', 'major', 'start_year', 'end_year', 'grade']
        widgets = {
            field: forms.TextInput(attrs={'required': False})
            for field in fields if field != 'degree'
        }
        widgets['degree'] = forms.Select()

EducationFormSet = modelformset_factory(Education, form=EducationForm, extra=1, can_delete=True)

# Form Skill
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']
        widgets = {'skill_name': forms.TextInput(attrs={'required': False})}

SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=1, can_delete=True)

# Form Certificate
class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate_name', 'year', 'company']
        widgets = {field: forms.TextInput(attrs={'required': False}) for field in fields}

CertificateFormSet = modelformset_factory(Certificate, form=CertificateForm, extra=1, can_delete=True)

# Form Experience
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['experience_name', 'location', 'position', 'start_year', 'end_year', 'jobdesc']
        widgets = {
            **{field: forms.TextInput(attrs={'required': False}) for field in fields if field != 'jobdesc'},
            'jobdesc': forms.Textarea(attrs={'rows': 8, 'required': False}),
        }


ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1, can_delete=True)
