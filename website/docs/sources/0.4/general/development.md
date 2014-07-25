---
  title: BOLTS development with git
  audience: contributors
---

BOLTS consists of quite a lot of code and data and to manage this code and data
and the changes made to it, [git](http://www.git-scm.com) is used. Git is a
distributed version control system and this allows everybody who wants to work
with git to obtain a version of BOLTS (called a fork), that is separate from
the main version, so that it is possible to play around, add parts and develop
new features without breaking the master branch. git then makes it very easy to
move the changes made in one branch to the master branch.

There exist many different workflows and ways how to develop software with git.
I will present three different ways that I consider useful for the purpose of
contributing to BOLTS. For more information see the [git
documentation](http://www.git-scm.com) or the [GitHub
documentation](https://help.github.com/).

### Using the GitHub web interface

For this way you need a [GitHub](https://github.com/) account. It is probably
the easiest way to make small corrections and additions, and works well for all
tasks that involve editing and creating text files.

Go to the [BOLTS repository page](https://github.com/jreinhardt/BOLTS), there
you see a list of all files and directories and you can navigate around by
clicking on them.

To edit a file just click on it, and then use the `Edit` button to open the web
based editor. You can now make your changes. When you are done, scroll to the
bottom of the page and add a short description, and a longer explanation about
what you changed if necessary. Try to use precise language and avoid having
unrelated changes in one commit (like fixing a typo and adding a new class).

Alternatively you can add a new file by clicking on the small `+` next to the
repository name. A editor page opens, and you can give a filename and start
typing contents.

Finally hit the `Commit Changes` button at the bottom of the page. GitHub will
now automatically fork the BOLTS and create a new commit with the changes you
just made.

On the next page you are asked whether you want to offer your changes to the
BOLTS maintainer, this is called a pull request. If your changes are more
substantial, you should add a short explanation, why you think these changes
should go into the main branch. You can then send the pull request.

The maintainer can now look at your changes, decide whether he wants them in
the main branch, give you feedback and ask for further modifications.

### Checking out a GitHub fork

For this way you also need a [GitHub](https://github.com/) account. It allows
you also to work offline. This way requires you to work with the commandline.

This way will also create a fork of BOLTS on the GitHub server, but
additionally you will also obtain a fork on your own computer. You make changes
to the one on your own computer and then communicate these changes back to the
GitHub fork. This way you can work offline, you only need to be online to push
your changes.

Before you start you should 
[install and set up git](https://help.github.com/articles/set-up-git)
supplying it with your name and email address, so that your contributions can
be attributed to you.

There is a 
[pretty good tutorial how to fork a repository](https://help.github.com/articles/fork-a-repo)
on the [GitHub help pages](https://help.github.com/),
 where you can also find more informations about working with git and GitHub.

The next steps are explained in the section about `Creating topic branches and
commiting your work`.

### Checking out a local copy of BOLTS

For this way you do not need a GitHub account, and it allows you to work
offline. In contrast to working with a GitHub fork, your proposed changes are
not published online, but sent to the maintainer by email.

Before you start you should 
[install and set up git](https://help.github.com/articles/set-up-git)
supplying it with your name and email address, so that your contributions can
be attributed to you.

To obtain a local version of the BOLTS git repository fire up the commandline,
change to the directory where you want to store the BOLTS repository and type

git clone git@github.com:jreinhardt/BOLTS.git

a new directory named `BOLTS` will be created that contains the current
development state.

The next steps are explained in the section about `Creating topic branches and
commiting your work`.

### Creating topic branches and commiting your work

You now should have a local copy of BOLTS. Before you start making changes, you
should create a new branch. There is a quite detailed description about
branches on the 
[git-scm website](http://git-scm.com/book/en/Git-Branching).
In short, a branch is like a parallel universe of the source code. This allows
you to work on independent changes (like adding a new collection and writing
base modules for another one) in parallel, by storing them in separate
branches. But if you do not want to work in parallel, it boils down to a few
commands that you use before and after you did your changes.

To create a new branch type on the commandline

    git checkout -b "branchname"

and replace branchname by a short descriptive name like
"steppermotorcollection", if you want to add a new collection for stepper
motors or "hexsocketbases" if you want to add base geometries for the hexsocket
collection. A branch that is used to work on a certain feature is called a
topic branch.

If you now type

    git status

it tells you which branch you are on

    # On branch steppermotorcollection
    ...

To switch branches you can use

    git checkout branchname

Before you edit files, make sure you are in your topic branch. To record a set
of changes, you first "add" the changed or new files that you want to include
in the commit by

    git add filename
    git add filename2
    git add filename3 filename4

with

    git status

you can get a list of changed files that will be commited and those that will
not be commited. Finally, to commit the added changes use

    git commit

A editor opens and you can enter a description of the changes. The first line
is a short description. If the changes deserve a more detailes explanation, one
can be added after a empty line.

Usually one structures the work on one feature into a series of commits that do
simple changes each. A rule of thumb is: If you cannot precisely describe the
changes in one line, you should consider to split it into smaller commits.

If you have finished the work on your feature you submit the changes  either by
fire off a pull request, or by creating a bundle and send it by mail to the
maintainer.

### Sending a pull request

To push your topic branch to GitHub, you use

    git checkout branchname
    git push -u origin branchname

This creates a new branch called branchname on your BOLTS fork on GitHub. If you make more changes on this topic branch (maybe on request of the maintainer), you can use just

    git push origin branchname

The initiation of a pull request on GitHub is covered very well by 
[this tutorial](https://help.github.com/articles/using-pull-requests).

### Creating a bundle

Another possibility to contribute your changes is to create a bundle file
containing all the commits you added.

To create the bundle use

    git bundle create branchname.bundle origin/master..branchname

but replace branchname by the name of your branch.

The resulting file can be attached to an email with a description what this
does and then send it to
<a href="mailto:BOLTS@ist-dein-freund.de">BOLTS@ist-dein-freund.de</a>.

