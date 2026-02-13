# root 관리자 실행
create user 'django'@'%' identified by 'django';

create database djangodb character set utf8mb4 collate utf8mb4_unicode_ci;

grant all privileges on djangodb.* to 'django'@'%';
flush privileges;
