-- phpMyAdmin SQL Dump
-- version 3.5.8.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 06, 2014 at 03:49 PM
-- Server version: 5.5.34-0ubuntu0.13.04.1
-- PHP Version: 5.4.9-4ubuntu2.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `cryptotrends`
--

-- --------------------------------------------------------

--
-- Table structure for table `currencypair`
--

CREATE TABLE IF NOT EXISTS `currencypair` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `exchange_id` bigint(20) NOT NULL,
  `code` varchar(135) NOT NULL,
  `name` varchar(765) NOT NULL,
  `api_url` varchar(765) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `currencypair_3800f639` (`exchange_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=101 ;

-- --------------------------------------------------------

--
-- Table structure for table `exchange`
--

CREATE TABLE IF NOT EXISTS `exchange` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(135) NOT NULL,
  `name` varchar(765) NOT NULL,
  `url` varchar(765) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Table structure for table `quote`
--

CREATE TABLE IF NOT EXISTS `quote` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `exchange_id` bigint(20) NOT NULL,
  `currencypair_id` bigint(20) NOT NULL,
  `created` datetime NOT NULL,
  `units` varchar(45) DEFAULT NULL,
  `last` double NOT NULL,
  `high` double NOT NULL,
  `low` double NOT NULL,
  `volume` double NOT NULL,
  `average` double NOT NULL,
  `bid` double NOT NULL,
  `ask` double NOT NULL,
  `mv_avg_10_min` double(10,6) DEFAULT NULL,
  `mv_avg_30_min` double(10,6) DEFAULT NULL,
  `mv_avg_60_min` double(10,6) DEFAULT NULL,
  `mv_avg_240_min` double(10,6) DEFAULT NULL,
  `mv_avg_600_min` double(10,6) DEFAULT NULL,
  `mv_avg_1_day` double DEFAULT NULL,
  `mv_avg_2_day` double DEFAULT NULL,
  `mv_avg_5_day` double DEFAULT NULL,
  `mv_avg_10_day` double DEFAULT NULL,
  `timsestamp` int(11) NOT NULL DEFAULT '0',
  `timestamp` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_quote_currencypair` (`currencypair_id`),
  KEY `fk_quote_exchange` (`exchange_id`),
  KEY `created` (`created`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6938332 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `currencypair`
--
ALTER TABLE `currencypair`
  ADD CONSTRAINT `exchange_id_refs_id_318a24e5` FOREIGN KEY (`exchange_id`) REFERENCES `exchange` (`id`);

--
-- Constraints for table `quote`
--
ALTER TABLE `quote`
  ADD CONSTRAINT `fk_quote_currencypair` FOREIGN KEY (`currencypair_id`) REFERENCES `currencypair` (`id`),
  ADD CONSTRAINT `fk_quote_exchange` FOREIGN KEY (`exchange_id`) REFERENCES `exchange` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
