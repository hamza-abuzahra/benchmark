create database if not exists website;

use website;

create table user(
    uid int primary key, 
    username varchar(20),
    upassword varchar(30), 
    uemail varchar(50),
    uphonenum varchar(15)
);

create table properties(
    pid int primary key, 
    pname varchar(50), 
    prooms int, 
    pavgocc float(20, 2), 
    pavgadr numeric(18, 2),
    plocation varchar(3),
    pn int, 
    uid int references user(uid)
);

create table records(
    rid int primary key, 
    pid int references properties(pid), 
    rdate date, 
    rrevenue numeric(18, 2), 
    rrooms int
);

-- create table charts(
--     cid int, 
--     rid int, 
--     cmedia 
-- )