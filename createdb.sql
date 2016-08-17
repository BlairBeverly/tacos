-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema tacosdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tacosdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tacosdb` DEFAULT CHARACTER SET utf8 ;
USE `tacosdb` ;

-- -----------------------------------------------------
-- Table `tacosdb`.`restaurants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tacosdb`.`restaurants` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `street_num` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `zip` SMALLINT NULL,
  `price` TINYINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tacosdb`.`items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tacosdb`.`items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `restaurant_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_items_restaurants_idx` (`restaurant_id` ASC),
  CONSTRAINT `fk_items_restaurants`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `tacosdb`.`restaurants` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
