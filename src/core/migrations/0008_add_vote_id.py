from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_add_procedure_type_department'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE procedure_experience_vote
                DROP CONSTRAINT procedure_experience_vote_pkey;

                ALTER TABLE procedure_experience_vote
                ADD COLUMN id SERIAL NOT NULL;

                ALTER TABLE procedure_experience_vote
                ADD PRIMARY KEY (id);

                ALTER TABLE procedure_experience_vote
                ADD CONSTRAINT procedure_experience_vote_unique_user_experience
                UNIQUE (user_id, experience_id);
            """,
            reverse_sql="""
                ALTER TABLE procedure_experience_vote
                DROP CONSTRAINT IF EXISTS procedure_experience_vote_unique_user_experience;

                ALTER TABLE procedure_experience_vote DROP CONSTRAINT IF EXISTS procedure_experience_vote_pkey;

                ALTER TABLE procedure_experience_vote DROP COLUMN IF EXISTS id;

                ALTER TABLE procedure_experience_vote
                ADD PRIMARY KEY (user_id, experience_id);
            """,
        ),
    ]
