from django.db import migrations


def set_default_roles(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM role WHERE name = 'regular'")
        row = cursor.fetchone()
        if row:
            regular_id = row[0]
            cursor.execute(
                'UPDATE "user" SET role_id = %s WHERE role_id IS NULL',
                [regular_id]
            )


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_admin_role_and_user'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE notice_like DROP CONSTRAINT IF EXISTS notice_like_pkey;
                ALTER TABLE notice_like ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;
            """,
            reverse_sql="""
                ALTER TABLE notice_like DROP COLUMN IF EXISTS id;
                ALTER TABLE notice_like ADD PRIMARY KEY (user_id, notice_id);
            """,
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE advice_like DROP CONSTRAINT IF EXISTS advice_like_pkey;
                ALTER TABLE advice_like ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;
            """,
            reverse_sql="""
                ALTER TABLE advice_like DROP COLUMN IF EXISTS id;
                ALTER TABLE advice_like ADD PRIMARY KEY (user_id, advice_id);
            """,
        ),
        migrations.RunPython(set_default_roles, migrations.RunPython.noop),
    ]
