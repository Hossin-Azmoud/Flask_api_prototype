"""

This file is meant to interact with the database, fetch, post, delete and update fields in the db tables:
	
	- Posts
		
		ID INTEGER PRIMARY KEY AUTOINCREMENT, [0]
    	USER_ID INTEGER, [1]
  		Text TEXT,  [2]
  		IMG TEXT [3]

	- Users
		ID INTEGER PRIMARY KEY AUTOINCREMENT, [0]
		EMAIL TEXT, 
		USERNAME TEXT, 
		PASSWORDHASH TEXT, 
		TOKEN TEXT, 
		IMG TEXT DEFAULT null,
		BG TEXT DEFAULT null,
		BIO TEXT DEFAULT null,
		ADDR TEXT DEFAULT null

"""

import sqlite3
from enum import Enum
import logging
from pathlib import Path
from hashlib import sha256
from .Models import UserModel, response
from base64 import b64encode, b64decode
from dataclasses import dataclass
from random import randint

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

DBMAP_ = {
	"USERS": [
		"ID",
		"EMAIL",
		"USERNAME",
		"PASSWORDHASH",
		"TOKEN",
		"IMG"
	],
	
	"POST": [
		"ID",
		"USER_ID",
		"Text",
		"IMG"
	]
}

class DB:

	def __init__(self, dbPath: Path):
		assert dbPath.exists(), f"{dbPath} file does not exist"
		self.__Path = dbPath
		self.isOpen = False
		self.Blueprint: dict = DBMAP_

	def GetDataBaseBlueprint(self): return self.Blueprint
	
	def GetUserPosts(self, id_: int):
		rows = self.cursor.execute("SELECT Text, IMG FROM POSTS WHERE USER_ID=? ORDER BY ID DESC", (id_, )).fetchall()
		if rows:
			for i, row in enumerate(rows):
				rows[i] = {
					"Text": row[0],
					"IMG": row[1]
				}

			return rows
		else:
			return False

	def GetUserById(self, id_: int) -> dict | None:
		assert self.isOpen, "The db is not yet connected, Try again"
		row = self.cursor.execute("SELECT * FROM USERS WHERE ID=?", (id_, )).fetchone()

		if row:
			
			return {
				"id_": row[0],
				"UserName": row[2],
				"img": row[5],
				"bg": row[6],
				"bio": row[7],
				"addr": row[8]
			}

		else:
			return None
	
	def UpdateBio(self, newValue, id_):
		assert self.isOpen, "The db is not yet connected, Try again"
		row = self.cursor.execute("UPDATE USERS SET BIO=? WHERE ID=?", (newValue, id_)).fetchone()
		self.commit()
		return row



	def UpdateBackgound(self, newValue, id_) -> bool:
		assert self.isOpen, "The db is not yet connected, Try again"

		try:
			row = self.cursor.execute("UPDATE USERS SET BG=? WHERE ID=?", (newValue, id_)).fetchone()
			self.commit()
			return True
		except Exception as e:
			print(e)

		return False
		
	def UpdateImg(self, newValue, id_) -> bool:
		assert self.isOpen, "The db is not yet connected, Try again"
		try:
			row = self.cursor.execute("UPDATE USERS SET IMG=? WHERE ID=?", (newValue, id_))
			print(row)
			self.commit()
			return True
		except Exception as e:
			print(e)

		return False

	def UpdateUserName(self, newValue, id_):
		res = self.Update("USERNAME", newValue, id_)
		return res

	def Update(self, fieldname, fieldNewVal, id_:int):
		assert self.isOpen, "The db is not yet connected, Try again"
		row = self.cursor.execute("UPDATE USERS SET ?=? WHERE ID=?", (fieldname, fieldNewVal, id_)).fetchone()
		return row
	
	def UpdateAll(self, data: dict):
		assert self.isOpen, "The db is not yet connected, Try again"
		
		row = self.cursor.execute(
			"UPDATE USERS SET IMG=?, BIO=?, BG=? WHERE ID=?", (
			data["img"],
			data['bio']),
			data["bg"],
			data["id_"]
		).fetchone()

		return row


	def addPost(self, data) -> response:
		
		assert self.isOpen, "The db is not yet connected, Try again"
		try:
			if "img" in data:
				
				self.conn.execute("INSERT INTO POSTS(USER_ID, Text, IMG) VALUES(?, ?, ?)", (
					data["User_id"], 
					data["text"],
					data["img"]
				))

			else:

				self.conn.execute("INSERT INTO POSTS(USER_ID, Text) VALUES(?, ?)", (
					data["User_id"], 
					data["text"]
				))

			self.commit()

			return response(200, "Post was added successfully")
		except Exception as e:
			print(e)

		return response(500, "Post was not added successfully")

	def GetAllPosts(self) -> list:
		assert self.isOpen, "The db is not yet connected, Try again"
		rows = self.cursor.execute("SELECT USER_ID, Text, IMG FROM POSTS ORDER BY ID DESC").fetchall()
		
		if rows:
			for i, row in enumerate(rows):
				rows[i] = {
					"id_": row[0],
					"Text": row[1],
					"IMG": row[2]
				}
				
				user = self.GetUserById(row[0])

				if user:
					rows[i]["user"] = {
						"id_": user["id_"],
						"UserName": user["UserName"],
						"img": user["img"]
					}
				
			return rows
		else:
			return False

	def TokenGen(self, salt: str):
		_IV: list[str] = [chr(randint(0, 255)) for i in range(32)]
		_S1 = ''.join(_IV)
		_S_FINAL = _S1 + b64encode(salt.encode()).decode()
		return sha256(_S_FINAL.encode()).hexdigest()
	
	def GetAllUsers(self):
		assert self.isOpen, "The db is not yet connected, Try again"
		rows = self.conn.execute("SELECT * FROM USERS").fetchall()

		if rows:
			for i, row in enumerate(rows):
				rows[i] = {
					"id_": row[0],
					"UserName": row[2],
					"img": row[5],
					"bg": row[6],
					"bio": row[7],
					"addr": row[8]
				}

			return rows
		else:
			return False

	def GetUserByToken(self, T: str):
		assert self.isOpen, "The db is not yet connected, Try again"
		T = b64decode(T).decode()
		row = self.cursor.execute("SELECT * FROM USERS WHERE TOKEN=?", (T, )).fetchone()		
		if row:
			
			return response(200, {
				"id_": row[0],
				"Email": row[1],
				"UserName": row[2],
				"img": row[5],
				"bg": row[6],
				"bio": row[7],
				"addr": row[8]
			})

		return response(500, "this token is not associated with a user!")

	def verify(self, User: UserModel) -> list | None:
		assert self.isOpen, "The db is not yet connected, Try again"
		row = self.cursor.execute("SELECT * FROM USERS WHERE EMAIL=?", (User.Email, )).fetchone()
		if row:
			if User.hashedPWD == row[3]:
				return row
			else:
				return None


	def AuthenticateUser(self, User: UserModel) -> response:
		""" Checks if the creds are correct then returns a token to be used as a secret to access user private data. """
		
		Data = self.verify(User)

		if Data:
			
			return response(200, {
				"id_": Data[0],
				"Email": Data[1],
				"UserName": Data[2],
				"Token": b64encode(Data[4].encode()).decode(),
				"img": Data[5]
			})

		else:
			return response(202, "Incorrect password.")
		return response(500, "This email is not registered, please recheck the email and try again!!")

	# def CheckPassword(self, Email: str, Password_hash: str) -> response:
		

	def connect(self):
		self.conn = sqlite3.connect(self.__Path)
		self.isOpen = True
		print("Connected to database..")
		return self

	@property
	def cursor(self):
		return self.conn.cursor()

	
	def CheckUserExistence(self, email):
		
		row = self.cursor.execute("SELECT USERNAME FROM USERS WHERE EMAIL=?", (email, )).fetchone()
		if row:
			return row
		else:
			return False

	def AddNewUser(self, Data: UserModel) -> response:
		
		if not self.CheckUserExistence(Data.Email):
			try:
				Token: str = self.TokenGen(Data.Email)
				self.conn.execute("INSERT INTO USERS(EMAIL, USERNAME, PASSWORDHASH, TOKEN, IMG, BIO, BG, ADDR) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (Data.Email, Data.UserName, Data.hashedPWD, Token, Data.IMG,Data.Bio, Data.bg, Data.addr))
				self.commit()
				
				logging.info("Added new user: {200}")
				
				return response(200, {
					"T": b64encode(Token.encode()).decode(), "msg": "Your account was made successfully, you can login now."
				})
			
			except Exception as err:
				self.warn("Error: %s" % str(err))

			return response(500, "The server had a problem adding the account, You can try later..")
		
		return response(500, "This email is already used by another account, Try with another email..")

	def warn(self, err: str):
		logging.warning(err)

	def close(self): 
		self.conn.close()

	def commit(self): 		
		self.conn.commit()
		return self


def constructDB(Path_: Path) -> DB:
	if isinstance(Path_, str):
		Path_ = Path(Path_)	
	db = DB(dbPath=Path_)
	return db


