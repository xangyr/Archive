/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 * Author:  xvr5040
 * Created: Apr 30, 2019
 */
/*
"Attributes", "Weapons", "Age", "Gender"
*/


create table outfits
(
outfits_id smallint not null GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1) primary key, 
description varchar(255)
);

create table attributes
(
attributes_id smallint not null GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1) primary key,
description varchar(255)
);

create table weapons
(
weapons_id smallint not null GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1) primary key,
description varchar(255)
);

create table characters
(
id int not null  GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1) primary key, 
name varchar(20) not null,
outfits_id smallint,
attributes_id smallint,
weapons_id smallint,
age int,
gender varchar(6),
foreign key(outfits_id) references outfits(outfits_id),
foreign key(attributes_id) references attributes(attributes_id),
foreign key(weapons_id) references weapons(weapons_id)
);