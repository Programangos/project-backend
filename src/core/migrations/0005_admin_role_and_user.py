from django.db import migrations
from hashlib import sha256


def seed_admin(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM role WHERE name = 'Administrador'")
        row = cursor.fetchone()
        if row:
            admin_role_id = row[0]
        else:
            cursor.execute("INSERT INTO role (name) VALUES ('Administrador') RETURNING id")
            admin_role_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT id FROM role WHERE name = 'regular'"
        )
        if not cursor.fetchone():
            cursor.execute("INSERT INTO role (name) VALUES ('regular')")

        cursor.execute(
            "SELECT id FROM role WHERE name = 'special'"
        )
        if not cursor.fetchone():
            cursor.execute("INSERT INTO role (name) VALUES ('special')")

        password_hash = sha256('AdminSISA'.encode()).hexdigest()
        cursor.execute(
            """
            INSERT INTO "user" (full_name, email, password_hash, major, current_semester, reputation_points, is_active, role_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT (email) DO NOTHING
            """,
            ['Administrador', 'admin@unal.edu.co', password_hash, 'Administración', 1, 0, True, admin_role_id]
        )


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_password_reset_token'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                INSERT INTO role (name) SELECT 'regular' WHERE NOT EXISTS (SELECT 1 FROM role WHERE name = 'regular');
            """,
            reverse_sql="DELETE FROM role WHERE name = 'regular';",
        ),
        migrations.RunSQL(
            sql="""
                INSERT INTO role (name) SELECT 'special' WHERE NOT EXISTS (SELECT 1 FROM role WHERE name = 'special');
            """,
            reverse_sql="DELETE FROM role WHERE name = 'special';",
        ),
        migrations.RunSQL(
            sql="""
                INSERT INTO role (name) SELECT 'Administrador' WHERE NOT EXISTS (SELECT 1 FROM role WHERE name = 'Administrador');
            """,
            reverse_sql="DELETE FROM role WHERE name = 'Administrador';",
        ),
        migrations.RunPython(seed_admin, migrations.RunPython.noop),
    ]
