from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_user_avatar_url'),
    ]
    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE "user" ALTER COLUMN avatar_url TYPE TEXT;',
            reverse_sql='ALTER TABLE "user" ALTER COLUMN avatar_url TYPE VARCHAR(500);',
        ),
    ]
