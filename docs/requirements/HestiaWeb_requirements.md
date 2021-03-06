![Website Design](images/hestiaLogo.png  "Hestia Web Development Architecture Document")

### Clients
- F. te Nijenhuis
- L. Holdijk

### Authors
* A. Lalis
* T.K. Harrison
* R.T. Nijman
* P. Oetinger
* N. Dijkema
* E. Abdo
* R. Bell
* S. Oegema

### Teaching Assistant
Feiko Ritsema

## Introduction
The Hestia Home Automation System, developed by the clients, aims to make home automation simple again. The team last year developed a local server based system, which allowed users on that server to add and remove devices, and change the values of the activators of each device, essentially giving them complete control of all devices connected to that server. However the system has the following drawbacks: all changes are made through posting HTTP requests to the server, which is slow and unintuitive to the average user. Also, accessing the server can only be done locally. In order to improve the functionality of the system, we will be developing an online interface between a user and their local Hestia servers, as specified in the architecture document. The user will be able to log in through a webpage, see all their servers and the devices on each server, and be able to have quick, intuitive access to all the functionality currently provided by the clients' existing API system. This document details all the requirements that should be fulfilled by our project

## User Stories

The requirements for the system are from the perspective of all those who are going to use the system, i.e. via user stories. The user stories are formatted as follows: the description of the user (either *User*, *Developer*, or *Plugin Developer*, as defined below), their requirement, and the reasoning behind that requirement. The user stories reaffirm the context of the requirement and aid in the prioritization of development and re-specification. More user stories will be added as more requirements are discovered throughout the development process and following further consultation with the client.

The actors referenced throughout the user stories are defined in more detail below, so that the reasoning for each story is logical and motivated by a realistic desire or need.

#### User
The majority of the stories are focused around the *User*, which is someone who makes use of the Hestia system to automate peripherals in their home. The user probably does not care about the implementation or backend behavior, as long as their experience with the interface is satisfactory. The user, in general, wants the system to be as intuitive and easy to use as possible, while still providing complete control over the devices in their home.

#### Developer
The *Developer* is one who is responsible for designing the software that the user will interact with. They are most concerned with the structure and design of the system, and must make the application in such a way as to satisfy the users' needs and the clients' goals. Note that the developer in this scenario is not responsible for the pre-existing software provided by the clients.

#### Plugin Developer
The *Plugin Developer* is a person who has created a plugin that the Hestia system can manage. The plugin developer does not need to know a great deal about the user interface in order to develop plugins, and as such is more concerned with being able to publish their plugin and have it work successfully on all other Hestia local systems.

#### Critical user stories
- [x] As a user, I would like to be able to change the status of peripherals in all of my Hestia servers from one location, so that it’s easier for me to configure my home automation.
- [x] As a user, I would like to be able to add a new Hestia server to be remotely controlled.
- [x] As a user, I would like to be able to ensure that my Hestia servers and their devices cannot be controlled without my knowledge.
  - [ ] As a user, I would like to be able to access a log of events associated with my servers, so that I can see what changes have occurred. *Did not have time to implement this. However, the logs would best be stored by each local controller, and forwarded via the API to the central web application*
- [x] As a user, I would like to be able to ensure that my Hestia servers cannot be accessed without my consent.
  - [x] As a user, I would like to be able to set my authentication credentials, to ensure that I am the only one who can be authenticated by those credentials.
- [x] As a user, I would like to be able to share access to my Hestia server to other people who I trust, so that others who are affected by the peripherals can change things to suit them.
- [x] As a user, I would like to be able to easily add or remove plugins from my Hestia servers, so that it’s easy for me to test various peripherals.
- [x] As a user, I would like to be able to use the Hestia service without interruption.
  - [x] As a user, I would like fast responses to any input I make.
- [x] As a user, I would like to be able to easily add or remove plugins from my Hestia servers, so that it’s easy for me to test various peripherals.
- [x] As a developer, I would like the web front-end to communicate to the servers via the REST API, to have consistency in the design of the system.
- [x] As a user, I would like to be able to control my Hestia systems even when I am not on their local network.

#### Important User Stories
- [x] As a user, I would like to be able to view details about my Hestia servers from a central location, so that I can monitor their status easily.
- [x] As a user, I would like to be able to specify presets across my peripherals and apply those presets, so that I can quickly configure the peripherals to suit my preferences.
- [ ] As a user, I would like to be able to submit feedback to plugin developers, so that they can improve their plugin.
- [ ] As a plugin developer, I would like to be able to receive detailed and organised feedback, so I can improve my plugin.
- [ ] As a user, I would like to be able to be able to be able to put my devices into groups of my choice, in order to be able to find specific devices more easily.

#### Useful User Stories
- [ ] As a user, I would like to be able to donate to plugin developers, to show my support.
- [ ] As a user, I would like to be able to export and import configurations for my Hestia servers, to make it easier for me to deploy my systems.
- [x] As a user, I would like to be able to specify presets for my peripherals and apply those presets, so that I can quickly configure the peripherals to suit my preferences.
- [ ] As a user, I would like to be able to change the theme of the user-interface, so that it suits my preferences.

## Non-Functional Requirements
- [x] As a user, I would like to be able to use the Hestia service without interruption.
- [x] As a developer, I would like to have consistent style between my products.

## Won't Do
Below are listed some requirements or concerns which the clients have told us about, but due to resource requirements, legal issues, or other barriers, we know in advance that such features cannot be reasonably implemented.

* Add secret backdoor access to allow administrators to control the lights in any house where Hestia is installed.
* Make website available by localhost as well as through internet. (Client says this is not necessary, but we realize it would be good to improve accessibility)
* As a user, I would like to be able to set permissions for the servers or peripherals, so that I can limit what people who I have shared access with can do on my servers. *Not possible due to structure of backend on client side.*


## Scenarios
The scenarios are intended to flesh out the user stories shown above, by giving examples of how the system will be used once it is fully developed. Each scenario is an outline of a situation in which one probable user will use the system.

### Scenario 1:
Mr A is an office worker who commutes to and from work each day, and lives alone. Lately, his neighbourhood has been affected by a spate of burglaries. In order to reduce the chance of this happening to him, he wants to turn on the lights in his home when it gets dark, however he is rarely home early enough to do it manually. Instead, he can access the Hestia website through his workstation, log in with his credentials, access his server and devices, and turn his lights on.

### Scenario 2:
Ms. B runs a popular and large nightclub in the centre of the city. In order to improve the mood in the club, she has bought a large number of multi-coloured lights. However, changing the settings on each of these lights individually would take far too long, manually wiring them all to a central control system would be complicated, and since the lights come from a range of manufacturers, multiple apps would be needed to manage them all. As a solution, she uses the Hestia website through her phone, and is able to manage all her lights easily and effectively.

### Scenario 3:
Mr C is someone who currently works in a supermarket, however he is learning software development in his spare time and is thinking of becoming a full-time plugin developer. In order to gain a better understanding of his possible future success, he can release plugins on the Hestia plugin marketplace. There he will recieve detailed feedback on his work from potential users, and he will be able to make an informed choice about his future.







## Change Log

| Who             |       When | Where          | What                                                                                              |
| :---            |       :--- | :---           | :---                                                                                              |
| Troy Harrison   | 2018-02-27 | Whole Document | Added initial description, and basic user stories.                                                |
| Rens Nijman     | 2018-02-27 | Whole Document | Fixed typos and separated user stories by importance.                                             |
| Philip Oetinger | 2018-02-27 | Whole Document | Added user stories.                                                                               |
| Andrew Lalis    | 2018-02-27 | Whole Document | Added Hestia Logo, fixed grammar, added changelog. Defined actors for user stories.               |
| Andrew Lalis    | 2018-03-04 | Whole Document | Added TA name, Won't Do section, removed duplicate user story, added non-functional requirements. |
| Andrew Lalis    | 2018-03-12 | Document Name  | Renamed to HestiaWeb_requirements, added local website to Won't Do.                               |
| Rens Nijman     | 2018-03-12 | Won't Do       | Removed a space.                                                                                  |
| Troy Harrison   | 2018-03-13 | Requirements   | Move requirements to better reflect current focus.                                                |
| Roman Bell      | 2018-03-23 | Whole Document | Edited in preparation for final hand in.                                                          |
| Roman Bell      | 2018-03-27 | User stories   | Did checkboxes of features.                                                                       |
| Roman Bell      | 2018-05-29 | Whole Document | Did checkboxes of features, editing before final submission                                       |
| Troy Harrison   | 2018-05-29 | User stories   | Reorder user stories and provide motivation for requirements not met.              |Roman Bell      | 2018-06-01 | Introduction    | Reworked introduction                                       |
|Roman Bell      | 2018-06-03 | Scenarios       | Added scenarios                                      |
