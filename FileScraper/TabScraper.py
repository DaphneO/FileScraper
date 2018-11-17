from selenium import webdriver
from os import path


def download_tab(tab_url, tab_directory, tab_name):
    """
    Try to download a tab file from the Ultimate Guitar (given url) and place it in the tab_directory, called tab_name

    :param tab_url: Location of the tab file on the Internet
    :param tab_directory: Local directory where the tab file should be placed on your machine
    :param tab_name: File name of your tab file
    :return: Boolean indicating success or failure, message
    """

    target_path = path.join(tab_directory, tab_name)
    if path.isfile(target_path):
        return False, 'This file already exists'

    try:
        browser = webdriver.Firefox()
        browser.get(tab_url)
        tab_text = browser.find_element_by_xpath('//pre[@class="_1YgOS"]').text
        browser.close()

        with open(target_path, 'wb') as f:
            f.write(tab_text)
    except:
        return False, 'Error downloading ' + tab_name
    return True, 'Download succeeded'


def download_data_set_from_csv(csv_path, tab_directory):
    """
    Download a data set of tab files, as specified by the csv file in csv_path, and put them into tab_directory

    :param csv_path: Path to the csv file with lines in format [url];[name];[key];[filename]
    :param tab_directory: Local location for the downloaded files
    """
    nr_successful = 0
    nr_unsuccessful = 0

    # Open the csv file
    with open(csv_path, 'r') as read_file:
        csv_content = read_file.readlines()
    for line in csv_content:
        parts = line.rstrip().split(';')
        tab_url = parts[0]
        tab_name = parts[3]
        success, message = download_tab(tab_url, tab_directory, tab_name)
        if success:
            nr_successful += 1
        else:
            nr_unsuccessful += 1
            print(message)

    print(str(nr_successful) + ' tab files were downloaded successfully. ' + str(nr_unsuccessful) + ' failed.')
