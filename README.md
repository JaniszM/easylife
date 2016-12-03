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
- [Help and Improvements](#help-and-improvements)

# Why you should use this tool?

Everybody do certain activities like paying bills, segregating photos from smartphone, checking exchange rates or viewing certain sets of data against any new changes. Examples may be an infinite number. Each of it takes Your time. When activity is repeatable e.g. each week, and the time spent to do it extends, let's say one minute, then automating such activity makes sense. Easylife is about to be a set of such automated activities.

Purpose of the easylife first of all is to **save Your time** and release you from usually boring tasks.

*If you have the idea for automate an activity which can be useful for others please write to me: janiszewski.m.a@gmail.com*.

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

# Help and Improvements

If you have found some bugs, errors, something is not working as you want, something is not intuitive or something is missing and can be added or you just simply want to concribute then write to me: janiszewski.m.a@gmail.com.
Or make issue on GitHub.
Sometimes I check mails quite rarely but at least once per week ;)
