/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.0.67-community-nt : Database - restaurant
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`restaurant` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `restaurant`;

/*Table structure for table `register` */

DROP TABLE IF EXISTS `register`;

CREATE TABLE `register` (
  `name` varchar(1000) default NULL,
  `email` varchar(1000) default NULL,
  `mobile` varchar(1000) default NULL,
  `username` varchar(1000) default NULL,
  `password` varchar(1000) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `register` */

insert  into `register`(`email`,`mobile`,`username`,`password`) values (1,'Kishan','gkvtechsolutions@gmail.com','09640257292','hyd','kishan','123');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
