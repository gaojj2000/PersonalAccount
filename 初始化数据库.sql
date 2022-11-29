/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50562
Source Host           : localhost:3306
Source Database       : zl

Target Server Type    : MYSQL
Target Server Version : 50562
File Encoding         : 65001

Date: 2021-07-11 08:11:12
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for income
-- ----------------------------
DROP TABLE IF EXISTS `income`;
CREATE TABLE `income` (
  `index` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `date` bigint(20) unsigned NOT NULL,
  `person` int(10) NOT NULL,
  `price` decimal(10,2) unsigned NOT NULL,
  `type` varchar(255) NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for person
-- ----------------------------
DROP TABLE IF EXISTS `person`;
CREATE TABLE `person` (
  `index` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `user` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `relation` varchar(255) NOT NULL,
  `admin` int(1) NOT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of person
-- ----------------------------
INSERT INTO `person` VALUES ('0000000001', '000001', '111111', '红妈妈', '母亲', '1');
INSERT INTO `person` VALUES ('0000000002', '000002', '222222', '小红', '弟弟', '0');
INSERT INTO `person` VALUES ('0000000003', '000003', '333333', '红爸爸', '父亲', '0');
INSERT INTO `person` VALUES ('0000000004', '000004', '444444', '红爷爷', '祖父', '0');
INSERT INTO `person` VALUES ('0000000005', '000005', '555555', '红奶奶', '祖母', '0');
INSERT INTO `person` VALUES ('0000000006', '000006', '666666', '大红', '哥哥', '0');
INSERT INTO `person` VALUES ('0000000007', '000007', '777777', '小蓝', '妹妹', '0');
INSERT INTO `person` VALUES ('0000000008', '000008', '888888', '大蓝', '姐姐', '0');

-- ----------------------------
-- Table structure for spend
-- ----------------------------
DROP TABLE IF EXISTS `spend`;
CREATE TABLE `spend` (
  `index` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `date` bigint(20) unsigned NOT NULL,
  `person` int(10) NOT NULL,
  `price` decimal(10,2) unsigned NOT NULL,
  `type` varchar(255) NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
