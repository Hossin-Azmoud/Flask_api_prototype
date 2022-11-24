from __init__ import (
	EncodeJWT,
	VerifyJWT
)


def main():
	s = "Key"
	Enc = EncodeJWT(s, {
		"Some": "paylaod"
	})
	print(Enc)
	Dec = VerifyJWT(s, Enc + "sss")
	print(Dec)
	print(type(Dec))




if __name__ == '__main__':
	main()