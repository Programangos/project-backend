CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    major VARCHAR(255),
    current_semester INT,
    avatar_url VARCHAR(500),
    reputation_points INT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    role_id INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,

    CONSTRAINT fk_user_role
        FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE building (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    building_number INT UNIQUE,
    description TEXT,
    latitude DECIMAL,
    longitude DECIMAL
);

CREATE TABLE building_comment (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INT,
    building_id INT,
    created_at TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (building_id) REFERENCES building(id)
);

CREATE TABLE advice (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    category VARCHAR(255),
    status VARCHAR(50),
    user_id INT,
    created_at TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE TABLE advice_like (
    user_id INT,
    advice_id INT,
    created_at TIMESTAMP,

    PRIMARY KEY (user_id, advice_id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (advice_id) REFERENCES advice(id)
);

CREATE TABLE procedure (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    official_description TEXT,
    avg_time_days DECIMAL DEFAULT 0
);

CREATE TABLE procedure_experience (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    actual_time_days INT,
    user_id INT,
    procedure_id INT,
    created_at TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (procedure_id) REFERENCES procedure(id)
);

CREATE TABLE procedure_experience_vote (
    user_id INT,
    experience_id INT,
    created_at TIMESTAMP,

    PRIMARY KEY (user_id, experience_id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (experience_id) REFERENCES procedure_experience(id)
);

CREATE TABLE notice (
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

CREATE TABLE notice_like (
    user_id INT,
    notice_id INT,
    created_at TIMESTAMP,

    PRIMARY KEY (user_id, notice_id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (notice_id) REFERENCES notice(id)
);

CREATE TABLE report (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(50),
    reference_id INT,
    reporter_id INT,
    reason TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP,

    FOREIGN KEY (reporter_id) REFERENCES "user"(id)
);

CREATE TABLE achievement (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    points_required INT
);

CREATE TABLE user_achievement (
    user_id INT,
    achievement_id INT,
    earned_at TIMESTAMP,

    PRIMARY KEY (user_id, achievement_id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (achievement_id) REFERENCES achievement(id)
);
