from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from apps.accounts.models import User
from .models import Course, Subject, Enrollment


def is_teacher_or_admin(user):
    return user.role in [User.Role.TEACHER, User.Role.ADMIN]


@login_required
def course_list(request):
    user = request.user
    if is_teacher_or_admin(user):
        if user.role == User.Role.TEACHER:
            courses = Course.objects.filter(teacher=user)
        else:
            courses = Course.objects.all()
    else:
        courses = Course.objects.filter(enrollments__student=user)
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    subjects = course.subjects.all()
    enrollments = course.enrollments.select_related('student').all()
    can_edit = is_teacher_or_admin(request.user) and (
        request.user.role == User.Role.ADMIN or request.user == course.teacher
    )

    # Handle enrollment POST
    if request.method == 'POST' and 'enroll_student' in request.POST and is_teacher_or_admin(request.user):
        student_id = request.POST.get('student_id')
        student = get_object_or_404(User, pk=student_id, role=User.Role.STUDENT)
        Enrollment.objects.get_or_create(student=student, course=course)
        messages.success(request, f'{student.get_full_name()} inscrito.')
        return redirect('course_detail', pk=pk)

    ctx = {'course': course, 'subjects': subjects, 'enrollments': enrollments, 'can_edit': can_edit}
    if is_teacher_or_admin(request.user):
        ctx['students'] = User.objects.filter(role=User.Role.STUDENT).exclude(
            enrollments__course=course
        )
    return render(request, 'courses/course_detail.html', ctx)


@login_required
def course_create(request):
    if not is_teacher_or_admin(request.user):
        messages.error(request, 'No tienes permiso.')
        return redirect('course_list')
    teachers = User.objects.filter(role=User.Role.TEACHER)
    if request.method == 'POST':
        name = request.POST.get('name')
        grade = request.POST.get('grade')
        year = request.POST.get('year')
        teacher_id = request.POST.get('teacher')
        teacher = get_object_or_404(User, pk=teacher_id, role=User.Role.TEACHER) if teacher_id else None
        if request.user.role == User.Role.TEACHER:
            teacher = request.user
        Course.objects.create(name=name, grade=grade, year=year, teacher=teacher)
        messages.success(request, 'Curso creado.')
        return redirect('course_list')
    return render(request, 'courses/course_form.html', {'teachers': teachers, 'editing': False})


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not is_teacher_or_admin(request.user) or (request.user.role == User.Role.TEACHER and request.user != course.teacher):
        messages.error(request, 'No tienes permiso.')
        return redirect('course_list')
    teachers = User.objects.filter(role=User.Role.TEACHER)
    if request.method == 'POST':
        course.name = request.POST.get('name')
        course.grade = request.POST.get('grade')
        course.year = request.POST.get('year')
        if request.user.role == User.Role.ADMIN:
            teacher_id = request.POST.get('teacher')
            course.teacher = get_object_or_404(User, pk=teacher_id, role=User.Role.TEACHER) if teacher_id else None
        course.save()
        messages.success(request, 'Curso actualizado.')
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/course_form.html', {'course': course, 'teachers': teachers, 'editing': True})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not is_teacher_or_admin(request.user) or (request.user.role == User.Role.TEACHER and request.user != course.teacher):
        messages.error(request, 'No tienes permiso.')
        return redirect('course_list')
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Curso eliminado.')
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@login_required
def subject_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not is_teacher_or_admin(request.user) or (request.user.role == User.Role.TEACHER and request.user != course.teacher):
        messages.error(request, 'No tienes permiso.')
        return redirect('course_detail', pk=course_pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        Subject.objects.create(name=name, description=description, course=course)
        messages.success(request, 'Asignatura creada.')
        return redirect('course_detail', pk=course_pk)
    return render(request, 'courses/subject_form.html', {'course': course})


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    course = subject.course
    if not is_teacher_or_admin(request.user) or (request.user.role == User.Role.TEACHER and request.user != course.teacher):
        messages.error(request, 'No tienes permiso.')
        return redirect('course_detail', pk=course.pk)
    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.description = request.POST.get('description', '')
        subject.save()
        messages.success(request, 'Asignatura actualizada.')
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/subject_form.html', {'subject': subject, 'course': course, 'editing': True})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    course = subject.course
    if not is_teacher_or_admin(request.user) or (request.user.role == User.Role.TEACHER and request.user != course.teacher):
        messages.error(request, 'No tienes permiso.')
        return redirect('course_detail', pk=course.pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Asignatura eliminada.')
        return redirect('course_detail', pk=course.pk)
    return render(request, 'courses/subject_confirm_delete.html', {'subject': subject})


@login_required
def enroll_student(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not is_teacher_or_admin(request.user):
        messages.error(request, 'No tienes permiso.')
        return redirect('course_detail', pk=course_pk)
    students = User.objects.filter(role=User.Role.STUDENT).exclude(enrollments__course=course)
    if request.method == 'POST':
        student_id = request.POST.get('student')
        student = get_object_or_404(User, pk=student_id, role=User.Role.STUDENT)
        Enrollment.objects.get_or_create(student=student, course=course)
        messages.success(request, 'Alumno inscrito.')
        return redirect('course_detail', pk=course_pk)
    return render(request, 'courses/enroll_form.html', {'course': course, 'students': students})
