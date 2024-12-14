from django import forms
from .models import Project
from apps.accounts.models import CustomUser
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'priority', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

        def __init__(self, *args, **kwargs):
            current_user = kwargs.pop('current_user', None)  # Get the current user
            super().__init__(*args, **kwargs)

            if current_user and current_user.role == 'Project Manager':
                self.fields['members'].queryset = CustomUser.objects.filter(
                    created_by=current_user, role='project_member'
                )
            else:
                self.fields['members'].queryset = CustomUser.objects.none()

class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),  # Default queryset, updated in __init__
        widget=forms.CheckboxSelectMultiple,  # You can use SelectMultiple if you prefer dropdown
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'deadline', 'members', 'created_at']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)  # Get the current user
        super().__init__(*args, **kwargs)

        if current_user and current_user.role == 'Project Manager':
            self.fields['members'].queryset = CustomUser.objects.filter(
                created_by=current_user, role='project_member'
            )
        else:
            self.fields['members'].queryset = CustomUser.objects.none()
