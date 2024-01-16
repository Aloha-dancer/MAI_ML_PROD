BEGIN;

DROP TABLE IF EXISTS public.user;
DROP TABLE IF EXISTS public.email;
DROP TABLE IF EXISTS public.message;

CREATE TABLE IF NOT EXISTS public.user(
user_id SERIAL CONSTRAINT pk1 PRIMARY KEY,
last_name VARCHAR(64) NULL,
first_name VARCHAR(64) NOT NULL,
email VARCHAR(64) NOT NULL UNIQUE,
password VARCHAR(128) NOT NULL,
login VARCHAR(64) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS public.message(
message_id BIGSERIAL,
date DATE NOT NULL,
user_id INT NOT NULL,
text TEXT NULL,
subject VARCHAR(100) NULL,
message TEXT NULL,
content TEXT NULL,
label VARCHAR(10) DEFAULT 'ham',
CONSTRAINT pk3 PRIMARY KEY (message_id, date)
);

ALTER TABLE public.message 
ADD CONSTRAINT fk_msg_user FOREIGN KEY (user_id) REFERENCES public.user (user_id) 
ON DElETE CASCADE 
ON UPDATE CASCADE;


INSERT INTO public.user (last_name, first_name, email, login, password) VALUES
('1', '1', '1', 'test', ' '),
('2', '2', '2', 'test2', ' '),
('Valery', 'Popov', 'valeriy.popov@gmail.com', 'valeriy.popov', '123123123');

COMMIT;

END;