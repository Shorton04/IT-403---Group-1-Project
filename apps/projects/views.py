
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Project, Task
from .forms import ProjectForm
from .forms import TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
            form._save_m2m()  # Save many-to-many changes
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



@login_required
def kanban_board(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Ensure only project members or managers can view this page
    if request.user != project.created_by and request.user not in project.members.all():
        messages.error(request, "You are not authorized to view this project.")
        return redirect('project_list')

    # Filter tasks by status
    tasks_to_do = Task.objects.filter(project=project, status='to_do')
    tasks_in_progress = Task.objects.filter(project=project, status='in_progress')
    tasks_done = Task.objects.filter(project=project, status='done')

    context = {
        'project': project,
        'tasks_to_do': tasks_to_do,
        'tasks_in_progress': tasks_in_progress,
        'tasks_done': tasks_done,
    }
    return render(request, 'kanban_board.html', context)


@csrf_exempt
def update_task_status(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)
            task_id = data.get('task_id')
            new_status = data.get('status')

            # Ensure the necessary data is available
            if not task_id or not new_status:
                return JsonResponse({'success': False, 'error': 'Missing task_id or status'}, status=400)

            # Retrieve the task and update its status
            if request.user.role == 'Project Manager':
                task = Task.objects.get(id=task_id, project__created_by=request.user)
                task.status = new_status
                task.save()
            else:
                task = Task.objects.get(id=task_id, assigned_to=request.user)
                task.status = new_status
                task.save()

            # Return a success response
            return JsonResponse({'success': True})

        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.role != 'Project Manager' or project.created_by != request.user:
        messages.error(request, "You are not authorized to create tasks for this project.")
        return redirect('kanban_board', project_id=project_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect('kanban_board', project_id=project_id)
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form, 'project': project})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.role != 'Project Manager' or task.project.created_by != request.user:
        messages.error(request, "You are not authorized to edit this task.")
        return redirect('kanban_board', project_id=task.project.id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('kanban_board', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form, 'project': task.project})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.role != 'Project Manager' or task.project.created_by != request.user:
        messages.error(request, "You are not authorized to delete this task.")
        return redirect('kanban_board', project_id=task.project.id)

    if request.method == 'POST':
        project_id = task.project.id
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('kanban_board', project_id=project_id)

    return render(request, 'delete_task.html', {'task': task})


@login_required
def task_list(request):
    if request.user.role == 'Project Manager':
        tasks = Task.objects.filter(project__created_by=request.user).order_by('deadline')  # Order by deadline
    else:
        tasks = Task.objects.filter(assigned_to=request.user).order_by('deadline')  # Order by deadline

    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def gantt_chart(request):
    # Fetch projects based on user role
    if request.user.role == 'Project Manager':
        projects = Project.objects.filter(created_by=request.user).order_by('created_at')
    else:
        projects = Project.objects.filter(tasks__assigned_to=request.user).distinct().order_by('created_at')

    # Determine the default project (oldest)
    default_project = projects.first()

    # Get selected project from request or default to the oldest
    selected_project_id = request.GET.get('project', default_project.id)
    selected_project = get_object_or_404(Project, id=selected_project_id)

    # Fetch tasks for the selected project
    tasks = Task.objects.filter(project=selected_project)

    # Prepare data for Gantt chart
    chart_data = []
    for task in tasks:
        chart_data.append({
            'label': f"{task.name} ({task.assigned_to.get_full_name()})",
            'start': task.created_at.isoformat(),
            'end': task.deadline.isoformat(),
            'project': task.project.name
        })

    return render(request, 'gantt.html', {
        'chart_data': chart_data,
        'projects': projects,
        'selected_project': selected_project
    })

