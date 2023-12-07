# 2D Data Visualization

## Description

The application uses Pygame to visualize 2D matrixes. The program is extendable, enabling any nxn matrix to display its entries and the spatial relationship of other pixels.
The main purpose of the application is for our lab to visualize the sensor data and help us develop hardware (analog) design that is equivalent to traditional computer vision algorithms.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)

## Installation

Run the following code inside the repository's directory

```
pip install -r requirements.txt
```

## Usage

Run the program by running the App.py
```
python App.py
```
You will see the following user interface:

Click the "Open File" button to open the file explore. Go to the /data folder in the repository to see sample data.
You can open either .txt file or .npy file that has pre-recorded data at our lab (the person shadows are all my shadows under the sensors, no legal concerns).
Now you will see the empty canvas has all the pixels displayed in grey scale:

Now the "Play" and "Pause" buttons are activated, you can click them to start the recordings.
The "Smooth" button doubles the resolution using interpolation.

Now Enjoy me walking in circles.

Provide instructions and examples for use. Include screenshots as needed.

## Credits

pygame: http://pygame.org
pygame_gui: https://pygame-gui.readthedocs.io
numpy: https://numpy.org
scipy: https://scipy.org

