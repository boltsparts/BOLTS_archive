---
  layout: docs
  title: How to get a development checkout
---

This tutorial covers only the very basics of git. For excellent documentation about git, visit [this page](http://git-scm.com).

You should have [installed git](http://git-scm.com/book/en/Getting-Started-Installing-Git), and be comfortable with the command line, as this tutorial makes heavy use of it.

Two different ways of getting a development checkout will be described, one for people that have a [GitHub](https://github.com) account, and one for people without one.

# Without GitHub



### Get a development checkout


Decide where you want to have your development checkout and change there:

    cd path/to/checkout

Then open the [BOLTS GitHub page](https://github.com/jreinhardt/BOLTS), copy to the clone URL given at the bottom of the side bar. Then enter

    git clone https://github.com/jreinhardt/BOLTS

git will now clone a copy of the complete version history of BOLTS and checkout the latest version in a directory called BOLTS under the current directory.

That is all. You can now make changes and additions (see [here]({{site.baseurl}}/contribute.html) for opportunities) and commit them. Try to create one commit for a logical set of changes, this will make review and acceptance much easier.


### Use it and make changes

You probably want to add new parts, create drawings and fix errors in BOLTS.
There is a number of [tutorials]({{site.baseurl}}/doc/index.html) and a [list
of opportunities]({{site.baseurl}}/contribute.html) for that. The checkout
contains [a script](use-checkout.html) that can simplifies some of the task
that you will perform regularly during this work.

### Commit your changes



### 
