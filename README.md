# LaundroBot AY23/24

## Table of Contents
### 1. Introduction
### 2. Prototyping and Solution
### 3. Performance
### 4. Challenges
### 5. Future Endeavours
### 6. Acknowledgements

### 1. Introduction
#### Motivations
Cinnamon College has two levels for students to do their Laundry - on Level 9 and Level 17. 
Each laundry room in Cinnamon College contains 5 Washing Machines (Washers) and 4 Dryers. 
LaundroBot started as an initiative by NUSCC’s Tech Directorate under Secretariate in order to facilitate the students’ 
usage of Washers and Dryers. The aim was to create an autodetection system that would ideally inform students when laundry
machines were done with its washing cycle, as well as to provide a real time update as to the status of washing machines
both at Level 9 and Level 17 - in use or not in use, so that students know exactly when to come down to their laundry when machines/dryers
are available.

#### Previous Attempts
Previous generations of LaundroBot Teams experimented with predominantly light sensors attached to the LEDs of
washing machines, each having one sensor as the primary means to detect whether a machine is on or off its washing cycle.
Other attempts included moving away from the washing machines, and trying to detect the payment gateway on the payment machine
opposite the washing machines in the laundry room. This would be done via the detection of electromagnetic fields emitted
from the payment machine which accepted several means of cashless payment including, QR Code, Paywave and EZLink.

Before taking over the current LaundroBot project, the main backend infrastructure done up by Wui Hong ran on an honours
based system, in which laundry/dryer users were to self update/self report the usage of washing machines. While this enabled
the AY23/24 Team to avoid much of the heavy lifting with regard to code, it was observed that uptake of the honours based system
was an issue, either due to unawareness of the system, and also adamance towards self reporting and using the honours system in general.

In this backdrop, the AY23/24 Team understood the necessity to ensure that new system was to be self running and convenient
as much as possible. We spectulate that these two factors if incorporated and mitigated via good design, will increase uptake and prove to
be an effective solution for the community living in Cinnamon.

At the time of writing, West Wing (Infra) runs their own similar LaundroBot system which runs on the same honours concept,
however the project was developed into a full-fledged application that could be downloaded on IOS and Android. The concept
is similar, just with a proper UI interface and user login abilities linked to their NUS account (citation needed). However, similar
to the previous implementation, the ground sentiment gathered indicated that uptake was not widespread throughout the community
even for a professional application done up by Infra.

### 2. Prototyping and Solution
Solutions towards the LaundroBot problem can be categorised into 3 broad categories. Invasive, Non-Invasive and Alternative
solutions. Invasive and Non-Invasive fall under the same umbrella category of involving the washing machine, and the
category of alternative referring to solutions that do not directly concern the washing machine. Invasive would mean opening
up the internal hardwares of the machine, and reading the signals directly from the machines' circuit board. While this would
definitely be accurate and 'at the source', this approach requires much more engineers to deal with the hardware, as well as
the red tape navigating both NUSCC Admin, Housing Services, and the LaundroMat Vendor. AY23/24 decided to proceed
with a Non-Invasive approach, which involved the usage of mounted sensors onto the washing machines itself.

#### Prototyping
We approached this problem considering the feedback of our predecessors that light sensors did not work out (amongst problems
with ensuring the mount was securely attached to the washers - we were generally advised against it), and decided to try 
alternative sensors, namely that of motion or touch/press sensors (either mounted on the doors of the washer/dryer or on 
the buttons on the machine's interface).

An initial reading using the motion sensors (accelerometers) proved to be ineffective as not only were the washing machines
wash cycles irregular (visual observation by hanging around the washing machine through its 30min~ wash cycle), but the bigger
problem was that the machines did not shake as violently enough for the accelerometer to detect significant readings. Furthermore,
washing machines and dryers were placed side by side each other in contact, so shaking from one machine would affect the
shaking of another machine (not that this shaking was to be detected but under the premise that our accelerometer was sensitive
enough, this solution would still pose challenges), which meant that readings may not be accurate to the specific washer.

Our alternative consideration was to experiment with using push sensors, either mounted on the interface of the washers/dryers,
with one push, depending on which sensor, meant that that machine was to be started and assumed to enter its wash cycle. Clearly
this solution has its own problems of false positives so we didnt explore it further. The alternative was to mount the sensors
onto the washing machine door, when doors were closed this also indicated an entry to the wash cycle, however it was noticed that
some washers would have finished and the doors were still kept closed, so the detection was not ideal. Furthermore, press
sensors were always subject to ware and tear, also subject to the same problem of mounting it securely - we didn't want to do much maintenance, so we stopped brainstorming at this point
and abandoned the option of using push sensors.

#### V1
Our last option was to use light sensors, specifically the old light sensors that were already wired up by previous LaundroBot
teams. To our surprise they were still functional and were as good as 'plug and play'. Experimenting using them proved to be
successful as a drop in the LED lights was enough to detect a considerable difference. The LED was to be positioned over the 'wash'
LED, which detected if the washing machine was on or off its wash cycle. A simple design set up was proposed as shown below.

![V1 Prototype 1.jpeg](images%2FV1 Prototype%201.jpeg)

Some design considerations included the placement of the housing so as to firstly not touch the top of the washer since it was
observed that most residents put detergent/washing liquids on the top of the machine; minimising interference meant that
the housing should be as un-intrusive as possible. Secondly, we knew that the LaundroMat contractor regularly serviced the
machines, some once a month, which involved the opening of the black flip out doors as seen by the knob keyhole on the black
pannel. This meant that this 'overhead flap' design would disrupt the opening of the machines.

In response to these considerations, we decided to move the housing to be mounted on the door itself entirely with minimal connections
to the body of the machine so as to un-hinder the servicing of the washing machines by external staff.

![V1 Prototyping Casing Concept.jpeg](images%2FV1%20Prototyping%20Casing%20Concept.jpeg)

In order to service all 5 machines, there were initial concerns voiced that the length of the wires would affect the sensitivity
of the light sensors due to increased resistance, as well as power travelling over increased distances. As such minimising the length of our light sensors was of priority. We came up with a possible placement
of the ESP32 to be placed in the center of all 5 machines so as to minimise range and the maximum length of light sensor wires
needed to be installed. An overlay image of this implementation is shown below, the main ESP32 is to be mounted on the W3 center
washer, with all the sensors and wires running from the W3 housing. The ESP32 casing was to be connected to the wall adjacent
wall plug.

![Overall Washer Set Up.jpeg](images%2FOverall%20Washer%20Set%20Up.jpeg)

#### V2
The housing was to be designed on AutoCAD with the appropriate measurements taken prior and 3D printed using NUSCC's Makers
Studio's 3D printer. The internal electronic circuits of the ESP were hacked and taken from spare breadboards and soldered in place.
The entire ESP was powered by a micro USB connected via a wall socket USB plug. We tested the set up on the nearest washer W5
to the wall as we did not have the required power cable to extend from W3 at that time, as we also did not plan to set up the
entire set up at one shot that day; additionally to avoid disruption amongst other Cinnamon laundry users with an incomplete set up.

![V2 Set Up Washer 5.jpeg](images%2FV2%20Set%20Up%20Washer%205.jpeg)

![V2 Washer Close Up.jpeg](images%2FV2%20Washer%20Close%20Up.jpeg)

We noted that we wanted to minimise any loose wires as much as possible by using double sided 3M waterproof tape, to keep
the overall set up clean and unintrusive as possible.

#### V3
The V2 model showed us a proof of concept and enabled us to detect the cycles of the W5 washing machine. Upon ordering the
necessary materials, we moved the placement of the ESP32 to W4 (initially planned to be on W3, however we realised that our power cable was not long enough; thankfully however
our light sensors were capable of reaching W1)

![V3 Sensor Close Up.jpeg](images%2FV3%20Sensor%20Close%20Up.jpeg)

Another major leap in hardware was the usage of pre-ordered printed circuit boards (PCBs). This made it clear which
components were to be soldered such that a non hardware trained individual (in the light of a manpower crunch;
technical expertise for soldering wouldnt be required as PCBs were generally thought of to be easy to pick up and teach
a layperson) was also able to help out for future scaling upwards to Level 9 and West Wing. This PCB was installed inside
the casing, however we do not have a specific photo showing it inside the casing.

![V3 PCB.jpeg](images%2FV3%20PCB.jpeg)


#### Software Implementation
These signals received from the light sensors are relayed to an ESP32 which stores information about which 
LED has been activated/deactivated. The ESP32 updates this information to our server via HTTP Request over the 
school’s network, which updates our database. This database is fetched by our telegram bot which then publishes the 
status of the washers/dryers in the form of a text message - which can be accessed by students of Cinnamon College.

### 3. Performance
The V3 model along with sensors and server were left on running for about 3 weeks for Level 17. Initial reactions to the publicised message indicated that the community was excited about its implementation, however
not enough research was done to gather feedback on its effectiveness or whether the community had been receptive towards LaundroBot
in this regard. However, with regard to the performance of the sensors and the server itself, no overloading was detected
and usage was generally stable, of course caveat - subject to NUS fluctuating Wifi.

### 4. Challenges
#### Hardware
We only had one hardware engineer on our team, so much of the challenges regarding implementation meant revolving around his
availabilities. Since much of the backend was already implemented and designed (minimal tweaking was needed), much of the heavy lifting
of this project lay on the hardware aspect - from deciding the design of the components, assembly, installation and debugging
on the spot if signals were being detected correctly.

#### Wiring
A big challenge was ensuring that the wires stayed glued to the machines as much as possible, however the 3M tape proved to be
ineffective for the washing machine surfaces, and needed constant reinforcement and periodic checking by the team to ensure
that the wires stayed on neatly. Our fix was to add a lot of tape, however in light of the washing machines moving about
on its own as well as by service staff, these wires came loose often, and was far from the ideal clean set up we had envisioned.

#### Light Sensors
The strong and sticky tape that we used was unfortunately transparent, which was sensitive enough to trigger a false positive
for the light sensors. Our quick fix was to tape them over with black tape to ensure that only light from the LEDs were being read.

#### Accuracy of Timing
We note that one unforseeable problem was that the washing machines had different wash settings. Meaning that one cycle could
vary from 30mins, 32mins and 34mins for light, medium and heavy washes respectively. Furthermore, our light sensor was installed
on the wash LED, which we thought was the correct LED to be attached on at the time, however upon further inspection we realised
that this 'wash' LED does not exactly correspond to the wash cycle - it represents the cycles in which the washing machine delivers water
to the wash, with the last 4~ mins of the wash cycle to be only rapid spinning of the drum to "dry" the clothes and remove execess
water. 

Our quick fix was to blanket the updating of the light sensors to a fixed 32 mins on the backend, as we had no idea whether settings were
30mins or 34mins. The net effect was the timings reflected on the telegram chat were not entirely accurate, and could deviate up to 8mins
at max.

#### LaundroMat Contractors
Part of why this project did not succeed was largely due to the priority that LaundroMat Contractors took when servicing
laundry machines. In our defence, we underestimated the frequency of servicing from the service staff, and we also underestimated the extent
of which washing machines could be moved/disruptive to our set up. Due to the design of our current set up, we were not made aware that contractors might need to move the
entire washing machine out from its location in order to access the back of the machine. This was to replace the belt which
kept the machines running and was understandably susceptible to wear and tear. With the wires secured and essentially mounted
onto the machines, we did not foresee the need for the machines to be moved in and out of its place. Moving even one machine
implied that the connecting wires were to be strained and pulled, often being torn off the machines. 

At the time it was decided to remove the set up entirely as the team did not see that re-installing/re-taping the wires back on was a sustainable method
each time the machines needed to be secured on. Leaving the wires droopy and exposed was decided to be unclean and potentially
disruptive to regular usage of the washing machines, and hence the project was discontinued.

### 5. Future Endeavours
This attempt largely set the groundwork for LaundroBot for the upcoming teams. A proposed solution/pathway for a future solution that
is long lasting would be as follows. 
1. Use wireless light detectors mounted on the "Lock" LED (an LED that corresponds directly
to the wash cycle) rather than the "Wash" LED.
2. Use mounts that can be detached easily 
3. Use battery powered solutions rather than wired socket solutions. 

We believe this solution would
largely solve all the problems faced by using a wired solution during our tenure, and we wish the future LaundroBot Teams the best of luck.

### 6. Acknowledgements
#### LaundroBot Team AY23/24
Team Lead: Lim Jia Wei

Hardware Lead: Terence Chan

Backend Lead: Khoo Wui Hong

AutoCAD Lead: Reuben Thomas

Team Members: Ryan Warwick Han, Bertrand Wong, Ethan Loo

#### Special Thanks
AY23/24 HGS: Denice Yeo

AY23/24 Deputy HGS: Clara Cher

AY23/24 Tech Department Lead: Megan Loo

AY23/24 Maker's Studio Director: Soham Pujari

AY22/23 Tech Department Lead: Cheng Yi


<br>
Prepared By: Lim Jia Wei



