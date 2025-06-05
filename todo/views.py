from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Todo
from .forms import TodoForm, TodoUpdateForm
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def todo_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    priority_filter = request.GET.get('priority', 'all')
    
    todos = Todo.objects.filter(user=request.user)
    
    if search_query:
        todos = todos.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if status_filter == 'completed':
        todos = todos.filter(completed=True)
    elif status_filter == 'pending':
        todos = todos.filter(completed=False)
    
    if priority_filter != 'all':
        todos = todos.filter(priority=priority_filter)
    
    context = {
        'todos': todos,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    return render(request, 'todo/todo_list.html', context)

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('todo:list')
    else:
        form = TodoForm()
    
    return render(request, 'todo/todo_form.html', {
        'form': form,
        'title': 'Create Todo'
    })

@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TodoUpdateForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todo:list')
    else:
        form = TodoUpdateForm(instance=todo)
    
    return render(request, 'todo/todo_form.html', {
        'form': form,
        'title': 'Update Todo',
        'todo': todo
    })

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    messages.success(request, 'Todo deleted successfully!')
    return redirect('todo:list')

@login_required
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    status = "completed" if todo.completed else "pending"
    messages.success(request, f'Todo marked as {status}!')
    return redirect('todo:list')

def logout_view(request):
    logout(request)
    return redirect('login')
