#################################################################
# FILE: wave_editor.py
# WRITER: Eitan_Stepanov , eitanste1 , Tanya_Fainstein, t_fainstein
# EXERCISE: intro2cs2 ex6 2021
# DESCRIPTION: a program for editing and creating wav audio files
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED: None
#################################################################

from math import sin, pi

import os.path

from pathlib import Path

import wave_helper as help

# some constant massages

START_INPUT = ('please choose a number \n '
               '1. to editing \n '
               '2. for creating \n '
               '3. for quit \n')

EDIT_INPUT = 'Pleas choose wat to do with the file: \n' \
             '1. Revers audio \n' \
             '2. Audio canceling\n' \
             '3. Speed up\n' \
             '4. Speed down\n' \
             '5. Volume up\n' \
             '6. Volume down\n' \
             '7. Dimming effect\n' \
             '8. Saving and back to start\n'

FILE_NAME = 'Please provide a file name: \n'

WRONG_INPUT = 'Wrong choise. '


# some constants

VALID_NOTES = 'ABCDEFGQ'
EDITING_FUNCTIONS = '1234567'
SAVE_FUNCTION = "8"
MIN_VALUE = -32768
MAX_VALUE = 32767
VOLUME_FACTOR = 1.2
SAMPLE_RATE = 2000
SAMPLES_PER_1_16_SEC = 125
PI = pi

# notes

A = 440
B = 494
C = 523
D = 587
E = 659
F = 698
G = 784
Q = 0

FREQ_MAPPER = {'A': A, "B": B, "C": C, "D": D, "E": E, "F": F, "G": G, "Q": 0}


# functions

def sample(i, freq):
    """This function gets the number of the sample value and frequency that uses the formula
    given in the exercise by calculating the appropriate sample value."""
    freq = FREQ_MAPPER[freq]
    return int(MAX_VALUE * (sin(PI * 2 * (i * freq / SAMPLE_RATE))))


# edit functions


def revers_audio(sound):
    """This function executes reversing of the audio file """
    sound.reverse()
    return sound


def canceling_audio(sound):
    """ This function creates the canceling sound audio """
    sound1 = sound[:]
    for i, j in enumerate(sound1):
        sound[i] = [-j[0], -j[1]]
    return sound


def audio_speed_up(sound):
    """This function creates speeded up version of the file"""
    sound1 = sound[::2]
    return sound1


def average(x, y):
    """This function calculates the average of two numbers"""
    return int((x + y) / 2)


def audio_speed_down(sound):
    """This function creates speeded down version of the file"""
    new_sound = []
    for i, x in enumerate(sound):
        if i < len(sound) - 1:
            new_sound.append(x)
            new_sound.append([average(sound[i][0], sound[i + 1][0]),
                              average(sound[i][1], sound[i + 1][1])])
        if i == len(sound) - 1:
            new_sound.append(x)
    return new_sound


def audio_volume_up(sound):
    """This function increases the volume of the audio file"""
    sound1 = sound[:]
    for i, j in enumerate(sound1):
        sound[i] = [int(1.2 * j[0]), int(1.2 * j[1])]

        if sound[i][0] > MAX_VALUE:
            sound[i][0] = MAX_VALUE

        if sound[i][1] > MAX_VALUE:
            sound[i][1] = MAX_VALUE

        if sound[i][0] < MIN_VALUE:
            sound[i][0] = MIN_VALUE

        if sound[i][1] < MIN_VALUE:
            sound[i][1] = MIN_VALUE
    return sound


def audio_volume_down(sound):
    """This function decreases the volume of the audio file"""
    sound1 = sound[:]
    for i, j in enumerate(sound1):
        sound[i] = [int(j[0] / 1.2), int(j[1] / 1.2)]
    return sound


def average_2(x, y, z):
    """Calculates the average of 3 numbers."""
    return int((x + y + z) / 3)


def audio_dimming(sound):
    """This function dims up the sound of the volume"""
    new_sound1 = []
    for i, x in enumerate(sound):
        if i == 0:
            new_sound1.append([average(sound[i][0], sound[i + 1][0]),
                               average(sound[i][1], sound[i + 1][1])])
        if i == len(sound) - 1:
            new_sound1.append([average(sound[i][0], sound[i - 1][0]),
                               average(sound[i][1], sound[i - 1][1])])
        elif i != 0 and i != -1:
            if i < len(sound) - 1:
                new_sound1.append(
                    [average_2(sound[i - 1][0], sound[i][0], sound[i + 1][0]),
                     average_2(sound[i - 1][1], sound[i][1], sound[i + 1][1])])
    return new_sound1


# manage functions

def check_sound_request_validity(file_name):
    """Checks the existence of the file with the instructions"""
    if not os.path.exists(file_name):
        print("Please enter valid instructions file")
        return False
    return True


def read_instructions(file_name):
    """A function that receives an instruction file, adjusts it so that we can absorb the values of a character and
    the amount of sampling by inserting them into list. Function returns list"""
    sound_command_list = []
    sound_data = Path(file_name).read_text()
    sound_commands = ''.join(sound_data.split())
    sound_copy = sound_commands[:]
    for i in sound_copy:
        if i in VALID_NOTES:
            sound_command_list.append(i)
            sound_commands = sound_commands[1:]
            for j, k in enumerate(sound_commands):
                if k in VALID_NOTES:
                    sound_command_list.append(sound_commands[:j])
                    sound_commands = sound_commands[j:]
                    break

    sound_command_list.append(sound_commands)
    return sound_command_list


def create_data_list(sound_command_list):
    """This function runs the instruction file and creates an audio list"""
    sound = []
    for j in range(0, len(sound_command_list), 2):
        freq, num_of_iterations = sound_command_list[j],\
                                  int(sound_command_list[j + 1])
        for i in range(num_of_iterations * SAMPLES_PER_1_16_SEC):
            tmp_val = sample(i, freq)
            sound.append([tmp_val, tmp_val])
    return sound


def compose_sound(file_name):
    """This function operates the process of creating an audio"""
    sound_command_list = read_instructions(file_name)
    sound = create_data_list(sound_command_list)
    return sound


def create_sound(sound):
    """A function gets an empty list and manages the entire audio creation process. It checks that an instruction file
    exists and if so, runs the write_sound function we described earlier. Function returns the list of new audio lists
    and start input value, to automatically enter the file change menu"""
    while True:
        valid_input = False
        file_name = input(FILE_NAME)
        valid_input = check_sound_request_validity(file_name)
        if not valid_input:
            continue
        sound = compose_sound(file_name)
        start_input = '1'
        break
    return sound, start_input


def apply_changes(edit_input, sound):
    """A function that performs the change on the audio according to the user's choice and prints a message about the
    success of the execution"""
    if edit_input == '1':
        sound = revers_audio(sound)
    if edit_input == '2':
        sound = canceling_audio(sound)
    if edit_input == '3':
        sound = audio_speed_up(sound)
    if edit_input == '4':
        sound = audio_speed_down(sound)
    if edit_input == '5':
        sound = audio_volume_up(sound)
    if edit_input == '6':
        sound = audio_volume_down(sound)
    if edit_input == '7':
        sound = audio_dimming(sound)
    print('Success!')
    return sound


def edit_sound(sound, sample_rate):
    """A function that manages the process of modifying a existing file. if the sound list is an empty one, meaning it
    wasn't modified from the creation in the "main" function, we will conclude that user wants to modify an existing
    file. Else, we suppose that the user want to process changes on the file that was created inside the program.
    We will ask If the user wants to modify the file and we call the "apply changes" function.
    The while loop is responsible for the validity of the user's input.
    Invalid input will trigger the loop to start over again.  If the user wants to go to finish the process it
    moves him to the end menu (to save the file and exit the program)."""
    if not sound:
        while True:
            file_name = input(FILE_NAME)
            if help.load_wave(file_name) == -1:
                print(WRONG_INPUT)
                continue
            else:
                sample_rate, sound = help.load_wave(file_name)
                break
    while True:
        edit_input = input(EDIT_INPUT)
        if edit_input == SAVE_FUNCTION:
            break
        if edit_input in EDITING_FUNCTIONS:
            sound = apply_changes(edit_input, sound)
        else:
            print(WRONG_INPUT)
    end_menu(sample_rate, sound)
    return


def end_menu(sample_rate, sound):
    """A function that receives the audio after making all the changes and the sample value and uses the "save_wave" utility
    function to save the audio as a file on the computer."""
    file_name = input(FILE_NAME)
    help.save_wave(sample_rate, sound, file_name)


def main():
    """The main function that manages our code"""
    while True:
        sound = []
        start_input = input(START_INPUT)
        if start_input == '2':
            sound, start_input = create_sound(sound)
        if start_input == '1':
            while True:
                edit_sound(sound, SAMPLE_RATE)
                start_input = '3'
                break
        elif start_input == '3':
            break
        else:
            print(WRONG_INPUT)


if __name__ == '__main__':
    main()
