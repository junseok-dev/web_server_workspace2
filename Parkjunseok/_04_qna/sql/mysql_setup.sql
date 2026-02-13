-- Active: 1770790774318@@127.0.0.1@3306@mysql
# root 관리자 실행
-- create user 'django'@'%' identified by 'django';

create database qnadb character set utf8mb4 collate utf8mb4_unicode_ci;

grant all privileges on qnadb.* to 'django'@'%';
flush privileges;
