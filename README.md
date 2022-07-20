# mix-blander-3000
Code for drink mixing contraption
Ment to be built around a raspberry pi, the IO will assume that it is a RPI (otherwise it will use a fake IO)


## Instructions 
```
python3 -m venv venv
```
Linux: 
```
source venv/bin/activate
```
Windows: 
```
venv\Scripts\activate
```
Both:
```
pip install -r requirements.txt
pip install -r requirements_pi.txt # Only on raspberry pi
git submoduile init
git submodule update
```
On raspberry pi
```
pip install RPi.GPIO
```

Start the python program in tmux:
run the attached tmux_start.sh at startup
add 
```
sudo -u pi bash /PATH/mix-blander-3000/tmux_start.sh &
```
to /etc/rc.local
