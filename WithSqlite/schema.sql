drop table if exists email;
create table email (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  email text not null
  
);