import itchat, time
from itchat.content import *

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    res = "Recv: " + msg.text
    itchat.send_msg(res, "filehelper")

itchat.auto_login(True)
#print itchat.search_friends()
itchat.send_msg("hello world", "filehelper")
itchat.run(True)