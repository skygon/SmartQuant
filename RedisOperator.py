import redis
import json

class RedisOperator(object):
    def __init__(self, host, port, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.con = redis.Redis(host=self.host, port=self.port, db=self.db)

    #=====Emhancement operator functions=============#
    def hsetJson(self, table, field, value):
        s = json.dumps(value)
        self.con.hset(table, field, s)

    def rpushJson(self, index_list, value):
        s = json.dumps(value)
        return self.con.rpush(index_list, s)
    
    #==== redis command wrapper=======================#
    def hkeys(self, table):
        return self.con.hkeys(table)
    
    def hset(self, table, field, value):
        return self.con.hset(table, field, value)
    
    def hget(self, table, field):
        return self.con.hget(table, field)
    
    def hlen(self, table):
        return self.con.hlen(table)
    
    def llen(self, index_list):
        return self.con.llen(index_list)

    def lindex(self, index_list, index):
        return self.con.lindex(index_list, index)
    
    def rpush(self, index_list, index):
        return self.con.rpush(index_list, index)
    

if __name__ == "__main__":
    r = RedisOperator("localhost", 6379, 0)
    data = r.lindex('index_2', 3)
    print data
    print json.loads(data)
    

    
