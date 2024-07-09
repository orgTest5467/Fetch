 CREATE TABLE IF NOT EXISTS login_user (
                user_id VARCHAR(128),
                devide_type VARCHAR(32),
                masked_ip VARCHAR(256),
                masked_device_id VARCHAR(256),
                Locale VARCHAR(32),
                app_version integer,
                create_date date, 
                PRIMARY KEY (masked_device_id, masked_ip)
                    );