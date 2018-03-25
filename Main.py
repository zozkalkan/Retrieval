from github import Github

# using username and password
g = Github("haciyakup", "Koc1234.")

print(g.get_user())
# or using an access token
#g = Github("access_token")
