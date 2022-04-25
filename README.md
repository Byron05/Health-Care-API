# Medical_Platform
This application will serve as a platform to monitor patients at home or in the hospitals.

---

## User Stories
* Patients
  * Can enter measurements at any time
  * Can write a text or upload video/voice message to medical professional
  * Can book an appointment 
  * Can view their results
* Medical Professionals
  * Browse their patients
  * Assign medical devices to patients
  * Assign alert and scheduling for medical measurements
  * Can input data for their patients
  * Can chat with patients using text, voice, or videos
  * Can read transcripts of uploaded videos/messages
  * Search for keywords in messages and chats
  * Have a calendar to show availability
  * See all the appointments booked at any time
* Administrators
  * Add users to the system
  * Assign and change roles to users
  * Provide interfaces to third party medical device makers
  * Ability to disable or enable any device maker or application developer

---

## Table of Contents

- [Branching Strategy](#branching-strategy)
- [Setup](#setup)
- [Progress](#progress)

---

## Branching Strategy
A branch will be made for every module that will be implemented. The reason for this is to allow the developer to implement, experiment and test any new functionality without damaging the original code base. The code implemented in the different branches will only be merged with the main branch once it has been tested thoroughly and it is considered as the finished product for that module. 

The current branches in mind are the following:
* Device/Chat Module
* Mobile Application

---

## Setup

This repo uses python 3.9+.

After cloning the repository, it is recommended to use a virtual environment when working with the repo to avoid any conflict that may occur between different environments. With virtualenv installed you can create a new environment by running:

```
python3 -m virtualenv .venv
```

Then activate the environment:

```
source .venv/bin/activate (macOS/*nix)
.venv/bin/activate.cmd (Windows)
```

Then install the requirements:

```
python3 -m pip install requirements
```

---

## Progress

### Phases

Phase 0: 
- [x] Setup Agile environment for the project (including project, GitHub, testing, etc.).
- [x] Setup branching strategy.

Phase 1:   Device Module 
- [x] Define interface for devices to ingest data into the system.
- [x] Implement Unit Tests for the module.
- [x] Implement a simulation to send data via an example program.
- [x] Document the interface well.

Phase 2:   REST API
- [x] Use Flask or Django as your WEB service platform
- [x] Integrate module to become a RESTFUL system
- [x] Deploy system to free [Azure](https://health-care-api.azurewebsites.net/) services
- [ ] Document REST APIs on Github

Phase 3:   Mobile Application
- [ ] Get familiar with a cross platform framework
- [ ] Develop a simple mobile application
  - Integrate REST API
  - Implement User Module

### REST API Documentation
