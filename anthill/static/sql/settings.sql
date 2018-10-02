CREATE TABLE `settings` (
  `gamespace_id` int(11) unsigned NOT NULL,
  `deployment_method` varchar(64) NOT NULL DEFAULT '',
  `deployment_data` json NOT NULL,
  PRIMARY KEY (`gamespace_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;