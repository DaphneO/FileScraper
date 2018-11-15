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


def download_data_set_from_csv(csv_path, midi_directory):
    """
    Download a data set of MIDI files, as specified by the csv file in csv_path, and put them into midi_directory
    :param csv_path: Path to the csv file with lines in format [midi_name];[midi_url]
    :param midi_directory: Local location for the downloaded files
    """
    nr_successful = 0
    nr_unsuccessful = 0

    # Open the csv file
    with open(csv_path, 'r') as read_file:
        csv_content = read_file.readlines()
    for line in csv_content:
        midi_name, midi_url = line.rstrip().split(';')[:2]
        success, message = download_midi(midi_url, midi_directory, midi_name)
        if success:
            nr_successful += 1
        else:
            nr_unsuccessful += 1
            print(message)

    print(str(nr_successful) + ' MIDI files were downloaded successfully. ' + str(nr_unsuccessful) + ' failed.')
