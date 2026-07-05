from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_drop_building_comment_fk'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE public.user ADD COLUMN IF NOT EXISTS title VARCHAR(100) NULL;",
            reverse_sql="ALTER TABLE public.user DROP COLUMN IF EXISTS title;",
        ),
    ]
