Read this in other language: [English](README.md), [Polski](README.pl.md).

**FULL Documentation currently available only in [Polish](README.pl.md).** English will soon be completed.

A module that gathers useful tools / scripts that makes life easier. Automates same things you can do every day.

TOC:

- [Why you should use this tool?](#why-you-should-use-this-tool)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)
- [Tools and Scripts](#tools-and-scripts)
    - [Transfers](#transfers)
        - [Requirements](#requirements)
        - [Configuration](#configuration)
        - [Running](#running)
        - [Usage](#usage)
        - [User support](#user-support)
    - [Photo and Video Organizer](#photo-and-video-organizer)
        - [Running and Usage](#running-and-usage)
- [Help and Improvements](#help-and-improvements)

# Why you should use this tool?

Everybody do certain activities like paying bills, segregating photos from smartphone, checking exchange rates or viewing certain sets of data against any new changes. Examples may be an infinite number. Each of it takes Your time. When activity is repeatable e.g. each week, and the time spent to do it extends, let's say one minute, then automating such activity makes sense. Easylife is about to be a set of such automated activities.

Purpose of the easylife first of all is to **save Your time** and release you from usually boring tasks.

*If you have the idea for automate an activity which can be useful for others please write to me: janiszewski.m.a@gmail.com*.

# Known problems

**Transfers:** Currently some locators for mbank are out of date, new version will be released soon.

# Requirements

- Python 2.7.
- geckodriver.

# Installation

Install easylife:
```
pip install easylife
```

After installation et geckodriver:
```
sudo easylife get-geckodriver
```

If you have already geckodriver add it to PATH system environment or move to:
`/usr/bin` in case of OSX or Linux system.

# Configuration

# Running

```
easylife <tool>

e.g.:
easylife transfers
```

# Tools and Scripts

## Transfers

*Tool purpose: pay series of bills by electronic transfers.*

Currently supported bank's interfaces:
- mbank \(Polish version\) **https://www.mbank.pl/indywidualny/**

### Requirements

### Configuration

### Running

```
easylife transfers
```

### Usage

### User support

## Photo and Video Organizer

*Purpose of the tool: organize or archive photo and video collections.*

The tool is recursively searching given path against graphic or video files. Then it moves found files to the given directory according to the given path structure and naming.
It uses EXIF metadata to locate date of the photo. In case of missing EXIF the tool tries to read date of the file creation.

The Template used to create directory structure where files are moved:
- YYYY: the year, will be replaced by date of file creation,
- MONTH or MM: the month,
- DD: the days,
- NAME: name of the currently moved file,
- splitters, '-' and '/'.

Files with known extensions are processed only. The list of the extensions can be found in `easylife/photo_organizer/__init__.py`. 

Tested on:
- OSX Yosemite,
- Windows 7.

### Running and Usage

```
easylife photo [params]
```

Parameters:
- source_dir: the directory where files for processing are placed,
- destination: the dir where processed file will be put,
- template: the template according to organize processed files,
- (OPTIONAL) remove-source: if param set then source dir (source_dir) will be removed,
- (OPTIONAL) overwrite-existing: if param set then in case any file collision these from *destination* will be replaced by files from *source_dir*. 

**EXAMPLES**
```
# Photo Backup from phone SD card to the dirs ./my_backup/photo/2017/05-21-DCIM0000001.jpg. Duplicates in ./my_backup/photo will be overwritten.
easylife photo /my_phone_card/photo ./my_backup/photo /YYYY/MM-DD-NAME overwrite-existing

# Photo Backup from phone SD card to the dirs ./my_backup/video/2017-03/funny1234.avi. Dir /my_phone_card/video will be removed.
easylife photo /my_phone_card/video ./my_backup/video /YYYY-MM/NAME remove source
```

# Help and Improvements

If you have found some bugs, errors, something is not working as you want, something is not intuitive or something is missing and can be added or you just simply want to concribute then write to me: janiszewski.m.a@gmail.com.
Or make issue on GitHub.
Sometimes I check mails quite rarely but at least once per week ;)
