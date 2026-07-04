from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_fix_noticelike_add_role_defaults'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE procedure
                ADD COLUMN IF NOT EXISTS type VARCHAR(255) NOT NULL DEFAULT '';
            """,
            reverse_sql="""
                ALTER TABLE procedure DROP COLUMN IF EXISTS type;
            """,
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE procedure
                ADD COLUMN IF NOT EXISTS department VARCHAR(255) NOT NULL DEFAULT '';
            """,
            reverse_sql="""
                ALTER TABLE procedure DROP COLUMN IF EXISTS department;
            """,
        ),
    ]
