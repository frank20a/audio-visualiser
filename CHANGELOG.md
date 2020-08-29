# Changelog

All notable changes to this project will be documented in this file.

# Releases

## [v1.4] - 29-08-2020
## Added
- Settings tab added on main application menubar.
- Added list to choose audio input device on settings tab.
- Added requirements.txt file for required Python3 modules.
## Changed
- License notice (will change again)
- Minor code reformatting

## [v1.3.1] - 17-06-2020
## Added
- Finished Settings Panel for TCP communication on beat detect
- Created connection UI for TCP communication with a console and ip/port selection
## Changed
- Fixed settings panels drawing over each other and overlapping
- Moved old utility scripts to different folder
- Minor Fixes

## [v1.3] - 11-06-2020
Introduced Sensor Screens. Sensors are modules that detect stuff (like beats) and do something with it.
### Added
- Added BeatDetector Class.
- BeatDetectorTCP subclasses BeatDetector and will connect to a remote host and send a TCP packet when detecting a beat
- Added support for size changing of screens
- Added settings for changing alignment of SpectrumLine
### Changed
- Fixed Size settings errors on boxes
- Fixed Colour change settings error
- Fixed y-dimension size changing not updating render area
- Minor Fixes

## [v1.2] - 30-05-2020
### Added
- Serial Connection added in the Layout Manager
- Created Arduino Firmware for communication. Transmition tested: barely fast enough at 250kBps baud rate. Recommended 500kBps or more (Arduino has been tested stable for up to 2MBps). Arduino code hasn't been tested with LEDs yet.
### Changed
- Minor Fixes

## [v1.1.2] - 17-05-2020
### Changed
- Changed audioInput.py to unpack data using numpy and float32 instead of int16 and built-in unpack() for more resolution and WAY more speed.
- Minor Bug Fix

## [v1.1.1] - 16-05-2020
### Changed
- Changed Spectrum default to ISO 31 band spectrum analiser frequencies with 40 pixels resolution
- Changes in audioInput.py. Deprecated bands displaying average of multiple frequencies (now display single frequency measurement)
- Default fft samples are now tripled (6144) in visualiser.py
- Changes in Spectrum Line to fit new single frequency change.
- Changes in Menus.py to fit new single frequency changes
- Minor Fixes

## [v1.1] - 26-04-2020
### Added
- Connections in Layout Manager now process data according to the LED Layout that the user provides
### Changed
- Minor Fixes

## [v1.0] - 26-04-2020
The first official non-beta release is marked by the integration of Audio Visualiser with the LED Screen Layout Manager. The software has reached a point where it is performing stabily enough and I can know call it COMPLETE. From now on I will keep updating with additions, fixes and new features.
### Added
- Integrated LED Screen Layout Manager with Audio Visualiser. Layout Manager is opened in a Process from Visualiser and shared data via Queue.
- Added menubar on Visualiser. Currently only adding screens and opening Layout Manager are functional.
- Visualiser screens have LIVE option when Layout Manager is open. The LIVE screen puts its frames into the shared Queue for the Layout Manager to read.
- Layout Manager now has Connection objects that transmit data received from the Visualiser. Currently they just dump the data.
### Changed
- Removed accidentally uploaded icon pack zip
- Minor Layout Manager menu fixes and additions

# Beta versions

## [v0.7-beta] - 25-04-2020
### Added
- Introduced the LED Screen Layout Manager. This program acts as a bridge between live input from Audio Visualiser and a microcontroller controlling individually addressable LEDs. Its job is to take the frames calculated by the Visualiser and communicate them over to the controller in a simple, serial manner. 
- Created menus for the two programs
- Created .info files that contain information about the programs version/license/etc.

## [v0.6-beta] - 07-04-2020
### Added
- ResponsiveBox box Screen
- ResponsiveStar box Screen
- ResponsiveHelix box Screen
### Changed
- Minor Bug Fixes

## [v0.5.4-beta] - 29-03-2020 to 06-04-2020
### Added
- [v0.5.2] Settings for Spectrum Line
- [v0.5.4] Started working on boxes Screen
### Changed
- [v0.5.1] The way settings menu works. Created custom tk widgets for each element.
- [v0.5.2] Improved the way tkinter code was implemented and added more widgets
- [v0.5.3] Reformatted code
- [v0.5.4] Fixed tkinter error when exiting
- [v0.5.4] Added back alignment for Spectrum Line

## [v0.5-beta] - 06-02-2020
### Added
- Spectrum Line effect (Pending settings)

## [v0.4-beta] - 28-01-2020
### Added
- Introduced the Application class. Application is subclassing tkinter.Tk effectively creating a real program GUI. The Application class contains a Window, integrating a pygame window inside a tkinter window
- Settings panels in the left of the window for every effect.
- Support for multiple screens in one window

## [v0.3-beta] - 26-01-2020
### Added
- Introduced the Screen class. Every effect/display will be subclassing Screen.
- Introduced the Window class. Window is effectively just a pygame window. Every Screen will be displayed within the Window object. A Window can contain many screens (currently works with 1)
- Almost every setting is dynamically changeable
### Changed
- Re-wrote large portion of code. Now everything is nice and organized in a correct Object-Oriented manner
- Improved beat detection

## [v0.2.1-beta] - 22-01-2020
### Added
- Gradient colouring for every effect
### Changed
- Bar height
- The way colours are calculated

## [v0.2-beta] - 22-01-2020
### Added
- Beat Detection Algorithm
- FPS counter
- Colour changing w/ beat detection (Test with Strobe by deadmau5)
- Colour fading effect
- Peak fall delay
### Changed
- Removed Blackman-Harris filtering from input (it muted some frequences)
- Minor fixes

## [v0.1-beta] - 21-01-2020
### Added
- Started working on the GUI
- Introduced the Spectrum Analiser: A nice, retro way to visualise audio


# Alpha versions

## [v0.0.1-alpha] - 21-01-2020
### Added
First alpha release contains:
- AudioInput: A module for capturing audio from input devices and processing it.
- live_spectrum: A simple proof-of-consept script that displays the FFT of the input audio signal
