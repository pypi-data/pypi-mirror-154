
# Useful commands 
sudo rm -rf .git/

# Brikeda Robot

Python Classes to support hardware on Raspberry Pi such as waveshare motor controllers,range detectors,cameras

## Instructions

1. Install:

```
pip install brikeda_robot
```

2. Generate an Brikeda object and call some methods:

```python
from brikeda_robot.robot import Robot

# initialize Brikeda Object with personal key retrieved at brikeda.com/aipanel
brik=Brikeda("4b6871e0d9d84de2926df29483a9aab9")
# send a message. any string will do. but if is a valid hex color it will display it
brik.SyncMessages("#ebde34")
# get a sentiment analysis of a sentence:postive, negative ratings
x = brik.Sentiment('this is exciting')
print(x)

```

