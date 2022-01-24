CREATE DATABASE /*!32312 IF NOT EXISTS*/ `speedtest` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `speedtest`;

DROP TABLE IF EXISTS `speedtest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `speedtest` (
  `test_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `datetime` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` int(11) NOT NULL,
  `ping_jitter` float unsigned DEFAULT NULL,
  `ping_latency` float unsigned DEFAULT NULL,
  `download_bandwidth` int(10) unsigned DEFAULT NULL,
  `download_bytes` int(10) unsigned DEFAULT NULL,
  `download_elapsed` int(10) unsigned DEFAULT NULL,
  `upload_bandwidth` int(10) unsigned DEFAULT NULL,
  `upload_bytes` int(10) unsigned DEFAULT NULL,
  `upload_elapsed` int(10) unsigned DEFAULT NULL,
  `packetloss` int(10) unsigned DEFAULT NULL,
  `server_id` int(10) unsigned DEFAULT NULL,
  `server_host` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `server_port` int(10) unsigned DEFAULT NULL,
  `server_name` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `server_location` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `server_country` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `server_ip` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`test_id`),
  UNIQUE KEY `data_id_UNIQUE` (`test_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

