from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from apps.accounts.models import User
from apps.courses.models import Course, Subject, Enrollment
from apps.grades.models import Grade
from apps.assignments.models import Assignment
from faker import Faker
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Genera datos de prueba para EduCore'

    def handle(self, *args, **options):
        fake = Faker('es_CL')
        Faker.seed(42)
        random.seed(42)

        self.stdout.write('Limpiando datos existentes...')
        Assignment.objects.all().delete()
        Grade.objects.all().delete()
        Enrollment.objects.all().delete()
        Subject.objects.all().delete()
        Course.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create admin user
        admin, _ = User.objects.get_or_create(
            email='admin@educore.cl',
            defaults={
                'first_name': 'Admin', 'last_name': 'Principal',
                'role': User.Role.ADMIN, 'is_staff': True,
            }
        )
        admin.set_password('admin123')
        admin.save()
        self.stdout.write(self.style.SUCCESS(f'✓ Admin: admin@educore.cl / admin123'))

        teachers = []
        teacher_names = [
            ('María', 'González'), ('Carlos', 'Muñoz'), ('Ana', 'López'),
            ('Pedro', 'Ramírez'), ('Laura', 'Torres'),
        ]
        for first, last in teacher_names:
            email = f'{first.lower()}.{last.lower()}@educore.cl'
            t, _ = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first, 'last_name': last, 'role': User.Role.TEACHER},
            )
            t.set_password('profesor123')
            t.save()
            teachers.append(t)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(teachers)} profesores creados (pass: profesor123)'))

        students = []
        for i in range(30):
            first = fake.first_name()
            last = fake.last_name()
            email = f'{first.lower()}.{last.lower()}{i}@educore.cl'
            s, _ = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first, 'last_name': last, 'role': User.Role.STUDENT},
            )
            s.set_password('alumno123')
            s.save()
            students.append(s)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(students)} alumnos creados (pass: alumno123)'))

        course_data = [
            ('1° Básico A', '1° Básico'), ('2° Básico A', '2° Básico'),
            ('5° Básico A', '5° Básico'), ('1° Medio A', '1° Medio'),
            ('2° Medio A', '2° Medio'), ('3° Medio A', '3° Medio'),
        ]
        courses = []
        for i, (name, grade) in enumerate(course_data):
            c = Course.objects.create(
                name=name, grade=grade, year=2025,
                teacher=teachers[i % len(teachers)],
            )
            courses.append(c)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(courses)} cursos creados'))

        subject_names = {
            '1° Básico': ['Lenguaje', 'Matemáticas', 'Ciencias Naturales', 'Historia'],
            '2° Básico': ['Lenguaje', 'Matemáticas', 'Ciencias Naturales', 'Historia'],
            '5° Básico': ['Lenguaje', 'Matemáticas', 'Ciencias Naturales', 'Historia', 'Inglés'],
            '1° Medio': ['Lenguaje', 'Matemáticas', 'Física', 'Química', 'Historia', 'Inglés'],
            '2° Medio': ['Lenguaje', 'Matemáticas', 'Física', 'Química', 'Historia', 'Inglés'],
            '3° Medio': ['Lenguaje', 'Matemáticas', 'Física', 'Química', 'Historia', 'Inglés', 'Biología'],
        }

        subjects = []
        for course in courses:
            names = subject_names.get(course.grade, ['Lenguaje', 'Matemáticas'])
            for name in names:
                s = Subject.objects.create(
                    name=name,
                    description=f'Asignatura de {name.lower()} para {course.name}',
                    course=course,
                )
                subjects.append(s)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(subjects)} asignaturas creadas'))

        enrollments_created = 0
        for student in students:
            enrolled_courses = random.sample(courses, k=random.randint(1, 2))
            for course in enrolled_courses:
                _, created = Enrollment.objects.get_or_create(student=student, course=course)
                if created:
                    enrollments_created += 1
        self.stdout.write(self.style.SUCCESS(f'✓ {enrollments_created} inscripciones creadas'))

        grades_created = 0
        for student in students:
            enrolled_courses = Course.objects.filter(enrollments__student=student)
            for course in enrolled_courses:
                course_subjects = Subject.objects.filter(course=course)
                for subject in course_subjects:
                    for _ in range(random.randint(3, 6)):
                        score = round(random.uniform(1.0, 7.0), 1)
                        Grade.objects.create(
                            student=student, subject=subject,
                            score=score, coefficient=random.choice([1, 1, 1, 2, 3]),
                            date=timezone.now().date() - timedelta(days=random.randint(1, 90)),
                        )
                        grades_created += 1
        self.stdout.write(self.style.SUCCESS(f'✓ {grades_created} notas creadas'))

        assignments_created = 0
        for subject in subjects:
            for _ in range(random.randint(1, 3)):
                due = timezone.now() + timedelta(days=random.randint(-10, 30))
                Assignment.objects.create(
                    title=fake.sentence(nb_words=4).rstrip('.'),
                    description=fake.paragraph(nb_sentences=3),
                    subject=subject,
                    due_date=due,
                    created_by=random.choice(teachers),
                )
                assignments_created += 1
        self.stdout.write(self.style.SUCCESS(f'✓ {assignments_created} tareas creadas'))

        self.stdout.write(self.style.SUCCESS('\n✓ Seed completado exitosamente'))
        self.stdout.write(self.style.SUCCESS('\nCredenciales:'))
        self.stdout.write(f'  Admin:   admin@educore.cl / admin123')
        self.stdout.write(f'  Profesor: maria.gonzalez@educore.cl / profesor123')
        self.stdout.write(f'  Alumno:  (cualquier alumno) / alumno123')
