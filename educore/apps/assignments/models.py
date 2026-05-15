from django.db import models
from django.conf import settings


class Assignment(models.Model):
    title = models.CharField('título', max_length=200)
    description = models.TextField('descripción', blank=True)
    subject = models.ForeignKey(
        'courses.Subject',
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='asignatura',
    )
    due_date = models.DateTimeField('fecha de entrega')
    attachment = models.FileField('archivo', upload_to='assignments/', blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='creado por',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'tarea'
        verbose_name_plural = 'tareas'

    def __str__(self):
        return self.title
