from os import path
import urllib2


def download_midi(midi_url, midi_directory, midi_name):
    """
    Try to download a MIDI file from the Internet, (use midi_url) and place it in the midi_directory, called midi_name
    :param midi_url: Location of the MIDI file on the Internet
    :param midi_directory: Local directory where the MIDI file should be placed on your machine
    :param midi_name: File name of your MIDI file
    :return: Boolean indicating success or failure, message
    """

    # Remove .mid (or .MID) extension from the midi_name if necessary
    if midi_name[-4:].lower() == '.mid':
        midi_name = midi_name[:-4]

    # Check if the target file already existed - this should not be the case
    target_path = path.join(midi_directory, midi_name + '.mid')
    if path.isfile(target_path):
        return False, 'This file already exists'

    try:
        file_data = urllib2.urlopen(midi_url)
        data_to_write = file_data.read()

        with open(target_path, 'wb') as f:
            f.write(data_to_write)
    except urllib2.HTTPError:
        return False, 'Error downloading the file'
    return True, 'Download succeeded'
