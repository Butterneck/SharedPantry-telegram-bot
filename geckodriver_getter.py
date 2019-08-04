import platform
import requests
from sys import exit
import tarfile
import os

from Utils import terminalColors
from tqdm import tqdm


def get_geckodriver_binary(path="./geckodriver"):
    pbar = tqdm(total=100, postfix="Download latest releases")

    url_to_latest = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    r = requests.get(url_to_latest)
    pbar.update(25)
    pbar.set_postfix_str("Ricerca URL per il download")

    json_r = r.json()
    if platform.system() == 'Linux':
        platform_name = 'linux64'
    elif platform.system() == 'Darwin':
        platform_name = 'macos'
    else:
        pbar.set_postfix_str("Abort")
        print(terminalColors.FAIL + "Not tested on this system")
        print("Abort" + terminalColors.ENDC)
        exit(1)

    for asset in json_r['assets']:
        if platform_name in asset['browser_download_url']:
            pbar.update(25)
            pbar.set_postfix_str("Download tar.gz file")
            gz_url = asset['browser_download_url']
            gzip_data = requests.get(gz_url).content

            geckodriver_file_zipped = open(path + "_.tar.gz", 'wb')
            geckodriver_file_zipped.write(gzip_data)
            geckodriver_file_zipped.close()

            pbar.update(25)
            pbar.set_postfix_str("Uncompressing file")
            tar = tarfile.open(path + "_.tar.gz")
            tar.extractall()
            tar.close()
            pbar.update(25)
            pbar.set_postfix_str("Finished")
            os.remove(path + "_.tar.gz")
            pbar.close()
            return True
    return False
