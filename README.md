# dummy
> The projet aims to provide a bot interacting with collaborative editing applications for simulating large scale virtual collaborative scenarios

[![Build Status](https://travis-ci.org/coast-team/dummy.svg?branch=master)](https://travis-ci.org/coast-team/dummy)

## How to run the bot
At this time, there are to way for dealing with the bot (dummy):
* Use of HTTP API (C&C server)  : easier way
* Use of API exposed by controller module

### General purposes about dummy

The dummy configuration is discribed in ".ini" config file. You can see some examples in the [config_files folder](./config_files)
The path to the configuration file is required for running the dummy.

#### Documentation : configuration file

### How to deal with dummy through HTTP API

#### Documenation : HTTP API
| Path                                           | Method | Action                                 |
| ---------------------------------------------- | ------ | -------------------------------------- |
| /get/status/                                   | GET    | Get server status                      |
| /create/[collaborator type]/collaborator       | POST   | create a collaborator instance         |
| /start/[collaborator type]/collaborator        | PUT    | start the interactions (collaboration) |
| /stop-writing/[collaborator type]/collaborator | PUT    | stop writing                           |
| /stop-reading/[collaborator type]/collaborator | PUT    | stop reading                           |
