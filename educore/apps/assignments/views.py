from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.accounts.models import User
from apps.courses.models import Course, Subject
from .models import Assignment


def is_teacher_or_admin(user):
    return user.role in [User.Role.TEACHER, User.Role.ADMIN]


@login_required
def assignment_list(request):
    user = request.user
    if is_teacher_or_admin(user):
        if user.role == User.Role.TEACHER:
            assignments = Assignment.objects.filter(subject__course__teacher=user)
        else:
            assignments = Assignment.objects.all()
        assignments = assignments.select_related('subject__course', 'created_by')
    else:
        courses = Course.objects.filter(enrollments__student=user)
        assignments = Assignment.objects.filter(
            subject__course__in=courses
        ).select_related('subject__course', 'created_by')
    return render(request, 'assignments/assignment_list.html', {
        'assignments': assignments, 'is_teacher': is_teacher_or_admin(user),
        'now': timezone.now(),
    })


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    is_teacher = is_teacher_or_admin(request.user)
    enrolled = request.user.role == User.Role.STUDENT and assignment.subject.course.enrollments.filter(
        student=request.user
    ).exists()
    if not is_teacher and not enrolled:
        messages.error(request, 'No tienes permiso.')
        return redirect('assignment_list')
    return render(request, 'assignments/assignment_detail.html', {
        'assignment': assignment, 'is_teacher': is_teacher,
    })


@login_required
def assignment_create(request):
    if not is_teacher_or_admin(request.user):
        messages.error(request, 'No tienes permiso.')
        return redirect('assignment_list')
    if request.user.role == User.Role.TEACHER:
        subjects = Subject.objects.filter(course__teacher=request.user)
    else:
        subjects = Subject.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        subject_id = request.POST.get('subject')
        due_date = request.POST.get('due_date')
        subject = get_object_or_404(Subject, pk=subject_id)
        attachment = request.FILES.get('attachment')
        Assignment.objects.create(
            title=title, description=description, subject=subject,
            due_date=due_date, attachment=attachment, created_by=request.user,
        )
        messages.success(request, 'Tarea creada.')
        return redirect('assignment_list')
    return render(request, 'assignments/assignment_form.html', {
        'subjects': subjects, 'editing': False,
    })


@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not is_teacher_or_admin(request.user):
        messages.error(request, 'No tienes permiso.')
        return redirect('assignment_list')
    if request.user.role == User.Role.TEACHER:
        subjects = Subject.objects.filter(course__teacher=request.user)
    else:
        subjects = Subject.objects.all()
    if request.method == 'POST':
        assignment.title = request.POST.get('title')
        assignment.description = request.POST.get('description', '')
        assignment.subject = get_object_or_404(Subject, pk=request.POST.get('subject'))
        assignment.due_date = request.POST.get('due_date')
        if request.FILES.get('attachment'):
            assignment.attachment = request.FILES.get('attachment')
        assignment.save()
        messages.success(request, 'Tarea actualizada.')
        return redirect('assignment_detail', pk=assignment.pk)
    return render(request, 'assignments/assignment_form.html', {
        'assignment': assignment, 'subjects': subjects, 'editing': True,
    })


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not is_teacher_or_admin(request.user):
        messages.error(request, 'No tienes permiso.')
        return redirect('assignment_list')
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Tarea eliminada.')
        return redirect('assignment_list')
    return render(request, 'assignments/assignment_confirm_delete.html', {'assignment': assignment})
