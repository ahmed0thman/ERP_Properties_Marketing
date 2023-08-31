-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 20, 2020 at 07:36 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `properties`
--
DROP DATABASE IF EXISTS `properties`;
CREATE DATABASE IF NOT EXISTS `properties` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `properties`;

-- --------------------------------------------------------

--
-- Table structure for table `blocks`
--

CREATE TABLE IF NOT EXISTS `blocks` (
  `block_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `num_of_pieces` int(11) DEFAULT NULL,
  `street` int(11) NOT NULL,
  `city` int(11) NOT NULL,
  PRIMARY KEY (`block_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `cities`
--

CREATE TABLE IF NOT EXISTS `cities` (
  `city_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `mohafza` varchar(45) CHARACTER SET utf8 NOT NULL,
  `num_of_streets` int(11) DEFAULT NULL,
  PRIMARY KEY (`city_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cities`
--

INSERT INTO `cities` (`city_id`, `name`, `mohafza`, `num_of_streets`) VALUES
(2, 'سمنود', 'الغربيه', 50),
(3, 'المنصوره', 'الدقهليه', 190),
(5, 'الشباب', 'القليوبيه', 160),
(6, 'طلخا', 'الدقهلية', 21);

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE IF NOT EXISTS `clients` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `phone1` varchar(45) NOT NULL,
  `phone2` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `is_owner` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`client_id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `phone1` (`phone1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `contracts`
--

CREATE TABLE IF NOT EXISTS `contracts` (
  `contract_id` int(11) NOT NULL,
  `type` varchar(45) NOT NULL,
  `price` float NOT NULL,
  `date_` date NOT NULL,
  `owner` int(11) NOT NULL,
  `client` int(11) NOT NULL,
  `employee` int(11) NOT NULL,
  `piece` int(11) NOT NULL,
  PRIMARY KEY (`contract_id`),
  KEY `owner` (`owner`),
  KEY `client` (`client`),
  KEY `employee` (`employee`),
  KEY `piece` (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `contracts_rents`
--

CREATE TABLE IF NOT EXISTS `contracts_rents` (
  `duration` int(11) NOT NULL,
  `rent_price` float NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `pre_price` float DEFAULT NULL,
  `paid_monthes` int(11) DEFAULT NULL,
  `contract` int(11) NOT NULL,
  KEY `contract` (`contract`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `doplex`
--

CREATE TABLE IF NOT EXISTS `doplex` (
  `doplex_type` varchar(45) DEFAULT NULL,
  `pool` tinyint(1) DEFAULT NULL,
  `special_enter` tinyint(1) DEFAULT NULL,
  `inner_stairs` tinyint(1) DEFAULT NULL,
  `garden` tinyint(1) DEFAULT NULL,
  `piece` int(11) NOT NULL,
  KEY `piece` (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `eductional`
--

CREATE TABLE IF NOT EXISTS `eductional` (
  `type` varchar(45) NOT NULL,
  `piece` int(11) NOT NULL,
  KEY `piece` (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `emara`
--

CREATE TABLE IF NOT EXISTS `emara` (
  `num_of_floors` int(11) DEFAULT NULL,
  `ta4teb_type` varchar(45) DEFAULT NULL,
  `gaz` tinyint(1) DEFAULT NULL,
  `water` tinyint(1) DEFAULT NULL,
  `electricity` tinyint(1) DEFAULT NULL,
  `piece` int(11) NOT NULL,
  PRIMARY KEY (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE IF NOT EXISTS `employee` (
  `emp_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `phone` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `department` varchar(45) DEFAULT NULL,
  `salary` float NOT NULL,
  `start_date` date DEFAULT NULL,
  PRIMARY KEY (`emp_id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `factories`
--

CREATE TABLE IF NOT EXISTS `factories` (
  `type` varchar(45) NOT NULL,
  `piece` int(11) NOT NULL,
  KEY `piece` (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `flat`
--

CREATE TABLE IF NOT EXISTS `flat` (
  `piece` int(11) NOT NULL,
  `num_of_rooms` int(11) DEFAULT NULL,
  `num_of_bathrooms` int(11) DEFAULT NULL,
  `floor_number` int(11) DEFAULT NULL,
  `type` varchar(45) NOT NULL,
  `ta4teb_type` varchar(45) DEFAULT NULL,
  `villa_type` varchar(45) DEFAULT NULL,
  `gaz` tinyint(1) DEFAULT NULL,
  `water` tinyint(1) DEFAULT NULL,
  `electricity` tinyint(1) DEFAULT NULL,
  `container` int(11) NOT NULL,
  PRIMARY KEY (`piece`),
  KEY `container` (`container`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE IF NOT EXISTS `images` (
  `image` longtext,
  `piece` int(11) NOT NULL,
  KEY `piece` (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `lands`
--

CREATE TABLE IF NOT EXISTS `lands` (
  `land_status` varchar(45) NOT NULL,
  `land_type` varchar(45) NOT NULL,
  `details` longtext,
  `piece` int(11) NOT NULL,
  KEY `piece` (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `login_info`
--

CREATE TABLE IF NOT EXISTS `login_info` (
  `username` varchar(45) NOT NULL,
  `password_` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `employee` int(11) NOT NULL,
  PRIMARY KEY (`username`),
  KEY `employee` (`employee`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `owners`
--

CREATE TABLE IF NOT EXISTS `owners` (
  `owner_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `phone1` varchar(45) NOT NULL,
  `phone2` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `is_trader` tinyint(1) DEFAULT NULL,
  `is_client` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`owner_id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `phone1` (`phone1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `points`
--

CREATE TABLE IF NOT EXISTS `points` (
  `proprety` varchar(45) DEFAULT NULL,
  `points` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE IF NOT EXISTS `projects` (
  `project_id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `projects_pieces`
--

CREATE TABLE IF NOT EXISTS `projects_pieces` (
  `project_id` int(11) NOT NULL,
  `proprety` int(11) NOT NULL,
  KEY `project_id` (`project_id`),
  KEY `proprety` (`proprety`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `propreties`
--

CREATE TABLE IF NOT EXISTS `propreties` (
  `proprety` int(11) NOT NULL,
  `type` varchar(45) NOT NULL,
  `area` float NOT NULL,
  `price` float NOT NULL,
  `details` longtext,
  `owner` int(11) NOT NULL,
  `street` int(11) NOT NULL,
  `block` int(11) NOT NULL,
  `city` int(11) NOT NULL,
  PRIMARY KEY (`proprety`),
  KEY `owner` (`owner`),
  KEY `city` (`city`),
  KEY `street` (`street`),
  KEY `block` (`block`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE IF NOT EXISTS `requests` (
  `client` int(11) NOT NULL,
  `piece` int(11) NOT NULL,
  KEY `client` (`client`),
  KEY `piece` (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `service_building`
--

CREATE TABLE IF NOT EXISTS `service_building` (
  `name` varchar(45) NOT NULL,
  `num_of_floors` int(11) NOT NULL,
  `num_of_units` int(11) NOT NULL,
  `trading` tinyint(1) DEFAULT NULL,
  `managing` tinyint(1) DEFAULT NULL,
  `apartment` tinyint(1) DEFAULT NULL,
  `piece` int(11) NOT NULL,
  PRIMARY KEY (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `service_unit`
--

CREATE TABLE IF NOT EXISTS `service_unit` (
  `unit_name` varchar(45) DEFAULT NULL,
  `trading` tinyint(1) DEFAULT NULL,
  `managing` tinyint(1) DEFAULT NULL,
  `apartment` tinyint(1) DEFAULT NULL,
  `building` int(11) NOT NULL,
  `piece` int(11) NOT NULL,
  KEY `building` (`building`),
  KEY `piece` (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `shifts`
--

CREATE TABLE IF NOT EXISTS `shifts` (
  `day_date` date NOT NULL,
  `begin_time` time NOT NULL,
  `end_time` time NOT NULL,
  `client` int(11) NOT NULL,
  KEY `client` (`client`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `streets`
--

CREATE TABLE IF NOT EXISTS `streets` (
  `street_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `num_of_blocks` int(11) DEFAULT NULL,
  `city` int(11) NOT NULL,
  PRIMARY KEY (`street_id`),
  UNIQUE KEY `name` (`name`),
  KEY `city_streets` (`city`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `streets`
--

INSERT INTO `streets` (`street_id`, `name`, `num_of_blocks`, `city`) VALUES
(2, 'العباسى', 9, 3);

-- --------------------------------------------------------

--
-- Table structure for table `villa`
--

CREATE TABLE IF NOT EXISTS `villa` (
  `num_of_floors` int(11) DEFAULT NULL,
  `ta4teb_type` varchar(45) DEFAULT NULL,
  `villa_type` varchar(45) DEFAULT NULL,
  `gaz` tinyint(1) DEFAULT NULL,
  `water` tinyint(1) DEFAULT NULL,
  `electricity` tinyint(1) DEFAULT NULL,
  `piece` int(11) NOT NULL,
  PRIMARY KEY (`piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `contracts`
--
ALTER TABLE `contracts`
  ADD CONSTRAINT `contracts_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `owners` (`owner_id`),
  ADD CONSTRAINT `contracts_ibfk_2` FOREIGN KEY (`client`) REFERENCES `clients` (`client_id`),
  ADD CONSTRAINT `contracts_ibfk_3` FOREIGN KEY (`employee`) REFERENCES `employee` (`emp_id`),
  ADD CONSTRAINT `contracts_ibfk_4` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `contracts_rents`
--
ALTER TABLE `contracts_rents`
  ADD CONSTRAINT `contracts_rents_ibfk_1` FOREIGN KEY (`contract`) REFERENCES `contracts` (`contract_id`);

--
-- Constraints for table `doplex`
--
ALTER TABLE `doplex`
  ADD CONSTRAINT `doplex_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `flat` (`piece`);

--
-- Constraints for table `eductional`
--
ALTER TABLE `eductional`
  ADD CONSTRAINT `eductional_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `emara`
--
ALTER TABLE `emara`
  ADD CONSTRAINT `emara_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `factories`
--
ALTER TABLE `factories`
  ADD CONSTRAINT `factories_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `flat`
--
ALTER TABLE `flat`
  ADD CONSTRAINT `flat_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`),
  ADD CONSTRAINT `flat_ibfk_2` FOREIGN KEY (`container`) REFERENCES `emara` (`piece`),
  ADD CONSTRAINT `flat_ibfk_3` FOREIGN KEY (`container`) REFERENCES `villa` (`piece`);

--
-- Constraints for table `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `lands`
--
ALTER TABLE `lands`
  ADD CONSTRAINT `lands_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `login_info`
--
ALTER TABLE `login_info`
  ADD CONSTRAINT `login_info_ibfk_1` FOREIGN KEY (`employee`) REFERENCES `employee` (`emp_id`);

--
-- Constraints for table `projects_pieces`
--
ALTER TABLE `projects_pieces`
  ADD CONSTRAINT `projects_pieces_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  ADD CONSTRAINT `projects_pieces_ibfk_2` FOREIGN KEY (`proprety`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `propreties`
--
ALTER TABLE `propreties`
  ADD CONSTRAINT `propreties_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `owners` (`owner_id`),
  ADD CONSTRAINT `propreties_ibfk_2` FOREIGN KEY (`city`) REFERENCES `cities` (`city_id`),
  ADD CONSTRAINT `propreties_ibfk_3` FOREIGN KEY (`street`) REFERENCES `streets` (`street_id`),
  ADD CONSTRAINT `propreties_ibfk_4` FOREIGN KEY (`block`) REFERENCES `blocks` (`block_id`);

--
-- Constraints for table `requests`
--
ALTER TABLE `requests`
  ADD CONSTRAINT `requests_ibfk_1` FOREIGN KEY (`client`) REFERENCES `clients` (`client_id`),
  ADD CONSTRAINT `requests_ibfk_2` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `service_building`
--
ALTER TABLE `service_building`
  ADD CONSTRAINT `service_building_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `service_unit`
--
ALTER TABLE `service_unit`
  ADD CONSTRAINT `service_unit_ibfk_1` FOREIGN KEY (`building`) REFERENCES `service_building` (`piece`),
  ADD CONSTRAINT `service_unit_ibfk_2` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);

--
-- Constraints for table `shifts`
--
ALTER TABLE `shifts`
  ADD CONSTRAINT `shifts_ibfk_1` FOREIGN KEY (`client`) REFERENCES `clients` (`client_id`);

--
-- Constraints for table `streets`
--
ALTER TABLE `streets`
  ADD CONSTRAINT `city_streets` FOREIGN KEY (`city`) REFERENCES `cities` (`city_id`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Constraints for table `villa`
--
ALTER TABLE `villa`
  ADD CONSTRAINT `villa_ibfk_1` FOREIGN KEY (`piece`) REFERENCES `propreties` (`proprety`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
