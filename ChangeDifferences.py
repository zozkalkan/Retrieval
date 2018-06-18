from github import Github

# Add your pull request number here
PR = -1

# Add your Github Access token here
TOKEN = "7733fbccdd8f6247b2c543ce68126d871170c1a5"

# Login to Github
g = Github(TOKEN)
if g is None:
    raise Exception("Github token invalid, couldn't login")

# Fetch your repositories & find pbspro
pbspro_repo = None
for repo in g.get_user().get_repos():
    if repo.name == "Retrieval":
        pbspro_repo = repo

if pbspro_repo is None:
    raise Exception("PBSPro repo not found")

# Get your PR & and associated comments
pr_object = pbspro_repo.get_pull(PR)
if pr_object is None:
    raise Exception("Pull Request " + str(PR) + " not found")
comments = pr_object.get_comments()
if comments is None:
    print ("No comments found on PR " + str(PR) + ", exiting")
    exit(0)

# Write the comments & related details in a file called 'pr_<pr number>_review_comments'
filename = "pr_" + str(PR) + "_review_comments"
with open(filename, "w") as fd:
    for comment in comments:
        fd.write(comment.commit_id + "\n" + str(comment.created_at))
        fd.write("\n" + comment.user.name + "\n")
        fd.write("FILENAME: " + comment.path + ": " + str(comment.position) + "\n")
        fd.write("COMMENT:\n" + comment.body + "\n")
        fd.write("DIFF: \n" + comment.diff_hunk + "\n\n")
        fd.write("==================\n\n")

    print ("PR comments written in " + filename)