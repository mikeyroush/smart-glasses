# smart-glasses

This project implements image recognition along with text recognition and translation for a pair of smart glasses built with a raspberry pi zero

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes.

### Prerequisites

- A working command line
- A Google Cloud Services account
  - A JSON account token with access to the Cloud Vision API and the Cloud Translation API
- A Telegram JSON token (This part can be skipped if you wish to exclude the telegram functionality)

### Installing and Running

Download the zip then link the files in the command line via the makefile and run the executable

Navigate to the correct directory and utilize the makefile

```console
foo@bar:~$ cd /path/to/directory/here
foo@bar:~$ make all
```

This will have created a few .o files and an executable. To run it, do as follows...

```console
foo@bar:~$ ./Main
```

Demo

```console

```

Example output after converting ppm to a jpg

![map with greedy paths](map-input-844-480.dat.jpg)

## Authors

* **Michael Roush** - *Project completion*

## License

Copyright © 2017 Michael Roush. All rights reserved.

