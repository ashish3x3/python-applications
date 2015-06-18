drop table if exists students;
create table students (
  id integer primary key autoincrement,
  name text not null,
  branch text not null
);

drop table if exists users;
    create table users (
        email text not null,
        username text primary key not null,
        password text null
    );
