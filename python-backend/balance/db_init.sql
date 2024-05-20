--psql -c "<command>"
create table if not exists balances (
user_id INTEGER PRIMARY KEY,
balance DECIMAL(10,2) NOT NULL
);

insert into balances (user_id, balance)
values (1, 100.00), (2, 200.00)
