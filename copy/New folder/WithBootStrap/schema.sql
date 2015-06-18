drop table if exists user;
    create table user (
       
        username text primary key not null,
        password text null
    );

     /*INSERT INTO 'user'
      SELECT 'ash' AS 'username', 'ash' AS 'password'
UNION SELECT 'man', 'man'
UNION SELECT 'san', 'san'
UNION SELECT 'asho', 'asho'*/


INSERT INTO 'user' values ('ash','ash');
INSERT INTO 'user' values ('man','ash');
INSERT INTO 'user' values ('san','ash');
/*SELECT ''ash, 'aaa'
UNION ALL
SELECT 'man', 'bbb'*/