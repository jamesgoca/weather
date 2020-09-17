# Weather Station

My personal weather station.

This weather station is accessible at [weather.jamesg.blog](https://weather.jamesg.blog).

## Setup

First, clone this repository:

```
git clone https://github.com/jamesgoca/weather
```

Next, set up a virtual environment and install the required dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Now you are ready to run this application:

```
python3 server.py
```

This application is accessible at ```localhost:5000```.

You must have a Raspberry Pi Sense HAT to run the scripts in the `get_weather` directory. This project will not work without having weather data collected and saved in `get_weather/data/data.json`.

## License

This project uses an MIT license. Read more about this project's license in [LICENSE.md](https://github.com/jamesgoca/weather/blob/master/LICENSE.md?raw=true).

## Screenshot

![A screenshot of my site](https://github.com/jamesgoca/weather/blob/master/screenshot.png?raw=true)

## Author

- James Gallagher
