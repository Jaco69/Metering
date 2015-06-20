-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- Machine: localhost
-- Genereertijd: 20 jun 2015 om 13:51
-- Serverversie: 5.5.43
-- PHP-Versie: 5.4.4-14+deb7u7

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Databank: `emoncms`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `dashboard`
--

CREATE TABLE IF NOT EXISTS `dashboard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `content` text,
  `height` int(11) DEFAULT NULL,
  `name` varchar(30) DEFAULT 'no name',
  `alias` varchar(10) DEFAULT NULL,
  `description` varchar(255) DEFAULT 'no description',
  `main` tinyint(1) DEFAULT NULL,
  `public` tinyint(1) DEFAULT NULL,
  `published` tinyint(1) DEFAULT NULL,
  `showdescription` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- Gegevens worden uitgevoerd voor tabel `dashboard`
--

INSERT INTO `dashboard` (`id`, `userid`, `content`, `height`, `name`, `alias`, `description`, `main`, `public`, `published`, `showdescription`) VALUES
(1, 1, '<div pricekwh="0.21" currency="Eur" kwhd="2" power="1" id="7" class="zoom" style="position: absolute; margin: 0px; top: 20px; left: 0px; width: 1140px; height: 420px;"><iframe style="width: 940px; height: 420px;" marginheight="0" marginwidth="0" src="http://192.168.1.2/emoncms/vis/zoom?embed=1&amp;power=1&amp;kwhd=2&amp;currency=Eur&amp;pricekwh=0.21" scrolling="no" frameborder="0"></iframe></div>', 440, 'Verbruik', 'verbruik', 'Energie verbruik', 1, 1, 1, 1),
(7, 1, NULL, NULL, 'no name', '', 'no description', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `feeds`
--

CREATE TABLE IF NOT EXISTS `feeds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `userid` int(11) DEFAULT NULL,
  `tag` text,
  `time` datetime DEFAULT NULL,
  `value` float DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `datatype` int(11) NOT NULL,
  `public` tinyint(1) DEFAULT NULL,
  `size` int(11) NOT NULL,
  `engine` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Gegevens worden uitgevoerd voor tabel `feeds`
--

INSERT INTO `feeds` (`id`, `name`, `userid`, `tag`, `time`, `value`, `status`, `datatype`, `public`, `size`, `engine`) VALUES
(1, 'Verbruikt gemiddeld Watt per uur', 1, '', '2013-03-26 20:41:18', 38.2182, 0, 1, 1, 0, 0),
(2, 'Verbruikt kWh per dag', 1, '', '2013-03-26 20:41:18', 5.98004, 0, 2, 1, 0, 0),
(3, 'Verbruikt kWh per jaar', 1, '', '2013-03-26 20:41:18', 3413.76, 0, 1, 1, 0, 0),
(4, 'Geleverd gemiddeld Watt per uur', 1, '', '2013-03-26 20:41:18', 0, 0, 1, 1, 0, 0),
(5, 'Geleverd kWh per dag', 1, '', '2013-03-26 20:41:18', 0, 0, 2, 1, 0, 0),
(6, 'Geleverd kWh per jaar', 1, '', '2013-03-26 20:41:18', 0, 0, 1, 1, 0, 0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `feed_1`
--

CREATE TABLE IF NOT EXISTS `feed_1` (
  `time` int(10) unsigned NOT NULL DEFAULT '0',
  `data` float unsigned DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden uitgevoerd voor tabel `feed_1`
--

INSERT INTO `feed_1` (`time`, `data`) VALUES
(1434798000, 0.0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `feed_2`
--

CREATE TABLE IF NOT EXISTS `feed_2` (
  `time` int(10) unsigned NOT NULL DEFAULT '0',
  `data` float unsigned DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden uitgevoerd voor tabel `feed_2`
--

INSERT INTO `feed_2` (`time`, `data`) VALUES
(1434758400, 0.0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `feed_3`
--

CREATE TABLE IF NOT EXISTS `feed_3` (
  `time` int(10) unsigned NOT NULL DEFAULT '0',
  `data` float unsigned DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden uitgevoerd voor tabel `feed_3`
--

INSERT INTO `feed_3` (`time`, `data`) VALUES
(2015, 0.0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `feed_4`
--

CREATE TABLE IF NOT EXISTS `feed_4` (
  `time` int(10) unsigned NOT NULL DEFAULT '0',
  `data` float unsigned DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden uitgevoerd voor tabel `feed_4`
--

INSERT INTO `feed_4` (`time`, `data`) VALUES
(1434798000, 0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `feed_5`
--

CREATE TABLE IF NOT EXISTS `feed_5` (
  `time` int(10) unsigned NOT NULL DEFAULT '0',
  `data` float unsigned DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden uitgevoerd voor tabel `feed_5`
--

INSERT INTO `feed_5` (`time`, `data`) VALUES
(1434758400, 0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `feed_6`
--

CREATE TABLE IF NOT EXISTS `feed_6` (
  `time` int(10) unsigned NOT NULL DEFAULT '0',
  `data` float unsigned DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden uitgevoerd voor tabel `feed_6`
--

INSERT INTO `feed_6` (`time`, `data`) VALUES
(2013, 0),
(2014, 0),
(2015, 0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `input`
--

CREATE TABLE IF NOT EXISTS `input` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `name` text,
  `nodeid` int(11) DEFAULT NULL,
  `processList` text,
  `time` datetime DEFAULT NULL,
  `value` float DEFAULT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `multigraph`
--

CREATE TABLE IF NOT EXISTS `multigraph` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `userid` int(11) DEFAULT NULL,
  `feedlist` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Gegevens worden uitgevoerd voor tabel `multigraph`
--

INSERT INTO `multigraph` (`id`, `name`, `userid`, `feedlist`) VALUES
(1, '', 1, '[{"id":"1","name":"Elektriciteitsmeter verbruik","datatype":"1","timeWindow":2592000000,"end":0},{"id":"2","name":"Verbruik in Watt","datatype":"1"}]'),
(5, NULL, 1, '');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `myelectric`
--

CREATE TABLE IF NOT EXISTS `myelectric` (
  `userid` int(11) DEFAULT NULL,
  `data` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Gegevens worden uitgevoerd voor tabel `myelectric`
--

INSERT INTO `myelectric` (`userid`, `data`) VALUES
(1, '{"powerfeed":1,"dailyfeed":2,"dailytype":2}');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `node`
--

CREATE TABLE IF NOT EXISTS `node` (
  `userid` int(11) DEFAULT NULL,
  `data` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------
