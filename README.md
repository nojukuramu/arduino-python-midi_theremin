# arduino-python-midi_theremin

##Setup:
1. Arduino or anything that works similar
    - Upload the code to the arduino
2. 2 Sonar Sensors
    - Power 2 sonars with 5v and gnd it
    - The code use 1 pin for both trigger and echo. tap them together and put each sensor in pin 8 and pin 9
3. Install Python RTMidi and LoopMIDI software
    - please see this for detailed instruction: https://github.com/AhmadMoussa/Python-Midi-Ableton/blob/master/Readme.md
4. Any Daw. I use Ableton the same with the link above

##Basic Concept of the project:
*We want to get the sensor value of sonar using the arduino and send it to python and use it to convert to midi and send it to ableton as inputs.
1. Arduino prints the sensor value to serial monitor
2. Python reads the sensor value from Serial Monitor
3. Python process the sensor values and send it to virtual midi port created by loopMidi
4. DAW, such as Ableton, receives MIDI Inputs from loopMidi's virtual midi
