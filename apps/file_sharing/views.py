from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SharedFile
from .forms import SharedFileForm

@login_required
def file_list(request):
    files = SharedFile.objects.filter(uploaded_by=request.user)
    return render(request, 'file_sharing/file_list.html', {'files': files})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = SharedFileForm(request.POST, request.FILES)
        if form.is_valid():
            shared_file = form.save(commit=False)
            shared_file.uploaded_by = request.user
            shared_file.save()
            return redirect('file_list')
    else:
        form = SharedFileForm()
    return render(request, 'file_sharing/upload_file.html', {'form': form})