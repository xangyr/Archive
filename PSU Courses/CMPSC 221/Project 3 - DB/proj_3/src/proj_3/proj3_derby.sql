/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 * Author:  Ritsh
 * Created: Apr 16, 2019
 */

create table zipcodes
(
zip varchar(5) not null primary key,
city varchar(30),
state varchar(2),
latitude float,
longtitude float
);

create table stores
(
store_id smallint not null GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1) primary key,
store_name varchar(20),
zip varchar(5),
address varchar(255),
description varchar(5000),
foreign key(zip) references zipcodes(zip)
);

create table store_hours
(
hr_id int not null GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1) primary key,
store_id smallint not null,
day smallint NOT NULL,
open_time time,
close_time time,
foreign key(store_id) references stores(store_id)
);

create table managerlogon
(
usr_id smallint not null GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1) primary key,
username varchar(20),
password varchar(20),
store_id smallint,
foreign key(store_id) references stores(store_id)
);

insert into stores
(store_name, zip, address, description)
values
('FamilyMart', '16601', '406 E 25th Ave','The first Familymart in Altoona, open 24 hours'),
('Seven Eleven', '16801', '228 W College Ave', 'A place where sells chinese food');

insert into managerlogon
(username, password, store_id)
values
('useradmin', 'admin', null),
('xvr5040', 'password', (select store_id from stores where store_name = 'Seven Eleven' and zip = '16801')),
('psu', 'pennstate', (select store_id from stores where store_name = 'FamilyMart' and zip = '16601'));

insert into store_hours
(store_id, day, open_time, close_time)
values
((select store_id from stores where store_name = 'FamilyMart' and zip = '16601'), 1, '09:00', '18:00'),
((select store_id from stores where store_name = 'FamilyMart' and zip = '16601'), 2, '09:00', '18:00'),
((select store_id from stores where store_name = 'FamilyMart' and zip = '16601'), 3, '09:00', '18:00'),
((select store_id from stores where store_name = 'FamilyMart' and zip = '16601'), 4, '09:00', '18:00'),
((select store_id from stores where store_name = 'FamilyMart' and zip = '16601'), 5, '09:00', '18:00'),
((select store_id from stores where store_name = 'FamilyMart' and zip = '16601'), 6, '09:00', '18:00'),
((select store_id from stores where store_name = 'FamilyMart' and zip = '16601'), 7, '09:00', '18:00'),
((select store_id from stores where store_name = 'Seven Eleven' and zip = '16801'), 1, '09:30', '17:30'),
((select store_id from stores where store_name = 'Seven Eleven' and zip = '16801'), 2, '09:30', '17:30'),
((select store_id from stores where store_name = 'Seven Eleven' and zip = '16801'), 3, '09:30', '17:30'),
((select store_id from stores where store_name = 'Seven Eleven' and zip = '16801'), 4, '09:30', '17:30'),
((select store_id from stores where store_name = 'Seven Eleven' and zip = '16801'), 5, '09:30', '17:30'),
((select store_id from stores where store_name = 'Seven Eleven' and zip = '16801'), 6, '09:30', '17:30'),
((select store_id from stores where store_name = 'Seven Eleven' and zip = '16801'), 7, '09:30', '17:30');
insert into store_hours
(store_id, day, open_time, close_time)
values
((select store_id from stores where store_name = 'Xiaomaibu' and zip = '01069'), 1, '09:30', '17:30'),
((select store_id from stores where store_name = 'Xiaomaibu' and zip = '01069'), 2, '09:30', '17:30'),
((select store_id from stores where store_name = 'Xiaomaibu' and zip = '01069'), 3, '09:30', '17:30'),
((select store_id from stores where store_name = 'Xiaomaibu' and zip = '01069'), 4, '09:30', '17:30'),
((select store_id from stores where store_name = 'Xiaomaibu' and zip = '01069'), 5, '09:30', '17:30'),
((select store_id from stores where store_name = 'Xiaomaibu' and zip = '01069'), 6, '09:30', '17:30'),
((select store_id from stores where store_name = 'Xiaomaibu' and zip = '01069'), 7, '09:30', '17:30');