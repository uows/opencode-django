from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from apps.courses.models import Course, Enrollment, Subject
from apps.grades.models import Grade
from apps.assignments.models import Assignment
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Email o contraseña incorrectos.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
        else:
            user = User.objects.create_user(
                email=email, first_name=first_name, last_name=last_name,
                password=password, role=User.Role.STUDENT
            )
            login(request, user)
            return redirect('dashboard')
    return render(request, 'accounts/register.html')


@login_required
def dashboard(request):
    user = request.user
    ctx = {'role': user.role}

    if user.role == User.Role.STUDENT:
        courses = Course.objects.filter(enrollments__student=user)
        enrollments_count = courses.count()
        grades = Grade.objects.filter(student=user)
        avg = grades.aggregate(Avg('score'))['score__avg']
        pending = Assignment.objects.filter(
            subject__course__in=courses,
            due_date__gte=__import__('django').utils.timezone.now()
        ).count()
        ctx.update({
            'courses': courses, 'enrollments_count': enrollments_count,
            'grades_count': grades.count(), 'average': round(avg, 1) if avg else None,
            'pending_assignments': pending,
        })

    elif user.role in [User.Role.TEACHER, User.Role.ADMIN]:
        if user.role == User.Role.TEACHER:
            courses = Course.objects.filter(teacher=user)
        else:
            courses = Course.objects.all()
        total_students = User.objects.filter(role=User.Role.STUDENT).count()
        total_courses = courses.count()
        total_teachers = User.objects.filter(role=User.Role.TEACHER).count()
        all_grades = Grade.objects.filter(subject__course__in=courses)
        avg = all_grades.aggregate(Avg('score'))['score__avg']
        ctx.update({
            'courses': courses, 'total_students': total_students,
            'total_courses': total_courses, 'total_teachers': total_teachers,
            'average': round(avg, 1) if avg else None,
        })

    return render(request, 'accounts/dashboard.html', ctx)


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        messages.success(request, 'Perfil actualizado.')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'profile_user': user})
