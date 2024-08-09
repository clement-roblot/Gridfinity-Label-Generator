# Gridfinity bin sticker generator

This project aims at building a sticker generator exported as a pdf of stickers that you can then print on a regular printer.

The "killer" feature of this project is the use of [Open CASCADE](https://www.opencascade.com/) to dynamicaly render the 3d view of the object showed on the sticker.

## Intro video

[![Intro video](https://img.youtube.com/vi/FzSsLz4fwTY/0.jpg)](https://youtu.be/FzSsLz4fwTY)

## Install

How to build the proper environnement:

```bash
conda create -n pyoccenv python=3.8
conda activate pyoccenv
conda install -c conda-forge pythonocc-core pillow pyside6 qrcode
```

## Run

Then once installed, just activate the environnement and run the GUI:

```bash
conda activate pyoccenv
python main.py
```

## Finding 3d models

Its great to be able to make nice stickers from 3d models but I'm not gonna model all the screw size I got for this. Not to worrie the internet is full of 3d models for most mechanical things. An amazing resource for this is [McMaster-Carr](https://www.mcmaster.com/) where you can find the step files of basicaly everything mechanical.

The meca folder contains a step file as exmemple, it is taken from [here](https://grabcad.com/library/ph-philips-sscrew-1).

## Additional customization

You can edit the json with the details of your stickers and them render it manually with the command:

```bash
python generator.py exempleSheet.json
```

A few advanced are not accessible in the GUI like the page size in mm. You can also add a font parameter to specify the font used to render the texts, for example:

```bash
"font": "/usr/share/fonts/truetype/msttcorefonts/times.ttf",
```
