# Docs
-----------------------------------------------------------------------------------------------

## Routes

- `/login`
- `/signup`
- `/UpdateUserImage`
- `/UpdateUserBackground`
- `/query`
- `/MakePost`
- `/GetAllPosts`
- `/Update`
- `/<user_id`
- `/getUserPosts`

## Models

- `User` -> Used to store user data to be either processed or sent to the client.
- `Post` -> Post data (img, text...), it is constructed to be either sent or saved to the sqlite3 db.
- `Response` -> Response is a model to encapsulate the server's response, Fields are `CODE` if the operation succeds then it is set to 200, if not it is set to another code. `DATA` which is set to whatever the response data is. it can be string, list of objects or an object. (Posts, Users, User, Post)

## Security

- For security I have used JWT to authenticate the User and I store passwords as sha256 hash to be verified when the user sends a login request.
- I also intend to add a layer of security to the api with an additional field `JWT_TOKEN` when performing operations such as making a post

## Lib and frameworks.
- Flask
- sqlite
- jwt
NOTE: To see more info about libs I used you can check requirements.txt


