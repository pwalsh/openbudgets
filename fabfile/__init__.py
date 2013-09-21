import remote
import local


###### SOME MANUAL MACHINE SETUP STILL...
#####
###
##
#

# 1. run the machine_bootstrap task (have a couple of questions to answer via prompts). It is CRITICAL to
# change the version number on the node install to be the same, WITHOUT the v prepended. pay attention.

# 2. manual setup of postgres user etc.


"""
def security_conf()
    pass
### Lock down access

Now we want to lock down access to the machine. We want to completely disable all password access, and, disable root logins.

To disable password access, first we need to generate some ssh keys.

If you are on Mac or Linux, simply type:

    ssh-keygen

and follow the steps. Create a name for the key (the same name as the hostname you gave to the machine earlier would be logical, but you can call it anything).

Again, on Mac or Linux, just make sure that this key is in the .ssh folder of your user.

I gave the key a name because I presume that most developers need multiple keys, so they need a way to manage them.

To do that, you need a config file in your .ssh folder. This file just tells ssh which key to use for any given connection. For each key, you'll have a record like this:

    Host your.ip.address
    IdentityFile ~/.ssh/your_key


It is pretty straightforward.

Again, these ssh steps are all on your local machine.

You'll notice that two files were generated when you created the ssh key - one with no extension, and one with a .pub extension. Now we need to get the one with the .pub extension into the user's ssh directory on the machine. The handshake between the keys is what will log you in.


For this we'll use scp, a utility to copy files over ssh. From your local machine, execute the following command.

    scp ~/.ssh/your_key.pub your_user@your.ip.address:

The trailing : is important. It says to put the public key in the user's home directory.

Now, log back into the machine, create an .ssh directory in the user's directory (if there isn't one already), and copy the pub key into that .ssh directory. The, rename the pub key as "authorized_keys". Future keys will need to be appended to this file.

To make sure that this user and only this user can fiddle with this key, enter the following commands:

    chown -R example_user:example_user ~example_user/.ssh
    chmod 700 ~example_user/.ssh
    chmod 600 ~example_user/.ssh/authorized_keys


Now we are going to shutdown password access, and root user login.

Remember, we are now logged in as the created user, so, to perform system commands like this, we use sudo.

    sudo nano /etc/ssh/sshd_config

First we'll disable root login. Find the appropriate lne and change it to no.

    PermitRootLogin no

Before we disbale password access, we want to check that our key is actually working.

So, logout of the machine.

If you can log back in again without reentering your password, you're good. (if you password protected your ssh key when setting it up, your local machne will ask for THAT password, but the server won't ask for a password).

If not, work out why and do not do the net steps.


So, now we are back in, we'll disable password access:

    sudo nano /etc/ssh/sshd_config

And the line:

    PasswordAuthentication no

Ok, we've go the system pretty locked down at a basic level. Now let's enable a firewall.
"""
