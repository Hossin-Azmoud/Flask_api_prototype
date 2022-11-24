import jwt


def EncodeJWT(key: str, data: dict) -> str:
	""" Encodes the Json web token and return a string repr to send to the client. """
	return jwt.encode(data, key, algorithm="HS256")


def VerifyJWT(key: str, Token: str) -> str | dict:
	""" Gets encoded JWT Token and tries to decode it and get the result, if not returns None.."""
	if isinstance(Token, str):
		Token = Token.encode()

	try:
		return jwt.decode(Token, key, algorithms=["HS256"])
	except Exception as e:
		return str(e) + "This Token is invalid"

def filteredUserList(q: str, users: list) -> list:
	""" gets a query and filters an Object of users. """
	res = []
	for i in users:
		if q.upper().strip() in i["UserName"].upper(): res.append(i)
	return res










