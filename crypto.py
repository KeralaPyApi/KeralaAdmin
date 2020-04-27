import BotClient

from datetime import datetime

cf = datetime.now()
BotClient.new("Token", "send_message")
cs = datetime.now()
print(f"{(cs - cf).microseconds / 1000} ms")

pf = datetime.now()
print("successful login Token\nMethod send")
ps = datetime.now()
print(f"{(ps - pf).microseconds / 1000} ms")
