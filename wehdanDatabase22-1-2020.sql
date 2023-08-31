-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 22, 2020 at 01:26 PM
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
CREATE DATABASE IF NOT EXISTS `properties` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `properties`;

-- --------------------------------------------------------

--
-- Table structure for table `blocks`
--

CREATE TABLE `blocks` (
  `block_id` int(11) NOT NULL,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `num_of_pieces` int(11) DEFAULT NULL,
  `street` int(11) NOT NULL,
  `city` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `blocks`
--

INSERT INTO `blocks` (`block_id`, `name`, `num_of_pieces`, `street`, `city`) VALUES
(1, 'الاول', 20, 5, 2),
(2, 'الثانى', 80, 5, 2);

-- --------------------------------------------------------

--
-- Table structure for table `cities`
--

CREATE TABLE `cities` (
  `city_id` int(11) NOT NULL,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `mohafza` varchar(45) CHARACTER SET utf8 NOT NULL,
  `num_of_streets` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

CREATE TABLE `clients` (
  `client_id` int(11) NOT NULL,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `phone1` varchar(45) CHARACTER SET utf8 NOT NULL,
  `phone2` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `address` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `email` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `is_owner` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `working` varchar(10) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`client_id`, `name`, `phone1`, `phone2`, `address`, `email`, `is_owner`, `working`) VALUES
(2, 'هشام سعد', '01225147332', '01005008070', 'سمنود', 'hesham@mail.com', 'نعم', 'no'),
(4, 'احمد عثمان', '01123694046', '01123694046', 'سمنود', 'ahmed@mail.com', 'نعم', 'yes'),
(5, 'احمد هشام', '01286615294', '01123694046', 'سمنود', 'ahmedneo@mail.com', 'نعم', 'yes'),
(6, 'محمود عبدالناصر', '01168053169', '', 'المنصوره', 'maho@mail.com', 'لا', 'yes'),
(7, 'السيد المنشاوى', '01145096174', '', 'سماحة سمنود', 'sayed@mail.com', 'لا', 'yes');

-- --------------------------------------------------------

--
-- Table structure for table `contracts`
--

CREATE TABLE `contracts` (
  `contract_id` int(11) NOT NULL,
  `type` varchar(45) NOT NULL,
  `price` float NOT NULL,
  `date_` date NOT NULL,
  `owner` int(11) NOT NULL,
  `client` int(11) NOT NULL,
  `employee` int(11) NOT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `contracts_rents`
--

CREATE TABLE `contracts_rents` (
  `duration` int(11) NOT NULL,
  `rent_price` float NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `pre_price` float DEFAULT NULL,
  `paid_monthes` int(11) DEFAULT NULL,
  `contract` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `doplex`
--

CREATE TABLE `doplex` (
  `doplex_type` varchar(45) DEFAULT NULL,
  `pool` tinyint(1) DEFAULT NULL,
  `special_enter` tinyint(1) DEFAULT NULL,
  `inner_stairs` tinyint(1) DEFAULT NULL,
  `garden` tinyint(1) DEFAULT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `eductional`
--

CREATE TABLE `eductional` (
  `type` varchar(45) NOT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `emara`
--

CREATE TABLE `emara` (
  `num_of_floors` int(11) DEFAULT NULL,
  `ta4teb_type` varchar(45) DEFAULT NULL,
  `gaz` tinyint(1) DEFAULT NULL,
  `water` tinyint(1) DEFAULT NULL,
  `electricity` tinyint(1) DEFAULT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `emp_id` int(11) NOT NULL,
  `ID_Num` varchar(20) CHARACTER SET utf8 NOT NULL,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `phone` varchar(45) CHARACTER SET utf8 NOT NULL,
  `email` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `address` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `department` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `salary` float NOT NULL,
  `start_date` date DEFAULT NULL,
  `working` varchar(10) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`emp_id`, `ID_Num`, `name`, `phone`, `email`, `address`, `department`, `salary`, `start_date`, `working`) VALUES
(1, '2981101600994', 'احمد هشام', '01123694046', 'ahmedneo@gmail.com', 'سمنود', 'قسم3', 10000, '2018-02-11', 'yes'),
(9, '2981101600996', 'احمد هشام عثمان', '01123694033', 'ahmedneo117@gmail.com', 'المنصوره', 'قسم2', 9000, '2018-02-08', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `factories`
--

CREATE TABLE `factories` (
  `type` varchar(45) NOT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `flat`
--

CREATE TABLE `flat` (
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
  `container` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `image` longtext,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `lands`
--

CREATE TABLE `lands` (
  `land_status` varchar(45) NOT NULL,
  `land_type` varchar(45) NOT NULL,
  `details` longtext,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `login_info`
--

CREATE TABLE `login_info` (
  `username` varchar(45) NOT NULL,
  `password_` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `employee` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `persons`
--

CREATE TABLE `persons` (
  `owner_id` int(11) NOT NULL,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `phone1` varchar(45) CHARACTER SET utf8 NOT NULL,
  `phone2` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `email` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `address` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `is_trader` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `is_client` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `is_owner` varchar(10) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `persons`
--

INSERT INTO `persons` (`owner_id`, `name`, `phone1`, `phone2`, `email`, `address`, `is_trader`, `is_client`, `is_owner`) VALUES
(2, 'هشام سعد', '01225147332', '01005008070', 'hesham@mail.com', 'سمنود', 'نعم', 'نعم', 'نعم'),
(3, 'احمد عثمان', '01123694046', '01123694046', 'ahmed@mail.com', 'سمنود', 'نعم', 'لا', 'نعم'),
(4, 'أحمد العزب', '01165119077', '', 'ahmedazab@mail.com', 'القاهرة الجديده', 'لا', 'لا', 'نعم'),
(5, 'احمد هشام', '01286615294', '01123694046', 'ahmedneo@mail.com', 'سمنود', 'لا', 'نعم', 'نعم'),
(9, 'السيد المنشاوى', '01167189942', '', 'sayed@mail.com', 'سماحة', NULL, 'نعم', 'لا');

-- --------------------------------------------------------

--
-- Table structure for table `points`
--

CREATE TABLE `points` (
  `proprety` varchar(45) DEFAULT NULL,
  `points` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `project_id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `projects_pieces`
--

CREATE TABLE `projects_pieces` (
  `project_id` int(11) NOT NULL,
  `proprety` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `propreties`
--

CREATE TABLE `propreties` (
  `proprety` int(11) NOT NULL,
  `type` varchar(45) NOT NULL,
  `area` float NOT NULL,
  `price` float NOT NULL,
  `details` longtext,
  `owner` int(11) NOT NULL,
  `street` int(11) NOT NULL,
  `block` int(11) NOT NULL,
  `city` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `client` int(11) NOT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `service_building`
--

CREATE TABLE `service_building` (
  `name` varchar(45) NOT NULL,
  `num_of_floors` int(11) NOT NULL,
  `num_of_units` int(11) NOT NULL,
  `trading` tinyint(1) DEFAULT NULL,
  `managing` tinyint(1) DEFAULT NULL,
  `apartment` tinyint(1) DEFAULT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `service_unit`
--

CREATE TABLE `service_unit` (
  `unit_name` varchar(45) DEFAULT NULL,
  `trading` tinyint(1) DEFAULT NULL,
  `managing` tinyint(1) DEFAULT NULL,
  `apartment` tinyint(1) DEFAULT NULL,
  `building` int(11) NOT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `shifts`
--

CREATE TABLE `shifts` (
  `day_date` date NOT NULL,
  `begin_time` time NOT NULL,
  `end_time` time NOT NULL,
  `client` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `streets`
--

CREATE TABLE `streets` (
  `street_id` int(11) NOT NULL,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `num_of_blocks` int(11) DEFAULT NULL,
  `city` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `streets`
--

INSERT INTO `streets` (`street_id`, `name`, `num_of_blocks`, `city`) VALUES
(2, 'العباسى', 9, 3),
(5, 'السيدة زينب', 10, 2);

-- --------------------------------------------------------

--
-- Table structure for table `villa`
--

CREATE TABLE `villa` (
  `num_of_floors` int(11) DEFAULT NULL,
  `ta4teb_type` varchar(45) DEFAULT NULL,
  `villa_type` varchar(45) DEFAULT NULL,
  `gaz` tinyint(1) DEFAULT NULL,
  `water` tinyint(1) DEFAULT NULL,
  `electricity` tinyint(1) DEFAULT NULL,
  `piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `blocks`
--
ALTER TABLE `blocks`
  ADD PRIMARY KEY (`block_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `cities`
--
ALTER TABLE `cities`
  ADD PRIMARY KEY (`city_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`client_id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `phone1` (`phone1`);

--
-- Indexes for table `contracts`
--
ALTER TABLE `contracts`
  ADD PRIMARY KEY (`contract_id`),
  ADD KEY `owner` (`owner`),
  ADD KEY `client` (`client`),
  ADD KEY `employee` (`employee`),
  ADD KEY `piece` (`piece`);

--
-- Indexes for table `contracts_rents`
--
ALTER TABLE `contracts_rents`
  ADD KEY `contract` (`contract`);

--
-- Indexes for table `doplex`
--
ALTER TABLE `doplex`
  ADD KEY `piece` (`piece`);

--
-- Indexes for table `eductional`
--
ALTER TABLE `eductional`
  ADD KEY `piece` (`piece`);

--
-- Indexes for table `emara`
--
ALTER TABLE `emara`
  ADD PRIMARY KEY (`piece`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`emp_id`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD UNIQUE KEY `ID_Num` (`ID_Num`);

--
-- Indexes for table `factories`
--
ALTER TABLE `factories`
  ADD KEY `piece` (`piece`);

--
-- Indexes for table `flat`
--
ALTER TABLE `flat`
  ADD PRIMARY KEY (`piece`),
  ADD KEY `container` (`container`);

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD KEY `piece` (`piece`);

--
-- Indexes for table `lands`
--
ALTER TABLE `lands`
  ADD KEY `piece` (`piece`);

--
-- Indexes for table `login_info`
--
ALTER TABLE `login_info`
  ADD PRIMARY KEY (`username`),
  ADD KEY `employee` (`employee`);

--
-- Indexes for table `persons`
--
ALTER TABLE `persons`
  ADD PRIMARY KEY (`owner_id`),
  ADD UNIQUE KEY `phone1` (`phone1`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`project_id`);

--
-- Indexes for table `projects_pieces`
--
ALTER TABLE `projects_pieces`
  ADD KEY `project_id` (`project_id`),
  ADD KEY `proprety` (`proprety`);

--
-- Indexes for table `propreties`
--
ALTER TABLE `propreties`
  ADD PRIMARY KEY (`proprety`),
  ADD KEY `owner` (`owner`),
  ADD KEY `city` (`city`),
  ADD KEY `street` (`street`),
  ADD KEY `block` (`block`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD KEY `client` (`client`),
  ADD KEY `piece` (`piece`);

--
-- Indexes for table `service_building`
--
ALTER TABLE `service_building`
  ADD PRIMARY KEY (`piece`);

--
-- Indexes for table `service_unit`
--
ALTER TABLE `service_unit`
  ADD KEY `building` (`building`),
  ADD KEY `piece` (`piece`);

--
-- Indexes for table `shifts`
--
ALTER TABLE `shifts`
  ADD KEY `client` (`client`);

--
-- Indexes for table `streets`
--
ALTER TABLE `streets`
  ADD PRIMARY KEY (`street_id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `city_streets` (`city`);

--
-- Indexes for table `villa`
--
ALTER TABLE `villa`
  ADD PRIMARY KEY (`piece`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `blocks`
--
ALTER TABLE `blocks`
  MODIFY `block_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `cities`
--
ALTER TABLE `cities`
  MODIFY `city_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `clients`
--
ALTER TABLE `clients`
  MODIFY `client_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `emp_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `persons`
--
ALTER TABLE `persons`
  MODIFY `owner_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `streets`
--
ALTER TABLE `streets`
  MODIFY `street_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `contracts`
--
ALTER TABLE `contracts`
  ADD CONSTRAINT `contracts_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `persons` (`owner_id`),
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
  ADD CONSTRAINT `propreties_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `persons` (`owner_id`),
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
