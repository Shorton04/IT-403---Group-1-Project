from django.shortcuts import render, get_object_or_404
from .models import Board
from django.contrib.auth.decorators import login_required

def board_list(request):
    boards = Board.objects.filter(owner=request.user)
    return render(request, 'board_list.html', {'boards': boards})

def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'board_detail.html', {'board': board})

@login_required
def home(request):
    return render(request, 'home.html')