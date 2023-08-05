game_coroutines
===============

game_coroutines is a pure-python lib with no dependencies, to simplify calling 
methods over time on game environments.

For example, on a game, if you need to move a sprite from point (0, 100) to 
(300, 100) over 10 seconds, you will need to deal with frame updates, 
delta_times and controlling the position over time.

With game_coroutines you can create a coroutine to do that for you, for example:

```python
#main.py

import arcade
from game_coroutines import Coroutine

...
self.player = #player sprite creation
...

def move_player(progress):
    self.center_x = arcade.lerp(0, 300, progress)

move_routine = Coroutine(delay=0.0, duration=10, progress_func=move_player)
move_routine()
```

Is was maded to work with arcade, but it can run easily on py-game too.

Install
-------

```
pip install game_coroutines
```

Configuring
-----------

It's very easy to configure game_coroutines. You need to call `.start` on the
setup method and `.update` on the on_update.

### Start

Call start on your `setup` method:

```python
#main.py

from game_coroutines import CoroutineManager
...
...

def setup(self):
    ...
    CoroutineManager.start()
```

### Update

Update coroutine manager every FPS tick:

```python
#main.py
...
...

def on_update(self, delta_time):
    ...
    CoroutineManager.update(delta_time)
```

Call Coroutine
--------------

Now you can create your Coroutine and call it.

```python
#main.py

import arcade
from game_coroutines import Coroutine

...
self.player = #player sprite creation
...

def move_player(progress):
    self.center_x = arcade.lerp(0, 300, progress)

move_routine = Coroutine(delay=0.0, duration=10, progress_func=move_player)
move_routine()
```

### Callbacks

You can have callbacks to be called after a coroutine finishes. 

A callback can be any Callable object or a Coroutine (which is a Callable
object too).

```python
#main.py

import arcade
from game_coroutines import Coroutine

...
self.player = #player sprite creation
...

def move_player(progress):
    self.center_x = arcade.lerp(0, 300, progress)

def print_player_x_after():
    print(f'Finished moving at: {self.player.center_x}')

def scale_up_player(progress):
    self.center_x = arcade.lerp(1, 1.5, progress)

scale_routine = Coroutine(delay=0.0, duration=10, progress_func=scale_up_player,
    callback=print_player_x_after)
move_routine = Coroutine(delay=0.0, duration=10, progress_func=move_player,
    callback=scale_routine)

move_routine()
```

On the example above we have 2 coroutines: `scale_routine` and `move_routine`.

We first call `move_routine`. After it finishes, it will start the coroutine
`scale_routine` which is defined as callback.

After `scale_routine` ends, it will call the `print_player_x_after` function.

Sequence
--------

You can call a sequence of couroutines too:

```python
#main.py

import arcade
from game_coroutines import Sequence, Coroutine

...
self.player = #player sprite creation
...

def move_player(progress):
    self.center_x = arcade.lerp(0, 300, progress)

def scale_up_player(progress):
    self.center_x = arcade.lerp(1, 1.5, progress)

def scale_down_player(progress):
    self.center_x = arcade.lerp(1.5, 1, progress)

Sequence(
    Coroutine(delay=0.0, duration=10, progress_func=move_player),
    Coroutine(delay=0.1, duration=1, progress_func=scale_up_player),
    Coroutine(delay=0.1, duration=1, progress_func=scale_down_player)
)
```

Sequences starts after initializing, don't need to call it.

Contributions
-------------

Future Needs:

* tests
* accept callbacks with args
* [add your needs here]

PRs are welcome!

How to upload to Pip
--------------------

This section is for the maintainer to remember how to upload to pypi.
Move along.

```
python setup.py sdist
pip install twine
twine upload dist/*
```

