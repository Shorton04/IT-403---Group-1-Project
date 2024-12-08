from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.projects.models import Project
from apps.accounts.models import CustomUser

@login_required
def project_list(request):
    projects = Project.objects.filter(created_by=request.user)
    members = CustomUser.objects.filter(created_by=request.user)
    return render(request, 'project_list.html', {'projects': projects, 'members': members})

@login_required
def view_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    return render(request, 'project_details.html', {'project': project})

@login_required
def create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        deadline = request.POST['deadline']
        members_ids = request.POST.getlist('members')

        project = Project.objects.create(
            name=name,
            description=description,
            deadline=deadline,
            created_by=request.user
        )
        project.members.set(members_ids)
        project.save()

        messages.success(request, "Project created successfully!")
        return redirect('project_list')
