Open Muni
=========

Open Muni is...

Get Involved
============

Code: https://github.com/hasadna/open-muni

Issues: https://github.com/hasadna/open-muni/issues

Discussion: https://groups.google.com/forum/?fromgroups=#!forum/open-muni-dev

Product requirements: https://docs.google.com/document/d/1cDOELgc4VQ8iPSr6795g0iMMz_klE5dM_s-y2GXbH7o/edit#

More about HaSadna (Public Knowledge Workshop): http://hasadna.org.il/


Quick Start
===========

Build a local environment
-------------------------


Git repository practices
------------------------

We are following the Git Flow paradigm for managing branches, deployment code, etc.

Read here for the background: http://nvie.com/posts/a-successful-git-branching-model/

The essentials:

We always have at least two branches: "master" and "development".

You should not ever be working on master, we just merge there for deployment.

We always work off "development". If you are coding a specific feature, branch development as such:

"feature/what-you-call-it"

examples:

"feature/user-accounts"

"feature/bootstrap-integration"

When you finish, submit a pull request for the branch, and we'll merge back into development.
