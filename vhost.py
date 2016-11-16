#!/usr/bin/env python2.7

import os
import time

if os.geteuid() != 0:
	exit("You isn't root, is it.")

vhost = raw_input('Enter name of new vhost to setup: ')

vhost_path = "/Users/jim/www/"
vhost_dir = vhost_path + vhost + "/public_html/"
print "Ok attempting to setup [%s] as a new vhost in dir [%s]" % (vhost, vhost_dir)

#os.makedirs(vhost_dir)

os.mkdir(vhost_path + vhost + "/logs/")
os.system("chown -R jim:staff " + vhost_path + vhost)

print "New vhost directory should be listed below:"
os.system ('ls -l ' + vhost_path)

print "Writing apache conf file..."
fd = open("/etc/apache2/vhosts/default.local", "r")
fn = open("/etc/apache2/vhosts/" + vhost + ".conf", "w")

for line in fd:
	fn.write(line.replace('hostname', vhost))

fd.close()
fn.close()

print "New conf file:"
os.system("cat " + "/etc/apache2/vhosts/" + vhost + ".conf")

print "Writing to hosts file..."
fh = open("/etc/hosts", "a")
fh.write("\n127.0.0.1\t" + vhost + "\n127.0.0.1\twww." + vhost + "\n")
fh.close()

print "\nNew hosts file:"
os.system("cat /etc/hosts")

print "\nRestarting apache..."
os.system("apachectl restart")

print "\nWaiting for apache to come back up..."
time.sleep(5)
print "\nIs apache back with us?"
os.system("ps aux | grep httpd")

print "\nTest apache config?"
os.system("apachectl configtest")

print "\nWriting php test file to " + vhost_dir + "test.php"

fp = open(vhost_dir + "test.php", "w")
fp.write("<?php echo phpinfo(); ?>\n")
fp.close()

print "\nListing files in [" + vhost_dir + "]..."
os.system("ls -la " + vhost_dir)

print "\n\nMy work is done.\n"

