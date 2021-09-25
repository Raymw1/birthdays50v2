from models.Birthday import getBirth, getSharedBirths
from models.User import getUser

def formatSharedBirthdays(receiver_id):
  births = getSharedBirths(receiver_id)
  users = {}
  for birth in births:
    try:
      users[getSenderName(birth["sender_id"])].append(getBirth(birth["birthday_id"])[0])
    except:
      users[getSenderName(birth["sender_id"])] = getBirth(birth["birthday_id"])
  print(users)
  return users

def getSenderName(sender_id):
  sender = getUser(sender_id)
  return sender[0]["username"]
