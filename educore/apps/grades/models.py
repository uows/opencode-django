from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Grade(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'},
        related_name='grades',
        verbose_name='estudiante',
    )
    subject = models.ForeignKey(
        'courses.Subject',
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='asignatura',
    )
    score = models.DecimalField('nota', max_digits=4, decimal_places=1,
                                validators=[MinValueValidator(1.0), MaxValueValidator(7.0)])
    coefficient = models.PositiveIntegerField('coeficiente', default=1)
    date = models.DateField('fecha', auto_now_add=True)

    class Meta:
        verbose_name = 'nota'
        verbose_name_plural = 'notas'

    def __str__(self):
        return f'{self.student.get_full_name()} - {self.subject.name}: {self.score}'
