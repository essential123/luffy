import redis
pool=redis.ConnectionPool(max_connections=200,host='127.0.0.1',port=6379)