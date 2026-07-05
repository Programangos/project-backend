from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_seed_procedures'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE building_comment DROP CONSTRAINT IF EXISTS building_comment_building_id_fkey;",
            reverse_sql="""
                ALTER TABLE building_comment
                ADD CONSTRAINT building_comment_building_id_fkey
                FOREIGN KEY (building_id) REFERENCES building(id);
            """,
        ),
    ]
