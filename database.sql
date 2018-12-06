
-- San Diego

CREATE TABLE IF NOT EXISTS `san_diego_grid` (
    `id` MEDIUMINT UNSIGNED NOT NULL,
    `ring` SMALLINT UNSIGNED NOT NULL,
    `segment` SMALLINT UNSIGNED NOT NULL,
    `tab` SMALLINT UNSIGNED NOT NULL,
    `latitude_deg` REAL NOT NULL,
    `longitude_deg` REAL NOT NULL,
    `latitude_rad` REAL NOT NULL,
    `longitude_rad` REAL NOT NULL,
    `radius` INT NOT NULL,
    PRIMARY KEY(`id`),
    INDEX(`ring`, `segment`, `tab`),
    INDEX(`latitude_deg`),
    INDEX(`longitude_deg`),
    INDEX(`latitude_rad`),
    INDEX(`longitude_rad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `san_diego_requests` (
    `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    `grid_id` MEDIUMINT UNSIGNED NOT NULL,
    `timestamp` BIGINT UNSIGNED NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`grid_id`) REFERENCES `san_diego_grid` (`id`),
    INDEX(`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `san_diego_responses` (

) ENGINE=InnoDB DEFAULT CHARSET=utf8;