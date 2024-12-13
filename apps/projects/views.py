from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.projects.models import Project
from apps.accounts.models import CustomUser

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm

@login_required
def project_list(request):
    if request.user.role == 'Project Manager':
        projects = Project.objects.filter(created_by=request.user)  # Projects managed by the user
    else:
        projects = request.user.assigned_projects.all()  # Projects the user is a member of

    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.role == 'Project Manager' and project.created_by != request.user:
        messages.error(request, "You are not authorized to view this project.")
        return redirect('project_list')

    if request.user not in project.members.all() and request.user != project.created_by:
        messages.error(request, "You are not authorized to view this project.")
        return redirect('project_list')

    return render(request, 'project_detail.html', {'project': project})

@login_required
def create_project(request):
    if request.user.role != 'Project Manager':
        messages.error(request, "You are not authorized to create projects.")
        return redirect('project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, current_user=request.user)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user  # Assign the project manager as the creator
            project.save()  # Save the project
            form.save_m2m()  # Save the many-to-many relationships (members)
            messages.success(request, "Project created successfully!")
            return redirect('project_list')
        else:
            messages.error(request, "There was an error creating the project. Please check the form.")
    else:
        form = ProjectForm(current_user=request.user)

    return render(request, 'create_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)

    if request.user.role != 'Project Manager':
        messages.error(request, "You are not authorized to edit this project.")
        return redirect('project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project, current_user=request.user)
        if form.is_valid():
            project = form.save()
            form.save_m2m()  # Save many-to-many changes
            messages.success(request, "Project updated successfully!")
            return redirect('project_list')
        else:
            messages.error(request, "There was an error updating the project.")
    else:
        form = ProjectForm(instance=project, current_user=request.user)

    return render(request, 'edit_project.html', {'form': form, 'project': project})


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)

    if request.user.role != 'Project Manager':
        messages.error(request, "You are not authorized to delete this project.")
        return redirect('project_list')

    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('project_list')

    return render(request, 'delete_project.html', {'project': project})

