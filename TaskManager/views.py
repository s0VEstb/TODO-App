
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Task, Status
from .forms import StatusForm, TaskForm

# Create your views here.
def main_page_view(request):
    if request.method == 'GET':
        return render(request, 'main.html')


def task_page_view(request):
    if request.method == 'GET':

        search = request.GET.get("search")
        status_id = request.GET.get("status")
        sort = request.GET.get("sort")
        page = request.GET.get("page", 1)
        page = request.GET.get("page", 1)

        tasks = Task.objects.all()
        status = Status.objects.all()

        limit = 6
        max_pages = len(tasks) / limit
        if max_pages != 0:
            max_pages = int(max_pages) + 1
        pages = [i for i in range(1, max_pages + 1)]

        start = (int(page) - 1) * limit
        end = start + limit

        if search:
            tasks = tasks.filter(
                Q(name__icontains=search) |
                Q(content__icontains=search) |
                Q(category__name__icontains=search) |
                Q(catalog__name__icontains=search)
            )
        if status_id:
            tasks = tasks.filter(
                status=status_id
            )

        if sort == "newest":
            tasks = tasks.order_by("-created_at")
            print(tasks)

        if sort == "oldest":
            tasks = tasks.order_by("created_at")

        tasks = tasks[start:end]


        return render(request,
                      'tasks.html',
                      context={'tasks': tasks,
                               'pages': pages,
                               'status': status})


def task_detail_view(request, task_id):
    task = Task.objects.get(id=task_id)
    form = TaskForm(instance=task)
    context = {'task': task, 'form': form}
    if request.method == 'GET':
        return render(request,
                      'task_detail.html',
                      context=context)
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if not form.is_valid():
            return render(request,
                          'task_detail.html',
                          context=context)
        form.save()
        return redirect('/tasks/')


@login_required(login_url='/accounts/login/')
def delete_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('/tasks/')


def create_task_view(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request,
                      'create_task.html',
                      context={'form': form})
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if not form.is_valid():
            return render(request,
                          'create_task.html',
                          context={'form': form})
        task = form.save(commit=False)  # Создаем задачу, но не сохраняем ее в базу данных
        task.user = request.user  # Устанавливаем текущего пользователя как владельца задачи
        task.save()
        return redirect('/tasks/')


def update_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request,
                      'update_task.html',
                      {'task': task, 'form': form})
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if not form.is_valid():
            return render(request,
                          'update_task.html',
                          {'task': task, 'form': form})
        form.save()
        return redirect(f'/tasks/{task_id}')

