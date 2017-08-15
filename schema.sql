drop table if exists entries;

create table entries 
(
	id integer primary key autoincrement,
	eventtitle text not null,
	college text not null,
	doe datetime not null,
	category text not null
);
