drop table if exists users;
drop table if exists accounts;

create table users (
    id integer primary key autoincrement,
    username text not null,
    pass_hash text not null
);

create table accounts (
    id integer primary key autoincrement,
    account_num text unique not null,
    balance int not null,
    account_holder integer not null
    -- foreign key(account_holder) refrences users(id)
);


insert into users (username, pass_hash) values ('Bob','Bob');
insert into accounts (account_num, balance, account_holder) values ('1',100,1);
insert into accounts(account_num, balance, account_holder) values ('2',200,1);
insert into accounts(account_num, balance, account_holder) values ('3',300,1);

insert into users(username, pass_hash)  values ('Alice','Alice');
insert into accounts(account_num, balance, account_holder) values ('4',-100,2);
insert into accounts(account_num, balance, account_holder) values ('5',-200,2);
insert into accounts(account_num, balance, account_holder) values ('6',-300,2);