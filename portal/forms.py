from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions)

class QuestionsForm(forms.Form):
    url = forms.URLField(label="URL", required=True)
    tag = forms.CharField(label="Tag", required=True)
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action   = 'questionsubmit'
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))