DROP DATABASE IF EXISTS vending;
CREATE DATABASE IF NOT EXISTS vending DEFAULT CHARSET=utf8;
USE vending;

CREATE TABLE `Products` (
	`name` VARCHAR(255) NOT NULL,
	`description` VARCHAR(255),
	`price` DECIMAL(11,2) UNSIGNED NOT NULL,
	`id` INTEGER(11) UNSIGNED AUTO_INCREMENT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Transactions` (
	`timestamp` DATETIME NOT NULL,
	`amount` DECIMAL(11,2) UNSIGNED NOT NULL,
	`id` INTEGER(11) UNSIGNED AUTO_INCREMENT NOT NULL,
	`product_id` INTEGER(11) UNSIGNED,
	PRIMARY KEY (`id`),
	CONSTRAINT `transactions_fk_product` FOREIGN KEY (`product_id`) REFERENCES `Products` (`id`)
);

CREATE TABLE `Inventory` (
	`product_id` INTEGER(11) UNSIGNED NOT NULL,
	`quantity` INTEGER(11) UNSIGNED NOT NULL DEFAULT 0,
	`rail` VARCHAR(2) NOT NULL,
	PRIMARY KEY (`product_id`),
	KEY `product_id` (`product_id`),
	CONSTRAINT `inventory_fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `Products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

