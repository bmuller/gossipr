# Gossipr
Gossipr is a Jabber (XMPP) component that logs chat rooms to a database and provides an optional web interface to view those logs.  Gossipr uses Python's [Twisted](http://twistedmatrix.com) and is thoroughly asynchronous.

# Usage

## Prerequisites
1. First, edit your jabber server config file to allow for a new component connection.  If you are using [ejabberd](http://www.ejabberd.im/), this can be done by adding the following lines to the services section of your *ejabberd.cfg* file:

      {5524, ejabberd_service, [ {ip, {127, 0, 0, 1}}, {access, all}, {shaper_rule, fast}, {host, "gossipr.localhost", [{password, "secret"}]} ]},

Make sure to change the password to something actually secret, and then restart your jabber server.
2. Install [Twisted](http://twistedmatrix.com).
3. Install [Twistar](http://findingscience.com/twistar/)
4. Install Divmod's [Nevow](http://divmod.org)

## Installation
First, get the source:
    git clone git://github.com/bmuller/gossipr.git

Then, within the gossipr directory:
    sudo python setup.py install

Then, after creating a database and setting up a user account that can access it, import the DB structure:
    mysql -u <user> -p <dbname> < db/mysql.sql

At this point, you can copy config.py.dist to config.py and edit it for your configuration.  At this point, you can copy your config.py and the gossipr.tac file anywhere you'd like and can start the server with:
    twistd -noy gossipr.tac

See the twistd man page for more information.