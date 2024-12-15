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
from .utils import notify_project_activity
from .models import Project, SharedFile
from .forms import SharedFileForm
import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import is_aware, make_naive
import datetime
from openpyxl.utils import get_column_letter

def safe_make_naive(dt):
    # Check if the object is a datetime and timezone-aware
    if isinstance(dt, datetime.datetime):
        return make_naive(dt) if is_aware(dt) else dt
    # If the object is a date, return it as is
    elif isinstance(dt, datetime.date):
        return dt
    # Return None or raise an error if the input is unexpected
    else:
        return None  # or raise ValueError("Expected a datetime or date object")

def report_view(request):
    projects = Project.objects.all()
    selected_project_id = request.GET.get('project')

    project = Project.objects.filter(id=selected_project_id).first() if selected_project_id else None
    tasks = Task.objects.filter(project=project) if project else Task.objects.none()

    # Calculate percentage of completed tasks
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='done').count()
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks else 0

    if request.GET.get('generate_report'):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={project.name}_report.xlsx'

        task_data = tasks.values('name', 'assigned_to__username', 'status', 'priority', 'created_at', 'deadline')

        task_data_list = []
        for task in task_data:
            task['created_at'] = safe_make_naive(task['created_at'])
            task['deadline'] = safe_make_naive(task['deadline'])
            task_data_list.append(task)

        df = pd.DataFrame(task_data_list)
        df.columns = ['Task Name', 'Assigned To', 'Status', 'Priority', 'Created At', 'Deadline']

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            # Create a new workbook and worksheet
            df.to_excel(writer, index=False, startrow=4, sheet_name='Tasks')
            worksheet = writer.sheets['Tasks']

            # Write the custom header
            worksheet['A1'] = f'Project: {project.name}'
            worksheet['A2'] = f'Completion: {completion_percentage:.2f}%'

            # Adjust column width
            for i, column in enumerate(df.columns, 1):
                max_length = max(df[column].astype(str).apply(len).max(), len(column))
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[get_column_letter(i)].width = adjusted_width

        return response

    return render(request, 'report.html', {
        'projects': projects,
        'status_counts': {
            'to_do': tasks.filter(status='to_do').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'done': completed_tasks,
        },
        'selected_project_id': selected_project_id,
        'project_name': project.name if project else '',
    })


@login_required
def project_file_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user not in project.members.all() and request.user != project.created_by:
        messages.error(request, "You are not authorized to view this project's files.")
        return redirect('projects_list')

    files = SharedFile.objects.filter(project=project)
    return render(request, 'project_file_list.html', {'project': project, 'files': files})


@login_required
def upload_file_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user not in project.members.all() and request.user != project.created_by:
        messages.error(request, "You are not authorized to upload files to this project.")
        return redirect('projects_list')

    if request.method == 'POST':
        form = SharedFileForm(request.POST, request.FILES)
        if form.is_valid():
            shared_file = form.save(commit=False)
            shared_file.uploaded_by = request.user
            shared_file.project = project
            shared_file.save()
            messages.success(request, "File uploaded successfully!")

        return redirect('project_file_list', project_id=project.id)
    else:
        form = SharedFileForm()

    return render(request, 'upload_file_to_project.html', {'form': form, 'project': project})

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
            # Notify members added to the project
            for member in project.members.all():
                notify_project_activity(request.user, member, project, "You have been added to a new project")
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
                project_manager = task.project.created_by
                notify_project_activity(
                    request.user,
                    project_manager,
                    task.project,
                    f"Task '{task.name}' status updated to {new_status}"
                )
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
            # Notify the assigned user
            if task.assigned_to:
                notify_project_activity(
                    sender=request.user,
                    recipient=task.assigned_to,
                    project=project,
                    message=f"You have been assigned a new task: {task.name}"
                )
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

def gantt_chart(request):
    projects = Project.objects.all()
    selected_project_id = request.GET.get('project')
    tasks = Task.objects.filter(project_id=selected_project_id) if selected_project_id else []

    return render(request, 'gantt.html', {'projects': projects, 'tasks': tasks})


def pie_chart_view(request):
    projects = Project.objects.all()
    selected_project_id = request.GET.get('project')
    tasks = Task.objects.filter(project_id=selected_project_id) if selected_project_id else []

    status_counts = {
        'to_do': tasks.filter(status='to_do').count(),
        'in_progress': tasks.filter(status='in_progress').count(),
        'done': tasks.filter(status='done').count(),
    }

    return render(request, 'gantt.html', {
        'projects': projects,
        'status_counts': status_counts,
    })

