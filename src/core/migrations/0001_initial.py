from django.db import migrations


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.RunSQL(
            sql="""
CREATE TABLE IF NOT EXISTS role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    major VARCHAR(255),
    current_semester INT,
    reputation_points INT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    role_id INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_user_role
        FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE IF NOT EXISTS building (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    building_number INT UNIQUE,
    description TEXT,
    latitude DECIMAL,
    longitude DECIMAL
);

CREATE TABLE IF NOT EXISTS building_comment (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INT,
    building_id INT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (building_id) REFERENCES building(id)
);

CREATE TABLE IF NOT EXISTS advice (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    category VARCHAR(255),
    status VARCHAR(50),
    user_id INT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE TABLE IF NOT EXISTS advice_like (
    user_id INT,
    advice_id INT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, advice_id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (advice_id) REFERENCES advice(id)
);

CREATE TABLE IF NOT EXISTS procedure (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    official_description TEXT,
    avg_time_days DECIMAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS procedure_experience (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    actual_time_days INT,
    user_id INT,
    procedure_id INT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (procedure_id) REFERENCES procedure(id)
);

CREATE TABLE IF NOT EXISTS procedure_experience_vote (
    user_id INT,
    experience_id INT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, experience_id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (experience_id) REFERENCES procedure_experience(id)
);

CREATE TABLE IF NOT EXISTS notice (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    category VARCHAR(255),
    is_official BOOLEAN DEFAULT false,
    expiration_date DATE,
    user_id INT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE TABLE IF NOT EXISTS notice_like (
    user_id INT,
    notice_id INT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, notice_id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (notice_id) REFERENCES notice(id)
);

CREATE TABLE IF NOT EXISTS report (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(50),
    reference_id INT,
    reporter_id INT,
    reason TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP,
    FOREIGN KEY (reporter_id) REFERENCES "user"(id)
);

CREATE TABLE IF NOT EXISTS achievement (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    points_required INT
);

CREATE TABLE IF NOT EXISTS user_achievement (
    user_id INT,
    achievement_id INT,
    earned_at TIMESTAMP,
    PRIMARY KEY (user_id, achievement_id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (achievement_id) REFERENCES achievement(id)
);
            """,
            reverse_sql="",
        ),
    ]
