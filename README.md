# Space Billiards

A 2D gravity-based pool game written in Python with Pygame and Pymunk during my first semester at KMITL (2022).

Demo video: https://www.youtube.com/watch?v=jAX7XecOy4E

## Features
- Scene state machine with fade transitions, a pause menu, name input and a top-5 scoreboard saved to `score.json`
- Custom per-step gravity on Pymunk bodies: pockets pull moving balls, and the cue ball attracts others until first contact
- Real-time trajectory preview that simulates the next shot ahead of time
- Score that decays with the number of collisions

## Run
Python 3.10 or later, on Windows (some file paths use backslashes):

```
pip install pygame pymunk
python main.py
```

The background music and the brand-logo ball textures from the original version are not included; the balls use plain placeholder images.
