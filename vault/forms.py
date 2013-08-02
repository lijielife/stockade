from django import forms

class ProjectForm(forms.Form):
	project_name = forms.CharField(max_length=255)
	project_desc = forms.CharField(max_length=255)