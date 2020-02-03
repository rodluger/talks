rm -rf .git
git init
git add .gitignore
git add *
git commit -m "rebase"
git push -f https://rodluger:$GITHUB_API_KEY@github.com/rodluger/talks HEAD:master