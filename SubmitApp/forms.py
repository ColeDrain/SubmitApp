from django import forms
from .models import Question, Solution
from datetime import datetime

class SubmitForm(forms.ModelForm):

    class Meta:
        model = Solution
        fields = ['question', 'image', 'solution_text']

    def __init__(self, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['question'].queryset = Question.objects.filter(upload_date=datetime.now().date())
        self.fields['question'].initial = Question.objects.filter(upload_date=datetime.now().date()).first()
        self.fields['question'].disabled = True
        if Question.objects.filter(upload_date=datetime.now().date()).first().question_type=='Maths':
            self.fields.pop('solution_text')
        else:
            self.fields.pop('image')

    def clean_question(self):
        if not self['question'].html_name in self.data:
            return self.fields['question'].initial
        return self.cleaned_data['question']

class QuestionUploadForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text', 'question_type']