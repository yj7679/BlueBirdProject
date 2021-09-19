create database bluebird;
use bluebird;


CREATE TABLE `Employee` (
	`employee_number`	int	NOT NULL,
	`room_number`	int	NOT NULL,
	`id`	varchar(20)	NULL,
	`name`	varchar(20)	NULL,
	`password`	varchar(50)	NULL,
	`company`	varchar(20)	NULL,
	`department`	varchar(20)	NULL,
	`rank`	varchar(20)	NULL,
	`x`	int	NULL,
	`y`	int	NULL
);

CREATE TABLE `Room` (
	`room_number`	int	NOT NULL,
	`name`	varchar(20)	NULL,
	`x`	int	NULL,
	`y`	int	NULL
);

CREATE TABLE `Device` (
	`device_number`	int	NOT NULL,
	`room_number`	int	NOT NULL,
	`name`	varchar(20)	NULL,
	`x`	int	NULL,
	`y`	int	NULL,
	`is_on`	boolean	NULL
);

ALTER TABLE `Employee` ADD CONSTRAINT `PK_EMPLOYEE` PRIMARY KEY (
	`employee_number`
);

ALTER TABLE `Room` ADD CONSTRAINT `PK_ROOM` PRIMARY KEY (
	`room_number`
);

ALTER TABLE `Device` ADD CONSTRAINT `PK_DEVICE` PRIMARY KEY (
	`device_number`
);
