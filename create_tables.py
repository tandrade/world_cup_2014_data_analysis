import MySQLdb as mdb


NO_PK_TABLES = {} 
PK_TABLES = {} 

PK_TABLES['players'] = ('''
CREATE TABLE `players` ( 
`player_id` int(6) NOT NULL AUTO_INCREMENT, 
`squad_number` varchar(120),
`league_number` varchar(120), 
`name` varchar(120) NOT NULL, 
`position` varchar(120), 
`club_id` int(6) NOT NULL, 
`team_id` int(6) NOT NULL, 
PRIMARY KEY (`player_id`), 
CONSTRAINT `players_ibfk_1` FOREIGN KEY (`club_id`) 
  REFERENCES `clubs` (`club_id`) ON DELETE CASCADE, 
CONSTRAINT `players_ibfk_2` FOREIGN KEY (`team_id`) 
  REFERENCES `teams` (`team_id`) ON DELETE CASCADE
) ENGINE=InnoDB;'''
) 

PK_TABLES['matches'] = (
"CREATE TABLE `matches` (" 
" `a_team_id` int(6) NOT NULL,"  
" `b_team_id` int(6) NOT NULL,"
" `date` date," 
" `score_a_team` int(3) NOT NULL," 
" `score_b_team` int(3) NOT NULL," 
" `stage` varchar(100)," 
" PRIMARY KEY (`a_team_ID`, `b_team_id`, `date`)," 
" KEY `a_team_id` (`a_team_id`)," 
" KEY `b_team_id` (`b_team_id`)," 
" CONSTRAINT `matches_ibfk_1` FOREIGN KEY (`a_team_id`)" 
"   REFERENCES `teams` (`team_id`) ON DELETE CASCADE," 
" CONSTRAINT `matches_ibfk_2` FOREIGN KEY (`b_team_id`)" 
"  REFERENCES `teams` (`team_id`) ON DELETE CASCADE"
") ENGINE=InnoDB") 
 
NO_PK_TABLES['clubs'] = (''' 
CREATE TABLE `clubs` ( 
`club_id` int(6) NOT NULL AUTO_INCREMENT, 
`name` varchar(100) NOT NULL, 
PRIMARY KEY (`club_id`)
) ENGINE=InnoDB''')

NO_PK_TABLES['conferences'] = (
"CREATE TABLE `conferences` (" 
"  `conference_id` int(6) NOT NULL AUTO_INCREMENT," 
"  `name` varchar(100) NOT NULL," 
"   PRIMARY KEY (`conference_id`)" 
") ENGINE=InnoDB") 

PK_TABLES['conference_club_membership'] = (''' 
CREATE TABLE `conference_club_membership` ( 
`conference_id` int(6) NOT NULL AUTO_INCREMENT, 
`club_id` int(6) NOT NULL, 
PRIMARY KEY (`conference_id`, `club_id`), 
KEY `conference_id` (`conference_id`), 
KEY `club_id` (`club_id`), 
CONSTRAINT `conference_club_ibfk_1` FOREIGN KEY (`conference_id`)  
  REFERENCES `conferences` (`conference_id`) ON DELETE CASCADE, 
CONSTRAINT `conference_club_ibfk_2` FOREIGN KEY (`club_id`)  
  REFERENCES `clubs` (`club_id`) ON DELETE CASCADE
) ENGINE=InnoDB''') 
 
NO_PK_TABLES['teams'] = (''' 
CREATE TABLE `teams` ( 
`team_id` int(6) NOT NULL AUTO_INCREMENT, 
`name` varchar(100) NOT NULL, 
`region` varchar(10), 
PRIMARY KEY `team_id` (`team_id`)
) ENGINE=InnoDB''') 


try: 
  con = mdb.connect('localhost', 'admin', 'password', 'world_cup') 
  cur = con.cursor() 
  for name, command in NO_PK_TABLES.iteritems(): 
    cur.execute("DROP TABLE IF EXISTS %s" % name) 
    print "CREATING DATABASE: %s" % name 
    cur.execute(command) 
  for name, command in PK_TABLES.iteritems(): 
    cur.execute("DROP TABLE IF EXISTS %s" % name) 
    print 'CREATING DATABASE: %s' % name 
    cur.execute(command) 
except mdb.Error, e: 
  print "Error %d: %s" %(e. args[0], e.args[1]) 
finally: 
  if cur: 
    cur.close() 
  if con: 
    con.close() 
