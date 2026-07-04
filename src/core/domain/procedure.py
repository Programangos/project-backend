from django.db import models


class Procedure(models.Model):
    TYPE_CHOICES = [
        ('academico', 'Académico'),
        ('administrativo', 'Administrativo'),
        ('admisiones', 'Admisiones'),
        ('bienestar', 'Bienestar Universitario'),
        ('biblioteca', 'Biblioteca'),
        ('cultural', 'Cultural'),
        ('deportivo', 'Deportivo'),
        ('extension', 'Extensión'),
        ('financiero', 'Financiero'),
        ('graduacion', 'Graduación'),
        ('internacionalizacion', 'Internacionalización'),
        ('investigacion', 'Investigación'),
        ('movilidad', 'Movilidad Académica'),
        ('posgrado', 'Posgrado'),
        ('practicas', 'Prácticas Académicas'),
        ('pregrado', 'Pregrado'),
        ('registro', 'Registro y Control'),
        ('salud', 'Salud'),
        ('seguridad', 'Seguridad Universitaria'),
        ('tecnologia', 'Tecnología'),
        ('vivienda', 'Vivienda Universitaria'),
    ]

    name = models.CharField(max_length=255)
    official_description = models.TextField()
    type = models.CharField(max_length=255, blank=True, default='', choices=TYPE_CHOICES)
    department = models.CharField(max_length=255, blank=True, default='')
    avg_time_days = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        db_table = 'procedure'
        managed = False


class ProcedureExperience(models.Model):
    comment = models.TextField()
    actual_time_days = models.IntegerField()
    user = models.ForeignKey(
        'core.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    procedure = models.ForeignKey(
        'core.Procedure',
        on_delete=models.DO_NOTHING,
        db_column='procedure_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'procedure_experience'
        managed = False


class ProcedureExperienceVote(models.Model):
    user = models.ForeignKey(
        'core.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    experience = models.ForeignKey(
        'core.ProcedureExperience',
        on_delete=models.DO_NOTHING,
        db_column='experience_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'procedure_experience_vote'
        managed = False
        unique_together = ('user', 'experience')
