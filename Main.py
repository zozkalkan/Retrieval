from git import *

repo = Repo('https://api.github.com/users/zozkalkan/repos')

commits =repo.commits()

print('%s'%commits[0].author)
