import redis

conn = redis.Redis(host='127.0.0.1', port=6379)


def append_shopping_cart(user_id, commodity_id, number):
    conn.hset(user_id, commodity_id, number)

def get_user_shaopping_cart(user_id):
    a=conn.hgetall(user_id)
    return a

def delete_shopping_cart(user_id):
    conn.delete(user_id)