#todo : таблица день - преп, таблица преподавателей
def findInDatabase(conn, name):
    cur = connection.cursor()
    cur.execute("""select name, href from prepods where name LIKE %(name)s""", {'name' : name})
    result = cur.fetchmany()
    cur.close();
    return result;

def insertIntoPrepods(con, name, href):
  cur = connection.cursor()
  result = cur.execute("""insert into Prepods values(%(name)s, %(href)s)""", {'name': name, 'href': href})
  cur.close();
  return result;

def insertIntoStats(con, date, name):
    cur = connection.cursor()
    cur.execute("""select id from prepods where name=%(name)s""", {'name' : name})
    result = cur.fetchone();
    result = cur.execute("""insert into Stats values(%(date)s, %(prepod_id)s)""", {'date': date, 'prepod_id' : result})
    cur.close();
    return result;
