create table if not exists transactions (
transaction_id SERIAL PRIMARY KEY,
sender_id INTEGER NOT NULL,
recipient_id INTEGER NOT NULL,
amount NUMERIC(7,5) NOT NULL);