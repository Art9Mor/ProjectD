from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from main.forms import StudentForm, SubjectForm
from main.models import Student, Subject


@login_required
@permission_required('main.view_subject')
def index(request):
    student_list = Student.objects.all()
    context = {
        'object_list': student_list,
        'title': 'Главная',
    }

    return render(request, 'main/index.html', context)


@login_required
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


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Список студентов'
    }

    # def get_queryset(self, *args, **kwargs):
    #     queryset = super().get_queryset(*args, **kwargs)
    #     queryset = queryset.filter(is_active=True)
    #     return queryset


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    permission_required = 'main.view_student'
    template_name = 'main/student_detail.html'


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    permission_required = 'main.add_student'
    form_class = StudentForm
    # fields = ['first_name', 'last_name', 'avatar', 'is_active', 'info']
    success_url = reverse_lazy('main:index')
    extra_context = {
        'title': 'Создать студента'
    }


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    permission_required = 'main.change_student'
    form_class = StudentForm
    success_url = reverse_lazy('main:index')

    def get_success_url(self):
        return reverse('main:view_student', args={self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Student, Subject, form=SubjectForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('main:index')

    def test_func(self):
        return self.request.user.is_superuser


@login_required
def toggle_activity(request, pk):
    student_item = get_object_or_404(Student, pk=pk)
    if student_item.is_active:
        student_item.is_active = False
    else:
        student_item.is_active = True
    student_item.save()
    return redirect(reverse('main:index'))
