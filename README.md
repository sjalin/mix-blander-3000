# mix-blander-3000
Code for drink mixing contraption
Ment to be built around a raspberry pi, the IO will assume that it is a RPI (otherwise it will use a fake IO)


## Instructions 
```
python3 -m venv venv
```
### Linux: 
```
source venv/bin/activate
```
### Windows: 
```
venv\Scripts\activate
```
### Both:
```
pip install -r requirements.txt
git submoduile init
git submodule update
```
### Raspberry pi
```
pip install -r requirements_pi.txt
```
#### Edit kivy configuration
This is because the touch screen "double clicks" by default

In ~/.kivy/config.ini change the [input]-section to:

```
[input]
%(name)s = probesysfs,provider=hidinput
mouse = mouse
hid_%(name)s = probesysfs,provider=hidinput
```