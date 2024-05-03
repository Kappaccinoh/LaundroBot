# LaundroBot AY23/24

## Table of Contents
### 1. Motivations
### 2. Prototyping and Solution
### 3. Challenges
### 4. Future Endeavours
### 5. Acknowledgements

### Motivations
Cinnamon College has two levels for students to do their Laundry - on Level 9 and Level 17. Each laundry room in Cinnamon College contains 5 Washing Machines (Washers) and 4 Dryers. LaundroBot started as an initiative by NUSCC’s Tech Directorate under Secretariate in order to facilitate the students’ usage of Washers and Dryers. This is done so by installing detectors on both washers and dryers in order to detect their washing/drying cycles, and inform students when a new washer/dryer is made available for them to use. This seeks to minimise the scenario in which students arrive at the Laundry Rooms only to realise that no washers/dryers are available for use.

### Prototyping and Solution
To detect whether washers/dryers are completed, we intend to paste small light sensors over the “wash/dry” LED lights on the washes/dryers themselves. These signals are relayed to an ESP32 which stores information about which LED has been activated/deactivated. The ESP32 updates this information to our server via HTTP Request over the school’s network, which updates our database. This database is fetch by our telegram bot which then publishes the status of the washers/dryers in the form of a text message - which can be accessed by students of Cinnamon College.

### Challenges
### Acknowledgements
#### LaundroBot Team AY23/24
Team Lead: Lim Jia Wei

Hardware Lead: Terence Chan

Backend Lead: Khoo Wui Hong

AutoCAD Lead: Reuben Thomas

Team Members: Ryan Warwick Han, Bertrand Wong, Ethan Loo

#### Special Thanks
HGS: Denice Yeo

Deputy HGS: Clara Cher

Tech Department Lead: Megan Loo

Maker's Studio Director: Soham Pujari



