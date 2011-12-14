# Git-Kit

## Why Git-Kit?

Git-kit is an effort to make Git easier to use by anyone. Git consists of what is referred to as "plumbing", that is, a small concise set of highly modularized tools that implement the standard Distributed VCS API. This plumbing allows for Git to be extremely flexible, as it can perform any workflow used by any other widely used VCS, and allow for seamless integration with mainstream VCS's like SVN, Hg, and Bzr. 

Git-Kit aims to encapsulate the basic workflow elements of Git so that anyone, on any schedule, can use Git without having to learn how it works.

## What Git-Kit is *Not*

Git-Kit is not a replacement for Git. It is importanty to know how a tool works if you want to use it effectively. In simplifying the Git API, Git-Kit aims to improve accessibility, but it cannot do all of the heavy-lifting for you. You can't have your cake and eat it too. Git-Kit is literally just a wrapper around git, so it aims to explain what it is doing to you, in case something ever goes wrong/ a weird and or unanticipated use-case comes up, you'll at least have an idea how to fix it.

## Install git-kit

1. Clone git-kit (this is important if you wish to receive updates!), 
1. Add the folder you just cloned to $PATH variable
1. Make sure you have python 2.6 installed (untested on python 3, but expect it would explode -plans to integrate with dulwich API and ship with a (java,jython,jsch) stack for OOB support for any platform with java.

<!-- To update gitkit, simply run "git-kit update" (unimplemented) -->

## Implemented API

* "gk ": When ran with no argument, gk begins an interactive help (handhold mode)
* "gk sync [message]". Default message is "incremental commit". You can run this on a crontab to constantly sync.
* "gk ignore PATTERN". Ignores a pattern suitable for consumption with libfnmatch
* "gk configure". Launches repo configuration, writes results to json.

The commands currently implemented run directly from the lib/cmds/__init__.py module.



## Future Workflow / Features

Git-kit aims to implement the following APIs:

* Git-kit sync [branch(es)["message"]]
Git-kit sync with no arguments will sync everything. Git kit sync with a branch arguemet will sync the current branch with the target branch. Git-kit sync with two or more arguments will sync all of the selected branches, (note, to sync with the current branch when supplying two or more branches, you must explicitely include the current branch as an argument - it is no longer implicite). When a sync occurs, the commit history will be auto-squashed to replace all incremental commits with one big commit.

* Git-kit create [branch|commit|tag]
Branches will be created as tracking branches by default, so that all stable code is auto-promoted to them. Creating a commit is a wrapper for the command 'git add REPOROOT &amp&amp git commit -a -m "YOUR_MESSAGE"'

* Git-kit destroy [file|folder|branch|commit|tag]
Destroying files and folders will permanently remove them from the repository, and it's history. When a destroy is invoked,
a flag is set to destroy them in remote repos as well when the next sync action is performed. Destroying files should not be taken lightly. As a precaution, run nightly snapshots on one of your remotes and back them up for a reasonable length of time.

* Git-kit use [branch|commit|tag|REF]
This will switch you to the selected ref. your old work will be saved in your footprints.

* Git-kit ignore [file|folder|regex]
Git-kit ignore is a macro to write to the repository's .gitignore file.
Before you add a rule, git-kit ignore will prompt you with a list of files matching the .gitignore glob expression. It will then add the .gitignore commit, and prompt you to ask if you would like to also remove (but not destroy) the matching files

* Git-kit publish [branch|commit|tag|REF]
Git-kit publish is a macro to build a selected branch, or REF, and put the result on a selected server. This information will be stored in git-kit's git-publish file. It requires a target host, and file as arguments, and just wraps scp. In order to build the target, the shell commands to run the build are required. It will require userauth to transfer the file.



## Wishlist Features:

* Git kit will include the "footprints" feature. each time a change is made (branch is switched,etc) this change is versioned within git kit. In other words, git-kit keeps track of your git state to let you rewind (an undo/redo stack). 

* git-kit backtrace
will show you a list of all of your actions. You can specify verbosity level by adding v's (-v,-vv,-vvvv). You can then select the commit ID and use it with Git-kit use.

## Technical info:

Git-kit wraps up the following standard git-workflow:

1. Pull
1. Commit
1. Push

Or, more specifically:

1. git commit -a -m "temporary commit"
1. git branch -D tempbranch
1. git checkout -b tempbranch
1. git checkout (original branch/commit)
1. git reset HEAD^
1. stash push
1. Pull --rebase
1. stash pop
1. add ROOT
1. commit -a -m "incremental commit"
1. git push
1. git push --tags

Gitkit serves as a wrapper for storing repository configuration. It is tailored to simplify submodules, and to allow for easy adaption of a large set of projects, that may not be related, but still required (a number of projects from the same organization - an entire "workspace"). 

Gitkit stores repository configurations in the gitkit.cfg file. This is a json file, is it can be safely editted directly (just make sure that you obey [json syntax][1]). All metadata about a repository can be stored here. Including, whether to store filesytem metadata, which remotes are writeable, and eventually which hooks (if any) to run on a repo (by default, all in the .hooks directory inside a repo will be executed).

## Feature requests /Bugs

Please submit all features requests/bugs to hameld@cc.umanitoba.ca
