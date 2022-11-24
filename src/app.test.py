from requests import (
	get,
	post
)
from dataclasses import dataclass
from json import dumps, loads
from base64 import b64encode

def addUsers():

	with open("./TestData/Emails.txt") as fp:
		Emails = fp.readlines()
		count = 0
		for i in Emails:
			prefix, suffix = i.split("@")[0], b64encode(i.split("@")[0].encode()).decode()

			Data = {
				"UserName": prefix,
				"Email": i,
				"Password": suffix 
			}
						
			try:
				res = postToUrl(Data)
				count += 1
				print(f'added: {count} Users -> Now added {prefix}')

			except Exception as e:
				print(e)


def postToUrl(data: dict):
	EndPointUrl: str = "http://localhost:5000/signup"
	res = post(EndPointUrl, json=data)
	return res.json()

def AddAdminUser():
	return postToUrl({
		"UserName": "test",
		"Email": "ss@ssx.com",
		"Password": "hadajeids"
	})

def main(): pass

if __name__ == "__main__":
	res = AddAdminUser()
	print(res)

"""
hymed credintials:
	email: Hymen@gmail.com
	pwd: HaiMen1234
"""