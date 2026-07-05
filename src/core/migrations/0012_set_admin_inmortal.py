from django.db import migrations


def set_admin_inmortal(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE "user"
            SET title = 'Inmortal Académico',
                reputation_points = GREATEST(reputation_points, 201)
            WHERE email = 'admin@unal.edu.co'
        """)


def update_all_titles(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE "user"
            SET title = CASE
                WHEN reputation_points >= 201 THEN 'Inmortal Académico'
                WHEN reputation_points >= 101 THEN 'Leyenda UNAL'
                WHEN reputation_points >= 51 THEN 'Veterano'
                WHEN reputation_points >= 21 THEN 'Sobreviviente'
                ELSE 'Cachorro'
            END
            WHERE title IS NULL OR title = ''
        """)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0011_add_user_title'),
    ]

    operations = [
        migrations.RunPython(set_admin_inmortal, migrations.RunPython.noop),
        migrations.RunPython(update_all_titles, migrations.RunPython.noop),
    ]
