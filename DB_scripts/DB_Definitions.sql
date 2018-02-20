CREATE TABLE Hero (
    `id` INT     NOT NULL UNIQUE AUTO_INCREMENT,
    `Hero_Name` VARCHAR(60) NOT NULL UNIQUE,
    `Hero_Category` VARCHAR(60),
    PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;

CREATE TABLE Map (
    `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
    `Map_Name` VARCHAR NOT NULL UNIQUE,
    `Map_Category` VARCHAR,
    PRIMARY KEY (`id`)
);

CREATE TABLE `Team` (
  `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
  `Team_Name` VARCHAR(60) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;