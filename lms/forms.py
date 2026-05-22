from django import forms
from .models import Assignment, Submission, Quiz, Question, LiveClass, Course


class AssignmentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(teacher=user)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

    class Meta:
        model  = Assignment
        fields = ('course', 'title', 'description', 'due_date', 'total_marks')
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model  = Submission
        fields = ('text_answer', 'file')
        widgets = {
            'text_answer': forms.Textarea(attrs={'rows': 5, 'class': 'form-input',
                                                  'placeholder': 'Type your answer here...'}),
            'file': forms.FileInput(attrs={'class': 'form-input'}),
        }


class QuizForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(teacher=user)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

    class Meta:
        model  = Quiz
        fields = ('course', 'title', 'description', 'total_marks', 'time_limit', 'due_date')
        widgets = {
            'due_date':    forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model  = Question
        fields = ('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'marks')
        widgets = {
            'text':           forms.Textarea(attrs={'rows': 2, 'class': 'form-input'}),
            'option_a':       forms.TextInput(attrs={'class': 'form-input'}),
            'option_b':       forms.TextInput(attrs={'class': 'form-input'}),
            'option_c':       forms.TextInput(attrs={'class': 'form-input'}),
            'option_d':       forms.TextInput(attrs={'class': 'form-input'}),
            'correct_option': forms.Select(attrs={'class': 'form-input'}),
            'marks':          forms.NumberInput(attrs={'class': 'form-input'}),
        }


class LiveClassForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(teacher=user)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

    class Meta:
        model  = LiveClass
        fields = ('course', 'title', 'description', 'date', 'start_time', 'end_time', 'meet_link')
        widgets = {
            'date':        forms.DateInput(attrs={'type': 'date'}),
            'start_time':  forms.TimeInput(attrs={'type': 'time'}),
            'end_time':    forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }