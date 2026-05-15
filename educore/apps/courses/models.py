from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField('nombre', max_length=100)
    grade = models.CharField('grado', max_length=50)
    year = models.PositiveIntegerField('año')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'TEACHER'},
        verbose_name='profesor',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'
        unique_together = ('name', 'grade', 'year')

    def __str__(self):
        return f'{self.name} - {self.grade} ({self.year})'


class Subject(models.Model):
    name = models.CharField('nombre', max_length=100)
    description = models.TextField('descripción', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects', verbose_name='curso')

    class Meta:
        verbose_name = 'asignatura'
        verbose_name_plural = 'asignaturas'

    def __str__(self):
        return f'{self.name} ({self.course.name})'


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'},
        related_name='enrollments',
        verbose_name='estudiante',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='curso')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'inscripción'
        verbose_name_plural = 'inscripciones'
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.get_full_name()} → {self.course}'
