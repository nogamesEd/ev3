CheckMate Hardware control API
==============================

This is designed to allow super-easy heavily abstracted control of hardware components 
of the robot from the application logic running on the Pi, using the EV3's USB tethered 
network interface.

It uses the [Falcon](https://falconframework.org/) WSGI API framework and 
[bjoern](https://github.com/jonashaag/bjoern) as its WSGI app server.

All **GET** requests read state from the robot, **POST** requests are used to request
an change to the robot's state.

*WTF is this mess?* - blame Rob, this was his hideously overengineered solution.

Installation
------------

This has been built inside a conda env for easy portability and to save ruining
my personal pip environment, there's an `environment.yml` if you feel like using 
it.

The actual dependencies are in the `requirements.txt`, just `pip install -r` the 
file and you'll be good to go. bjoern needs GCC and the `libev-dev` package as
it uses a lot of C to make it speedy.

Running
-------

First you need to make sure the `Ylength` and `Xlength` entries in the Falcon request
options are correct. These should be in mm, and are in the Falcon object's
initialisation in `app.py`.

The `start.py` script handles getting WSGI started for you, so once everything is
installed give `python ./start.py` a try.

Endpoints:
----------

  - **POST** `/init`: 
    Asks the hardware to reinitialise, reset tachometers from limit switches
    and return to home position. Request completes when finished.

    ```(NO POST BODY)```
  
  - **GET** `/position`:
    Returns the current robot position in mm from the origin point (2-tuple: x,y)
  
  - **POST** `/position`:
    Requests the robot move to the requested (2-tuple: x,y) coordinate, distances in
    mm.

    ```json
    {
      'x': <requested x-pos in mm>,
      'y': <requested y-pos in mm>
    }
    ```

  **NOT YET IMPLEMENTED:**
  
  - **GET** `/grabber`:
    Returns current state of grabber.

  - **POST** `/grabber/height`:
    Requests the grabber move to the height in the request. Limited by limit
    switches/piece sensor.

  - **POST** `/grabber/grab`:
    Requests the robot close/activate the grabber (pump managed by ev3).

  - **POST** `/grabber/release`:
    Requests the robot release/deactivate the grabber (again specifics managed by
    the ev3)
  
  - **POST** `/grabber/lower`:
    Request grabber be lowered until piece is sensed. Returns the resulting z height
    of the grabber.
  
  - **POST** `/grabber/lowerandgrab`:
    Request grabber be lowered until piece is sensed, then activate grabber. Returns 
    the resulting z height of the grabber.

Structure
---------

The Falcon configuration is included in `app.py`, but all endpoints live as
individual classes in the `endpoints` directory. Create your API endpoints 
in here, import them into the main `app.py` and add them to a route within 
Falcon.
