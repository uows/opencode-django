from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.utils import timezone
from apps.accounts.models import User
from apps.courses.models import Course, Subject, Enrollment
from .models import Grade


def is_teacher_or_admin(user):
    return user.role in [User.Role.TEACHER, User.Role.ADMIN]


@login_required
def grade_list(request):
    user = request.user
    if is_teacher_or_admin(user):
        if user.role == User.Role.TEACHER:
            courses = Course.objects.filter(teacher=user)
        else:
            courses = Course.objects.all()
        ctx = {'courses': courses, 'is_teacher': True}

        subject_id = request.GET.get('subject')
        course_id = request.GET.get('course')
        grades = Grade.objects.filter(subject__course__in=courses).select_related('student', 'subject')
        if course_id:
            grades = grades.filter(subject__course_id=course_id)
            ctx['selected_course'] = int(course_id)
        if subject_id:
            grades = grades.filter(subject_id=subject_id)
            ctx['selected_subject'] = int(subject_id)
        ctx['grades'] = grades
        if course_id:
            ctx['subjects'] = Subject.objects.filter(course_id=course_id)
        return render(request, 'grades/grade_list_teacher.html', ctx)
    else:
        grades = Grade.objects.filter(student=user).select_related('subject__course')
        avg = grades.aggregate(Avg('score'))['score__avg']
        return render(request, 'grades/grade_list_student.html', {
            'grades': grades, 'average': round(avg, 1) if avg else None,
        })


@login_required
def grade_create(request):
    if not is_teacher_or_admin(request.user):
        messages.error(request, 'No tienes permiso.')
        return redirect('grade_list')
    if request.user.role == User.Role.TEACHER:
        courses = Course.objects.filter(teacher=request.user)
    else:
        courses = Course.objects.all()
    subjects = Subject.objects.none()
    students = User.objects.none()

    course_id = request.GET.get('course') or request.POST.get('course')
    subject_id = request.GET.get('subject') or request.POST.get('subject')

    if course_id:
        subjects = Subject.objects.filter(course_id=course_id)
        students = User.objects.filter(role=User.Role.STUDENT, enrollments__course_id=course_id)

    if request.method == 'POST':
        student = get_object_or_404(User, pk=request.POST.get('student'), role=User.Role.STUDENT)
        subject = get_object_or_404(Subject, pk=request.POST.get('subject'))
        score = request.POST.get('score')
        coefficient = request.POST.get('coefficient', 1)
        Grade.objects.create(student=student, subject=subject, score=score, coefficient=coefficient)
        messages.success(request, 'Nota registrada.')
        return redirect('grade_create')

    return render(request, 'grades/grade_form.html', {
        'courses': courses, 'subjects': subjects, 'students': students,
        'selected_course': int(course_id) if course_id else None,
        'selected_subject': int(subject_id) if subject_id else None,
    })


@login_required
def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if not is_teacher_or_admin(request.user):
        messages.error(request, 'No tienes permiso.')
        return redirect('grade_list')
    if request.method == 'POST':
        grade.score = request.POST.get('score')
        grade.coefficient = request.POST.get('coefficient', 1)
        grade.save()
        messages.success(request, 'Nota actualizada.')
        return redirect('grade_list')
    return render(request, 'grades/grade_edit.html', {'grade': grade})


@login_required
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if not is_teacher_or_admin(request.user):
        messages.error(request, 'No tienes permiso.')
        return redirect('grade_list')
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Nota eliminada.')
    return redirect('grade_list')


@login_required
def student_grades(request, student_id):
    student = get_object_or_404(User, pk=student_id, role=User.Role.STUDENT)
    user = request.user
    if user != student and not is_teacher_or_admin(user):
        messages.error(request, 'No tienes permiso.')
        return redirect('dashboard')
    grades = Grade.objects.filter(student=student).select_related('subject__course')
    avg = grades.aggregate(Avg('score'))['score__avg']
    by_subject = grades.values('subject__name', 'subject_id').annotate(avg=Avg('score')).order_by('subject__name')
    return render(request, 'grades/student_grades.html', {
        'student': student, 'grades': grades,
        'average': round(avg, 1) if avg else None,
        'by_subject': by_subject,
    })
