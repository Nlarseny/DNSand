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

answer:
NASA is the slowest, then ICANN, then the rest
1259d771a4143bd7a24683c6b4ae5940ea5ed413




1 Feb 2022
ark
 /usr/local/ark/activity/dns-access/ArkDNS
 tools
 pi3:/usr/local/ark/bin


2 Feb 2022
cd /usr/local/ark/activity/dns-access/ArkDNS
git clone https://github.com/Nlarseny/ArkDNS.git
/usr/local/ark/bin/pip3 install dnspython --user
cd ArkDNS
mkdir []
cd []
nohup /usr/local/ark/bin/python3 ../timechecker.py &

git config --global user.name "Nlarseny"
git config --global user.email "larsen.d.nathan@gmail.com"
git config -l

git add .
git commit -m "added new node"
git pull
git push



/usr/local/ark/bin/pip3 install dnspython



setting up git on each node:
git config --global user.name "Nlarseny"
git config --global user.email "larsen.d.nathan@gmail.com"
git config -l

git config --global credential.helper cache

NOTE: you need to make one commit for it to cache it



4 Feb 2022
nohup /usr/local/ark/bin/python3 ../timechecker.py > /dev/null & -> keiv && ham
nohup /usr/local/ark/bin/python3 ../timechecker.py & -> san



8 Feb 2022


