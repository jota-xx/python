from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView
from .forms import LoginForm, UserRegistrationForm, UserEditForm, Perfil, UserForm
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def add_user(request):
    if request.method == "POST":
        perfil_form=UserForm(request.POST)
        if perfil_form.is_valid():
            try:
                new_user = perfil_form.save(commit=False)
                new_user.set_password(
                    perfil_form.cleaned_data['password'])
                new_user.save()

                return render(request,
                              'students/student/registration.html',
                              {'mensaje': 'Se agrego correctamente', 'new_user': new_user, })
            except:
                return render(request,
                              'students/student/registration.html',
                              locals(),)

    else:
        perfil_form = UserForm
    return render(request,
                  'students/student/registration.html',
                  locals(), )



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()

            # Create the user profile
            profile = Perfil.objects.create(user=new_user)
            profile.date_of_birth = request.POST['date_of_birth']
            profile.save()

            # profile_form = ProfileEditForm(instance=request.user.profile)

            return render(request,
                          'students/student/edit.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = UserForm()
    return render(request,
                  'students/student/registration.html',
                  {'user_form': user_form, "profile_form": profile_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = UserForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserForm(instance=request.user.profile)
    return render(request,
                  'students/student/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context