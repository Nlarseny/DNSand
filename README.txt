DNS repo

-----------------------------
Fun stuff:
awk '{print $2}' filename.txt

sed '/TIMED/d' ./jan_14_NASA.txt > test.txt

BIND9
service bind9 start
service bind9 stop
service bind9 restart
service bind9 reload
service bind9 status

Unbound
stystemcrl start | stop | status unbound


21 Jan 2022
answer this:
find the root that updates the earliest, find what order the servers come in after this one (a-m), and the variation of each server



1 Feb 2022
ark
 /usr/local/ark/activity/dns-access/ArkDNS
 tools
 pi3:/usr/local/ark/bin


2 Feb 2022
cd /usr/local/ark/activity/dns-access
git clone https://github.com/Nlarseny/ArkDNS.git
to install dnspython : /usr/local/ark/bin/pip3 install dnspython --user
nohup /usr/local/ark/bin/python3 ../timechecker.py &

/usr/local/ark/bin/pip3 install dnspython



setting up git on each node:
git config --global user.name "Nlarseny"
git config --global user.email "larsen.d.nathan@gmail.com"
git config -l

git config --global credential.helper cache

NOTE: you need to make one commit for it to cache it
