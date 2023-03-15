CREATE TABLE `spiderlist_monitor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `spider_name` varchar(255) DEFAULT NULL,
  `spider_path` varchar(255) DEFAULT NULL,
  `pages` varchar(255) DEFAULT NULL,
  `run_time` varchar(255) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL,
  `is_run` varchar(50) DEFAULT NULL,
  `start_time` varchar(50) DEFAULT NULL,
  `end_time` varchar(50) DEFAULT NULL,
  `remarks` varchar(50) DEFAULT NULL,
  `add_time` varchar(50) DEFAULT NULL,
  `log_path` varchar(255) DEFAULT NULL,
  `is_new` varchar(10) DEFAULT NULL,
  `sign` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5476 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;