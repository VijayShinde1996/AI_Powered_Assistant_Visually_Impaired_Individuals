1. Check Git Status
git status
2. Add All Files to Staging Area
git add .
3. Commit Your Changes
git commit -m "Your commit message"
4. Push Your Changes to GitHub
git push origin main
5. Clone a Repository from GitHub
git clone <repository_url>
6. Create a New Branch
git branch <branch_name>
7. Switch to a Branch
git checkout <branch_name>
Or use the newer version:
git switch <branch_name>
8. Create and Switch to a New Branch
git checkout -b <branch_name>
Or use the newer version:
git switch -c <branch_name>
9. Merge a Branch into the Current Branch
git merge <branch_name>
10. Pull Latest Changes from GitHub
git pull origin main
11. View Commit History
git log
12. View a Specific Commit
git show <commit_id>
13. View a List of All Branches
git branch
14. Delete a Branch Locally
git branch -d <branch_name>
15. Force Delete a Branch Locally (if not fully merged)
git branch -D <branch_name>
16. Delete a Remote Branch
git push origin --delete <branch_name>
17. Check Remote Repositories
git remote -v
18. Add a Remote Repository
git remote add origin <repository_url>
19. Set a Remote Repository's URL
git remote set-url origin <new_repository_url>
20. Fetch Latest Changes from Remote (without merging)
git fetch origin
21. Rebase a Branch onto Another
git rebase <branch_name>
22. Undo Last Commit (and keep changes)
git reset --soft HEAD~1
23. Undo Last Commit (and discard changes)
git reset --hard HEAD~1
24. Create a Tag
git tag <tag_name>
25. Push a Tag to GitHub
git push origin <tag_name>
26. Delete a Tag Locally
git tag -d <tag_name>
27. Delete a Tag Remotely
git push origin --delete tag <tag_name>
28. View Differences Between Commits or Branches
git diff <commit_id> <commit_id>
git diff <branch_name>
29. Show a Specific File’s History
git log -- <file_path>
30. Stash Changes (save changes temporarily)
git stash
31. Apply Stashed Changes
git stash apply
32. List Stashed Changes
git stash list
33. Drop a Stash
git stash drop