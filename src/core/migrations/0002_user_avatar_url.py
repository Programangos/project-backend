from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]
    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE "user" ADD COLUMN IF NOT EXISTS avatar_url TEXT NULL;',
            reverse_sql='ALTER TABLE "user" DROP COLUMN IF EXISTS avatar_url;',
        ),
    ]
