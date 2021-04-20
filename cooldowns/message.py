import queue
import threading
import time
rateLimit = []
rateLimitQueue = queue.Queue()
def cooldown_add(user, cooldown_amount=3600):
    rateLimitQueue.put((user, time.time()+cooldown_amount))
    rateLimit.append(user)
def deleteLimit():
    while True:
        if rateLimitQueue.empty == True:
            time.sleep(1)
        else:
            latest = rateLimitQueue.get()
            current = round(time.time())
            expires = latest[1]
            if current >= expires:
                rateLimit.pop(0)
                continue
            else:
                time.sleep(expires-current)
                rateLimit.pop(0)
rateLimitThread = threading.Thread(target=deleteLimit)
rateLimitThread.start()