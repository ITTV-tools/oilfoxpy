import oilfox

api = oilfox.api("", "")
api.login()
print(api.getSummery())
