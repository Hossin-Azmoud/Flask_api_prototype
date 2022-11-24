from dataclasses import dataclass
from hashlib import sha256
from json import dumps

def hashPwd(s: str) -> str: return sha256(s.encode()).hexdigest()
def getField(Frame: dict, Field: str): return Frame[Field] if Field in Frame else ""

@dataclass
class PostModel:
	UserID: int
	TEXT: int
	IMG: str

	def __dict__(self) -> dict: return {"UserID": self.UserID, "TEXT": self.TEXT, "IMG": self.IMG}
	def __str__(self) -> str: return dumps(self.__dict__())

@dataclass
class UserModel:
	UserName: str
	Email: str
	hashedPWD: str
	IMG: str
	Bio: str
	bg: str
	addr: str

	def __dict__(self): 
		return {
			"UserName": self.UserName, 
			"Email": self.Email, 
			"hashedPWD": self.hashedPWD,
			"Bio": self.Bio,
			"bg": self.bg,
			"addr": self.addr
		}
	
	def __iter__(self):
		for i in self.__dict__():
			yield i

	def __str__(self) -> str: return dumps(self.__dict__())


@dataclass
class response:
	code: int
	data: any
	
	def __dict__(self) -> dict:
		return {
			"code": self.code,
			"data": self.data
		}

	def makeResponse(self) -> dict:
		return self.__dict__()

def ConstructModel(DataFrame: dict) -> UserModel:

	return UserModel(
		UserName = getField(DataFrame, 'UserName'),
		Email = getField(DataFrame, 'Email'),
		hashedPWD = hashPwd(DataFrame['Password']) if 'Password' in DataFrame else "",
		IMG = DataFrame["img"] if "img" in DataFrame else "/img/defUser.jpg",
		Bio	= DataFrame["bio"] if "bio" in DataFrame else "Wait for it to load :)",
		bg = DataFrame["bg"] if "bg" in DataFrame else "/img/defBg.jpg",
		addr = DataFrame["addr"] if "addr" in DataFrame else "Everywhere",
	)


