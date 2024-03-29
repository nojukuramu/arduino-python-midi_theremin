import serial #serial library
import rtmidi #rtmidi library
import statistics #statistics useful for getting median later

#initialization of the midi
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# Print available MIDI ports
print(available_ports)

# Attempt to open the port
if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("VirtualMIDI")

ser = serial.Serial('COM4', 9600)

#list of notes is for the notes i want to send as midi notes. idstance are just gates to avoid shaky values
list_of_notes = [65, 66, 68, 70, 72, 73, 75, 77, 78, 80, 82]
distance_gate = [15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55]


 # Set MIDI channel to 1 explicitly in the status byte
status_byte = 0x90 | 0x00  # 0x90 is the note-on status, 0x00 is the MIDI channel (1)

#initialization of midichannel and volume_cc number
midi_channel = 1
volume_cc = 7

#function for sending the volume value as midi
def set_volume(value):
    midiout.send_message([0xB0 | (midi_channel - 1), volume_cc, value])

#basically just the map() of arduino library
def map(x, in_min, in_max, out_min, out_max):
  return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

#smoother of the inputs
def smoother(input_list):
    return round((sum(input_list)/len(input_list)))

#try block to catch errors
try:
    #initialization. dont change value unless you know what you are doing
    active_notes = set()
    snap_note = 0
    index = 0
    note_list = set()
    vol_list = set()
    cycler = 0
    #loop to read from serial monitor and send midi inputs
    while True:
        line = ser.readline().decode('utf-8')   #read serial monitor
        list_line = line.split()                #splitting and putting it on a list
        note_line = int(list_line[0])           #you know what this does
        vol_line = int(list_line[1])            #this onoe too
        mapvol = map(vol_line, 9, 30, 0, 127)   #remapping sonar output to midi inputs

        #keep mapvol above 0
        if mapvol < 0:
            mapvol = 0

        #collects input data and select the lower median
        if cycler < 10:
            note_list.add(note_line)
            vol_list.add(mapvol)
            cycler += 1
            continue
        else:
            cycler = 0
            note_line = statistics.median_low(note_list)
            mapvol = statistics.median_low(vol_list)
            note_list.clear()
            vol_list.clear()
            pass
        
        

        

        #distance gate to list of notes
        for items in distance_gate:
            if abs(items - note_line) <= 2:
                snap_note = list_of_notes[index]
                break
            index += 1
        index = 0

        #if input is 0, pitch should be 0 too
        if note_line == 0:
            snap_note = 0

        #Sending messages to midi
        midiout.send_message([status_byte, snap_note, 112])
        set_volume(mapvol)

        #just to keep the midi message limit not full
        active_notes.add(snap_note)
        if len(active_notes) > 20:
            for note in active_notes:
                midiout.send_message([0x80 | 0x00, note, 0])
                active_notes.remove(note)

        #Log just to track
        logger = [str(list_line), snap_note, mapvol]
        print("{: >12} {: >3} {: >3}".format(logger[0],logger[1],logger[2],))


except KeyboardInterrupt:
    pass

finally:
    midiout.close_port()
    ser.close()
    print("End")
