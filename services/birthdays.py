from models.Birthday import getBirth, getSharedBirths
from models.User import getUser

def formatSharedBirthdays(receiver_id):
  births = getSharedBirths(receiver_id)
  users = {}
  for birth in births:
    birthToGet = getBirth(birth["birthday_id"])
    birthToGet[0]["share_id"] = birth["id"]
    try:
      users[getSenderName(birth["sender_id"])].append(birthToGet[0])
    except:
      users[getSenderName(birth["sender_id"])] = birthToGet
  return users

def getSenderName(sender_id):
  sender = getUser(sender_id)
  return sender[0]["username"]
