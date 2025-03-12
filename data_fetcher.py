### required libs
import requests
from bs4 import BeautifulSoup as bs
import urllib.request
from zipfile import ZipFile as zf
import zipfile
import os
from pathlib import Path
import shutil
from colorama import Fore, Back, Style

##################################################
###             Get data from DISA             ###
##################################################
# Get OS Path
# print(os.getcwd())

# Set storage locations
file_location = os.getcwd() + '/file-imports/'
srg_folder = os.getcwd() + '/srgs/'
stig_folder = os.getcwd() + '/stigs/'
base_path = os.getcwd()

# Set up link
disa_url = 'https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/U_SRG-STIG_Library_January_2025.zip'

# Retrieve File
print(Back.YELLOW + f"Retrieving file from {disa_url}")
get_disa_file = requests.get(disa_url)

# Set file name
disa_file = disa_url.split('/')[-1]
print(f'File {disa_file} was retrieved')

# Store File
with open(disa_file,'wb') as output_file:
    output_file.write(get_disa_file.content)
print (Fore.GREEN + f'Stored {disa_file} in {base_path}')
print(Style.RESET_ALL)

##################################################
###           Extract and move files           ###
##################################################

# Extract files
print(Fore.MAGENTA + f'Extracting files to: {file_location}')
print(Style.RESET_ALL)
with zf(disa_file, 'r') as zObject:
    zObject.extractall(
       path=file_location)

# Move SRGs and STIGs
print(Fore.CYAN + f"Checking for SRGs and STIGs in: {file_location}")
files = os.listdir(file_location)
for f in files:
    if (f.endswith('SRG.zip')):
        print(Fore.CYAN + f'Moving {f} to {srg_folder}')
        shutil.move(file_location + f, srg_folder + f)
    elif (f.endswith('zip')):
        print(Fore.CYAN + f'Moving {f} to {stig_folder}')
        shutil.move(file_location + f, stig_folder + f)
print(Style.RESET_ALL)

# Unzip SRGs
for item in os.listdir(srg_folder):
    if not item.endswith('zip'):
        continue
    else:
        file_name = os.path.abspath(srg_folder + item)
        zip_ref = zipfile.ZipFile(file_name)
        zip_ref.extractall(srg_folder)
        zip_ref.close()
        os.remove(file_name)

# Unzip STIGs
for item in os.listdir(stig_folder):
    if not item.endswith('zip'):
        continue
    else:
        file_name = os.path.abspath(stig_folder + item)
        zip_ref = zipfile.ZipFile(file_name)
        zip_ref.extractall(stig_folder)
        zip_ref.close()
        os.remove(file_name)

# Sort actual SRG's 
for subdir, dirs, files in os.walk(srg_folder):
    for f in files:
        if (f.endswith('xml')):
            print(Fore.LIGHTYELLOW_EX + f'Moving {f} to {srg_folder}')
            file_path = os.path.join(subdir, f)
            shutil.move(file_path, srg_folder + f)

# Sort actual STIGs 
for subdir, dirs, files in os.walk(stig_folder):
    for f in files:
        if (f.endswith('xml')):
            print(Fore.LIGHTYELLOW_EX + f'Moving {f} to {stig_folder}')
            file_path = os.path.join(subdir, f)
            shutil.move(file_path, stig_folder + f)
print(Style.RESET_ALL)

##################################################
###             Clean up Files                 ###
##################################################

# Clean up File Download
if os.path.exists(disa_file):
    os.remove(disa_file)
    print(Fore.RED + f'Removed {disa_file} from {base_path}')
else:
    print('File does not exist')

# Clean up Files / Folders in SRG and STIG Directories
# Remove non-xml files from SRG directories
for subdir, dirs, files in os.walk(srg_folder):
    for f in files:
        if not (f.endswith('xml')):
            print(Fore.RED + f'deleting {f} from {srg_folder}')
            file_path = os.path.join(subdir, f)
            os.remove(file_path)

# Remove empty SRG directories
for item in os.listdir(srg_folder):
    if os.path.isdir(item):
        print(Fore.RED + f'Removing: ',os.path.join(os.getcwd(), item))
        os.removedirs(os.path.join(os.getcwd() , item))

# Remove non-xml files from STIG directories
for subdir, dirs, files in os.walk(stig_folder):
    for f in files:
        if not (f.endswith('xml')):
            print(Fore.RED + f'deleting {f} from {stig_folder}')
            file_path = os.path.join(subdir, f)
            os.remove(file_path)

# Remove empty STIG directories
for item in os.listdir(stig_folder):
    if os.path.isdir(item):
        print(Fore.RED + f'Deleting: ', os.path.join(os.getcwd(), item))
        os.removedirs(os.path.join(os.getcwd() , item))
print(Style.RESET_ALL)