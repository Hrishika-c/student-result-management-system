create database student_db;
use student_db;

create table admin(
admin_id int primary key,
username varchar(50),
password varchar(50)
);

create table students(
student_id varchar(50) primary key,
name varchar(50), 
password varchar(50));

CREATE TABLE teachers (
    teacher_id varchar(50) PRIMARY KEY ,
    name varchar(50),
    username VARCHAR(255),
    password VARCHAR(255)
);
CREATE TABLE results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id varchar(50),
    english INT,
    maths INT,
    physics INT,
    chemistry INT,
    computer INT,
    total INT,
    percentage FLOAT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

insert into students values('S1','Rita','student123');
insert into teachers values('T1','Mr.ghosh','T1','teacher123');
select * from results;
select * from students;