#SMS
## The minimalistic messaging client on *Linux*

![Alt text](1.png?raw=true "ScreenShot")

###What you will need###
*On your android:*
- Busybox
- SSH Server (any you like from google store)

*On your Linux desktop:*
- Quickly *(development framework)*
- Bash
- Accessable commands: ssh, scp
- Python 2.7, python packages: sqlite3, commands, time, subprocess

How to setup it up:
*On Ubuntu*
```bash
sudo apt-get install quickly quickly-ubuntu-template
sudo apt-get install python-pip
sudo pip install sqlite3
```
*Then:*
1. Create a folder called **sms-quickly** and put the **root content in it**.
2. Open the terminal and cd into the **sms-quickly**
3. run: *quickly run* - and it should run the application
4. To design the app, in the root folder run: *quickly design*.
5. The core code can be found in sms-quickly/SmsQuicklyWindow.py