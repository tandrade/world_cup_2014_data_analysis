# First, read in players docs
import os 
import re
import MySQLdb as mdb


#TODO: clean up code... 
#TODO: check data integrity 


SQUAD_DIR_RELATIVE_PATH = 'data/squads' 
MATCH_FILE_RELATIVE_PATH = 'data/cup_finals.txt' 
CURRENT_PATH = os.getcwd() 

################## PARSING FILES ######################################

PLAYER_NUMBER_REGEX = "^[ ]*\([0-9]+\)[ ]+" 
PLAYER_POSITION_REGEX = "^[A-Z]+[ ]+" 
PLAYER_NAME_REGEX = "[^#]+" 
PLAYER_POSITION_CLUB_REGEX = "[^0-9 ]+,"
PLAYER_LEAGUE_NO_REGEX = "##[ ]+[0-9]+"
LEAGUE_NAME_REGEX = ",[ ]+[^(]+"
LEAGUE_COUNTRY_REGEX = "\([A-Z ]+\)"


def get_number(line, playerinfo): 
  number = re.findall(PLAYER_NUMBER_REGEX, line)
  if not number: 
    return line, playerinfo 
  playerinfo["number"] = number[0].replace("(", "").replace(")", "")    
  return line[len(number[0]):], playerinfo 

def get_position(line, playerinfo): 
  pos = re.findall(PLAYER_POSITION_REGEX, line) 
  if not pos: 
    return line, {} 
  playerinfo["position"] = pos[0].strip() 
  return line[len(pos[0]):], playerinfo

def get_name(line, playerinfo): 
  name = re.findall(PLAYER_NAME_REGEX, line) 
  if not name: 
    return line, {} 
  playerinfo["name"] = name[0].strip() 
  return line[len(name[0]):], playerinfo 

def get_league_no(line, playerinfo): 
  num = re.findall(PLAYER_LEAGUE_NO_REGEX, line) 
  if not num: 
    return line, {}  
  playerinfo["league_no"] = num[0].replace("#", "").strip()
  return line[len(num[0]):], playerinfo
  
def get_league_name(line, playerinfo): 
  name = re.findall(LEAGUE_NAME_REGEX, line) 
  if not name: 
    return line, {} 
  playerinfo["league"] = name[0].replace(",", "").replace("'", "").strip() 
  return line[len(name[0]):], playerinfo 

def get_country_of_league(line, playerinfo): 
  country = re.findall(LEAGUE_COUNTRY_REGEX, line) 
  if not country: 
    return line, {} 
  playerinfo["league_country"] = (country[0].replace(")", "")
                                            .replace("(", "")
                                            .strip()) 
  return line[len(country[0]):], playerinfo  

def parse_text(line, playerinfo): 
  line, playerinfo = get_number(line, playerinfo) 
  if not playerinfo: 
    return {} 
  line, playerinfo = get_position(line, playerinfo)
  if not playerinfo: 
    return {} 
  line, playerinfo = get_name(line, playerinfo)
  if not playerinfo: 
    return {} 
  line, playerinfo = get_league_no(line, playerinfo) 
  if not playerinfo: 
    return {}  
  line, playerinfo = get_league_name(line, playerinfo) 
  if not playerinfo: 
    return {} 
  line, playerinfo = get_country_of_league(line, playerinfo) 
  if not playerinfo: 
    return {} 
  return playerinfo

########## UPDATING DB ###########################

def update_query(table_name, name):
  con = mdb.connect('localhost', 'admin', 'password', 'world_cup')
  cur = con.cursor()
  id_type = table_name[:-1] + "_id"
  cur.execute("SELECT %s FROM %s WHERE name='%s'" % (id_type, table_name, name))
  results = cur.fetchone()
  if results:
    con.close() 
    return results[0]
  cur.execute("INSERT INTO %s (name) VALUES ('%s')" % (table_name, name))
  con.commit()
  con.close()
  return cur.lastrowid
  
def store_league_info(conference_name): 
  return update_query("conferences", conference_name)  

def store_club_info(club_name): 
  return update_query("clubs", club_name)  

def store_player_results(results, country_id): 
  club_id = store_club_info(results["league"]) 
  if (club_id and country_id): 
    con = mdb.connect('localhost', 'admin', 'password', 'world_cup') 
    cur = con.cursor() 
    try:  
      cur.execute('''
          INSERT INTO players (squad_number, league_number, name, position, club_id, team_id) 
          VALUES ('%s', '%s', '%s', '%s', '%s', '%s')'''
          % (results["league_no"], results["number"], results["name"], results["position"], 
           club_id, country_id))
      con.commit() 
      con.close()  
    except mdb.Error, e: 
      print "Error %d: %s" %(e.args[0], e.args[1]) 
  else: 
    print "ERROR WILL ROBINSON", results 

def store_country_info(country_name): 
  return update_query("teams", country_name)  

def get_country_name(filename): 
  return filename[3:][:-4].replace("-", " ") 

#################################################333

team_files = os.path.join(CURRENT_PATH, SQUAD_DIR_RELATIVE_PATH) 
for team_file in os.listdir(team_files): 
  countryname = get_country_name(os.path.basename(team_file))
  if countryname: 
    team_id = store_country_info(countryname) 
    with open(os.path.join(team_files, team_file), 'r') as f: 
      text = f.readlines() #TODO: better way to do this? 
      for line in text: 
        playerinfo = {} 
        results = parse_text(line, playerinfo) 
        if results: 
          store_player_results(results, team_id)    


# Second, read in match data 

#match_file = os ( get file) 
#with open(match_file, r) as f: 
#  text = f.readlines() 
#  for line in text: 
#    match_results = parse_match_text(line) 
#    store_in_db(results)  
