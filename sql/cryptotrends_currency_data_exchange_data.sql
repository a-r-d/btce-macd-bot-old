-- phpMyAdmin SQL Dump
-- version 3.5.8.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 06, 2014 at 03:50 PM
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

--
-- Dumping data for table `currencypair`
--

INSERT INTO `currencypair` (`id`, `exchange_id`, `code`, `name`, `api_url`) VALUES
(1, 1, 'LTC_USD', 'Litecoins per dollar', 'https://btc-e.com/api/2/ltc_usd/ticker'),
(2, 1, 'LTC_BTC', 'Litecoins per bitcoin', 'https://btc-e.com/api/2/ltc_btc/ticker'),
(3, 1, 'BTC_USD', 'Bitcoins per dollar.', 'https://btc-e.com/api/2/btc_usd/ticker'),
(4, 1, 'BTC_EUR', 'Bitcoins per Euro.', 'https://btc-e.com/api/2/btc_eur/ticker'),
(5, 1, 'PPC_BTC', 'Peercoin per bitcoin.', 'https://btc-e.com/api/2/ppc_btc/ticker'),
(6, 1, 'NMC_BTC', 'Namecoin per bitcoin.', 'https://btc-e.com/api/2/nmc_btc/ticker'),
(7, 1, 'NMC_BTC', 'Namecoins per bitcoin.', 'https://btc-e.com/api/2/nmc_btc/ticker'),
(8, 1, 'TRC_BTC', 'Terracoins per bitcoin.', 'https://btc-e.com/api/2/trc_btc/ticker'),
(9, 1, 'NVC_BTC', 'Novacoins per bitcoin.', 'https://btc-e.com/api/2/nvc_btc/ticker'),
(10, 1, 'XPM_BTC', 'XPM per bitcoin.', 'https://btc-e.com/api/2/xpm_btc/ticker'),
(11, 1, 'NVC_USD', 'Novacoin Per Dollar.', 'https://btc-e.com/api/2/nvc_btc/ticker'),
(12, 1, 'NMC_USD', 'Namecoin Per Dollar.', 'https://btc-e.com/api/2/nmc_btc/ticker'),
(50, 2, 'LTC_BTC', 'Litecoin Per Bitcoin', 'https://bter.com/api/1/ticker/ltc_btc'),
(51, 2, 'FTC_BTC', 'Feathercoin Per Bitcoin', 'https://bter.com/api/1/ticker/ftc_btc'),
(52, 2, 'PPC_BTC', 'PPCoin Per Bitcoin', 'https://bter.com/api/1/ticker/ppc_btc'),
(53, 2, 'CNC_BTC', 'Chinacoin Per Bitcoin', 'https://bter.com/api/1/ticker/cnc_btc'),
(100, 4, 'BTC_USD', 'Dollars per bitcoin', 'http://data.mtgox.com/api/1/BTCUSD/ticker');

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

--
-- Dumping data for table `exchange`
--

INSERT INTO `exchange` (`id`, `code`, `name`, `url`) VALUES
(1, 'BTCE', 'BTC-e.com Alt Coin Exchange', 'https://btc-e.com/'),
(2, 'BTER', 'Bter.com Alt Coin Exchange', 'http://bter.com/'),
(3, 'VCX', 'VirCurEx - Virtual Currency Exchange', 'http://vircurex.com'),
(4, 'MTGOX', 'mtgox', 'http://mtgox.com');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `currencypair`
--
ALTER TABLE `currencypair`
  ADD CONSTRAINT `exchange_id_refs_id_318a24e5` FOREIGN KEY (`exchange_id`) REFERENCES `exchange` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
