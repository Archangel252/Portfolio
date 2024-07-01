CREATE TABLE IF NOT EXISTS `experiences` (
`experience_id`        int(11)       NOT NULL AUTO_INCREMENT  COMMENT 'The expierence id',
`position_id`          int(11)       NOT NULL 				  COMMENT 'FK:The position id',
`name`                 varchar(100)  NOT NULL				  COMMENT 'the name of this expierence',
`description`          varchar(500)  NOT NULL                 COMMENT 'a description of this expierence',
`hyperlink`            varchar(255)  NOT NULL                 COMMENT 'My start date for this position',
`start_date`           date          NOT NULL                 COMMENT 'My start date for this expierence',
`end_date`             date          DEFAULT NULL             COMMENT 'The end date for this expierence',
PRIMARY KEY (`experience_id`),
FOREIGN KEY (position_id) REFERENCES positions(position_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="expierences I have had";