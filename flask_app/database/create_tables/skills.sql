CREATE TABLE IF NOT EXISTS `skills` (
`skill_id`        int(11)       NOT NULL AUTO_INCREMENT  COMMENT 'The skill id',
`experience_id`   int(11)       NOT NULL                 COMMENT 'The expierence where I obtained the skill',
`name`            varchar(100)  NOT NULL                 COMMENT 'The name of the skill',
`skill_level`     int(11)       NOT NULL                 COMMENT 'the level of the skill',
CONSTRAINT min_max_skill CHECK (skill_level >= 1 AND skill_level <= 10),  
PRIMARY KEY (`skill_id`),
FOREIGN KEY (experience_id) REFERENCES experiences(experience_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="skills I possess";