from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_alter_user_avatar_url_type'),
    ]
    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS password_reset_token (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                    token VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_password_reset_token_token ON password_reset_token(token);
            """,
            reverse_sql='DROP TABLE IF EXISTS password_reset_token;',
        ),
    ]
