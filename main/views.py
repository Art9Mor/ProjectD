from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.models import Student


class StudentListView(ListView):
    model = Student
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Список студентов'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset


def index(request):
    student_list = Student.objects.all()
    context = {
        'object_list': student_list,
        'title': 'Главная',
    }

    return render(request, 'main/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    context = {
        'title': 'Контакты'
    }

    return render(request, 'main/contact.html', context)


class StudentDetailView(DetailView):
    model = Student
    template_name = 'main/student_detail.html'


class StudentCreateView(CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'avatar', 'is_active', 'info']
    success_url = reverse_lazy('main:index')
    extra_context = {
        'title': 'Создать студента'
    }


class StudentUpdateView(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'avatar', 'is_active', 'info']

    def get_success_url(self):
        return reverse('main:view_student', args={self.kwargs.get('pk')})


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('main:index')
