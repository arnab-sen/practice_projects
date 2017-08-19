import praw

class User():
	def __init__(self):
		self.__username, self.reddit = self.__get_auth_instance()
		self.__user = self.reddit.redditor(self.__username)

	def __get_auth_instance(self):

		with open("auth.txt", "r") as file:
			u, p, c_id, c_secret = file.read().split()
		
		reddit = praw.Reddit(
								client_id = c_id,
								client_secret = c_secret,
								username = u,
								password = p,
								user_agent = "My Comment Manager"
								)

		return u, reddit

	def print_comments(self):
		for comment in self.__user.comments.new():
			print(comment.body + "\n")

	def get_username(self):
		return self.__username

	def get_comments(self):
		return list(self.__user.comments.new())

	def __repr__(self):
		return "Username: " + self.__username

def main():
	user = User()
	print(user)
	comments = user.get_comments()
	for comment in comments:
		comment.edit("[deleted]")
		comment.delete()

main()
