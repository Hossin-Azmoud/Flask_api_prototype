
from flask import (
	Flask, 
	request, 
	render_template,
	redirect,
	url_for,
	make_response,
	session
)

from flask_cors import CORS
from json import dumps
from pathlib import Path
from time import sleep
from DataBaseModel import (
	ConstructModel,
	constructDB,
	response,
	DB_PATH
)

from Funcs import (
	EncodeJWT,
	VerifyJWT,
	filteredUserList
)

from json import dumps

from Constants import (
	APP_SECRET,
	JWT_SECRET
)

def createNewDbObject(): return constructDB(Path(DB_PATH))

app = Flask(__name__)
app.secret_key = APP_SECRET


CORS(app)
PORT = 5000
NOT_EMP: str = "<h1 style=\"color: red;\"> Route still NotImplemented </h1>"
# More speed I think
Api_DB_HANDLER = createNewDbObject()

@app.route("/")
def index():
	return render_template("index.html")
def getUserByAT(T: str):
	
	Api_DB_HANDLER.connect()
	Db_res = Api_DB_HANDLER.GetUserByToken(T)
	if Db_res.code == 200:
		return Db_res.data
	return None
def getAccessToken():
	sessionT = None
	AccessToken = request.cookies.get("Access-Token")
	if "Access-Token" in session:
		sessionT = session["Access-Token"]

	if AccessToken or sessionT:
		AccessToken = VerifyJWT(JWT_SECRET, AccessToken)
		if isinstance(AccessToken, dict):
			print(AccessToken["T"])
			return AccessToken["T"]
	return None
def MakeServerResponse(code, data) -> str: 
	return response(code, data).makeResponse()
@app.route("/login", methods=["POST"])
def login():
	if request.method == "GET":
		AccessToken = getAccessToken()
		if AccessToken:
			return dumps({"T": AccessToken})
		return "Access denied."
		
	else:
		if "AccessToken" in request.json:
			Jwt_token = request.json["AccessToken"]
			data = VerifyJWT(JWT_SECRET, Jwt_token)
			if isinstance(data, dict):
				# Try to get user data to send to my client.
				accessToken = data['T']
				User = getUserByAT(accessToken)
				return MakeServerResponse(200, User)
			elif isinstance(data, str):
				# Return an  error code and the error message to the client.
				return MakeServerResponse(202, data)

		data = ConstructModel(request.json)
		DB_HANDLER = createNewDbObject()
		DB_HANDLER.connect()
		User = DB_HANDLER.AuthenticateUser(data)
		if User.code == 200:
			response = User.makeResponse()
			
			AccessToken = {
				"T": User.data["Token"]
			}

			User.data["Token"] = EncodeJWT(JWT_SECRET, AccessToken)
			return dumps(response)

		return dumps(User.makeResponse())
@app.route("/signup", methods=["POST"])
def signUp():	
	data = ConstructModel(request.json)

	Api_DB_HANDLER.connect()
	User = Api_DB_HANDLER.AddNewUser(data)

	if User.code == 200:
		AccessToken = User.data["T"]
		User = getUserByAT(AccessToken)
		User["Token"] = EncodeJWT(JWT_SECRET, {"T": AccessToken})
		return MakeServerResponse(200, User)
	return dumps(User.makeResponse())
	
@app.route("/UpdateUserImage", methods=["POST"])
def UpdateUserImage():
	# TODO: Require the access token in this route for more security ;)
	if request.method == "POST":
		
		data = request.json
		if "id_" in data:
			if "img" in data:
				DB_HANDLER = createNewDbObject()
				DB_HANDLER.connect()
				res = DB_HANDLER.UpdateImg(data["img"], data["id_"])
				if res:
					return MakeServerResponse(200, res)

		return MakeServerResponse(202, "Encountered an error!")

	return MakeServerResponse(500, "The get method is not Implemented")
@app.route("/UpdateUserBackground", methods=["POST"])
def UpdateUserBg():
	# TODO: Require the access token in this route for more security ;)
	if request.method == "POST":
		data = request.json
		if "id_" in data:
			if "img" in data:
				DB_HANDLER = createNewDbObject()
				DB_HANDLER.connect()
				res = DB_HANDLER.UpdateBackgound(data["img"], data["id_"])
				if res:
					return MakeServerResponse(200, res)

		return MakeServerResponse(202, "Encountered an error!")

	return MakeServerResponse(500, "The get method is not Implemented")
@app.route("/query", methods=["GET"])
def queryUsers():
	
	DB_HANDLER = createNewDbObject()
	DB_HANDLER.connect()
	users = DB_HANDLER.GetAllUsers()
	if "q" in request.values:
		q = request.values["q"]
		users = filteredUserList(q, users)
		return MakeServerResponse(200, users)
	else:
		return MakeServerResponse(200, users)

@app.route("/MakePost", methods=["POST"])
def createPost():
	""" 
	Route for making a post. 
	Waiting for this json entries:
		User_Access_Token: int,
		Postimg: base64EncodedBytes,
		PostText: str
	"""
	# TODO: Require the access token in this route for more security ;)

	if request.method == "POST":
		DB_HANDLER = createNewDbObject()
		DB_HANDLER.connect()
		res = DB_HANDLER.addPost(request.json)
		return dumps(res.makeResponse())

	return dumps({"data": NOT_EMP})
@app.route("/GetAllPosts", methods=["GET"])
def getAllPosts():
	""" 
	Route for getting all posts.. 
	Waiting for this json entries:
		key: str
	"""
	DB_HANDLER = createNewDbObject()
	DB_HANDLER.connect()
	Posts = DB_HANDLER.GetAllPosts()
	return MakeServerResponse(200, Posts)
@app.route("/Update", methods=["POST"])
def Update():
	# TODO: Require the access token in this route for more security ;)
	"""
	this routes expects this format:
		json = { 
			"img",
			"bio",
			"bg",
			"id_"
		}
	"""

	if request.method == "POST":
		data = request.json
		DB_HANDLER = createNewDbObject()
		DB_HANDLER.connect()
		User = DB_HANDLER.UpdateAll()
		
		if User:
			return MakeServerResponse(200, "Data was Modefied!")
		else:
			return MakeServerResponse(500, "Data was not Modefied!")

	return "Wrong Method: get is not NotImplemented"
@app.route("/<user_id>", methods=["GET"])
def GetUserById(user_id):
	DB_HANDLER = createNewDbObject()
	DB_HANDLER.connect()
	User = DB_HANDLER.GetUserById(int(user_id))
	if User:
		return MakeServerResponse(200, User)
	return MakeServerResponse(500, "This user does not exist.")
@app.route("/getUserPosts", methods=["GET"])
def getUserPosts():

	"""
	Getting a user's posts.. 
	Waiting for this json entries:
		id_: int
	"""
	
	if "id_" in request.values:
		id_ = request.values["id_"]
		DB_HANDLER = createNewDbObject()
		DB_HANDLER.connect()
		
		posts = DB_HANDLER.GetUserPosts(id_)

		if posts:
			return MakeServerResponse(200, posts)

		else: 
			return MakeServerResponse(500, "No posts yet.")

	return "[]"

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
