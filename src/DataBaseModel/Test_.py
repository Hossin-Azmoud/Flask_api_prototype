from Database import (
	constructDB
)



def main():
	db = constructDB("./db/Users.db")
	db.connect()
	users = db.GetAllUsers()
	print(users)



def jwtTest(json):
	encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
	print(encoded_jwt)
	print(jwt.decode(encoded_jwt, "secret", algorithms=["HS256"]))
	



if __name__ == '__main__':
	main()

