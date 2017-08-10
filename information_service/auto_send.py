import itchat, time
from itchat.content import *
import time

itchat.auto_login(False)
#print itchat.get_friends('skycuiluo')
author = itchat.search_friends(nickName='skygon')[0]
author.send('greeting, skycuiluo!')

itchat.send_msg("hello world", toUserName="@cefaa7f2ca6905f870a3e54147f46f6f")
itchat.run(True)

time.sleep(10)