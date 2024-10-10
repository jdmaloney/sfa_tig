CREATE TABLE `failed_drives` (
	`timestamp` TIMESTAMP NOT NULL,
	`storage_unit` VARCHAR(100) NOT NULL,
	`serial_number` VARCHAR(100) NOT NULL,
	`enclosure_index` INT NOT NULL,
	`slot_index` INT NOT NULL,
	`drive_vendor` VARCHAR(50) NOT NULL,
	`drive_model` VARCHAR(100) NOT NULL,
	`drive_type` VARCHAR(25) NOT NULL,
	`drive_speed` VARCHAR(25) NOT NULL,
	`drive_capacity_tib` INT NOT NULL,
	`drive_fw_rev` VARCHAR(25) NOT NULL
);
