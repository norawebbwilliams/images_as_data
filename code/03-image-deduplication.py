"""
Purpose: Example Python script for deduplicating images
"""

from PIL import Image
import os
import re
import math
import operator
import csv
from shutil import copyfile
import collections
from functools import reduce

############## User Specific Variables #####################
# Setting working directory, if you are using a matching project file structure
# Assuming you are running the script in command line
# from your project code directory and Python subdirectory
root_directory = os.getcwd()
# Subs out any part of the path after the root of the folder containing your code
root_directory = root_directory.replace('\\code\\python', '')
root_directory = root_directory.replace('/code/python', '')

# Sets relative directory paths for deduplication
MAIN_PATH = os.path.join(root_directory, 'data') # Data directory in root folder
IMAGES_PATH = os.path.join(MAIN_PATH, 'raw_images') # Where the images you want to deduplicate are stored; recommended as subdirectory of project data directory
UNIQUE_PATH = os.path.join(MAIN_PATH, 'unique_images') # Where to copy set of unique images if you want to; recommended as subdirectory of project data directory

# Or uncomment and set absolute paths if you prefer
# MAIN_PATH = ''path_to_where_you_will_store_deduplicated_csv/'' 
# IMAGES_PATH = ''path_to_where_raw_images_are_stored/''
# UNIQUE_PATH = ''path_to_where_you_will_store_a_copy_of_each_unique_image/''

copy_unique_images = 'no' # If yes, will copy unique images to Unique Images path

os.chdir(MAIN_PATH)

############### FUNCTIONS #################
# Gets file sizes for files in a given directory
def get_file_size(dirname, file_list, reverse=False):
    '''''' Return list of file paths in directory sorted by file size ''''''
    # Get list of files
    filepaths = []
    for item in file_list:
        filepaths.append(item['id'])
    counter = 0
    # Re-populate list with filename, size tuples
    for i in range(0,len(filepaths)):
        counter += 1
        if counter % 1000 == 0:
            print('...got size for ' + '[' + str(counter) + '/' + str(len(filepaths)) + '] images...')
        size = (os.path.getsize(os.path.join(dirname,filepaths[i])))
        file_list[i]['size'] = size
    return file_list


# Defining Ordered Set
class OrderedSet(collections.Set):
    def __init__(self, iterable=()):
        self.d = collections.OrderedDict.fromkeys(iterable)
    def __len__(self):
        return len(self.d)
    def __contains__(self, element):
        return element in self.d
    def __iter__(self):
        return iter(self.d)


# - loading a csv list with the IDs of all processed images so far called `checked_images.csv', 
# with one column for file_id, which is the filename of images that have already been deduplicated
# If the `checked_images.csv' does not exist, the script will create an empty list of checked images and will add images to this list for output at the end
row_count = 0
checked_images = []
if os.path.exists(os.path.join(MAIN_PATH, 'checked_images.csv')):
    with open('checked_images.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row_count += 1
            if row_count != 1:
                dic = {}
                dic['file_id'] = row[0]
                checked_images.append(dic)
                

checked_images_ids = [t['file_id'] for t in checked_images]


# - loading the previous csv table of matched images, called `images_matches.csv',
# If the `checked_images.csv' does not exist, the script will create an empty list of checked images and will add images to this list for output at the end
print('Loading past matches...')
row_count = 0
matched_images = []
if os.path.exists(os.path.join(MAIN_PATH, 'images_matches.csv')):
    with open('images_matches.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row_count += 1
            if row_count != 1:
                dic = {}
                dic['id'] = row[0]
                dic['matches'] = row[2]
                dic['matched_to'] = row[1]
                matched_images.append(dic)

matched_images_ids = [t['id'] for t in matched_images]

# Building a list of new image files (e.g. that haven't already been checked):
print('Loading new images...')
os.chdir(IMAGES_PATH)
filenames = [filename for filename in os.listdir(IMAGES_PATH) if re.search('.jpg', filename) and filename not in checked_images_ids]

# Creating the main table to hold info
#   about which images are similar:
counter = 0
for f in filenames:
    counter += 1
    if counter % 1000 == 0:
        print('...loaded ' + '[' + str(counter) + '/' + str(len(filenames)) + '] images...')
    if f not in matched_images_ids:
        dic = {}
        dic['id'] = f
        dic['matched_to'] = ''
        dic['matches'] = []
        matched_images.append(dic)


print('Sorting new images by size...')
unsorted_main = get_file_size(IMAGES_PATH, matched_images)

print(unsorted_main[0:4])

main = sorted(unsorted_main, key=lambda k: k['size']) 

print(main[0:4])

main_names = []
for entry in main:
    new_name = entry['id']
    main_names.append(new_name)

print(main_names[0:4])

# An empty vector where we will store the images that
#   have been already matched to another image
matched = []
match_count = 0

############    
# The algorithm that compares all the images:
############
os.chdir(IMAGES_PATH)

for i in range(0,len(main)):
    if main_names[i] in matched:
        continue
    else:
        print('STARTING WITH IMAGE n.' + str(i) + '/' + str(len(main_names)) + ': ' + str(main_names[i]))
        others = list(OrderedSet(main_names)-OrderedSet(matched))
        current = others.index(main_names[i])
        del others[current]
        try:
            img1 = Image.open(main_names[i]).histogram()
        except KeyboardInterrupt:
            raise
        except IOError:
            matched.append(main_names[i])
            main[i]['matched_to'] = 'NO IMAGE'
            continue
        main[i]['matched_to'] = 'root'
        for j in others[current-3:current+7]:
            try:
                img2 = Image.open(j).histogram()
            except KeyboardInterrupt:
                raise
            except IOError:
                matched.append(main_names[i])
                main[main_names.index(j)]['matched_to'] = 'NO IMAGE'
                continue
            if len(img1) != len(img2):
                continue
            rms = math.sqrt(reduce(operator.add,
            map(lambda a,b: (a-b)**2, img1, img2))/len(img1))
            if rms == 0:
                match_count += 1
                checked_images.append({'file_id': j})
                checked_images_ids.append(j)
                if main[i]['matches'] == []:
                    main[i]['matches'] = str(j)
                else:
                    main[i]['matches'] = str(str(main[i]['matches']) + ', ' + str(j))
                if main[main_names.index(j)]['matches'] != []:
                    print('-----Replacing old match data with new match data-----')
                    main[i]['matches'] = str(str(main[i]['matches']) + ', ' + str(str(main[main_names.index(j)]['matches'])))
                main[main_names.index(j)]['matched_to'] = main_names[i]
                matched.append(main_names[main_names.index(j)])
                print('Image ' + str(j) + ' matched with ' + str(main_names[i]))
        checked_images.append({'file_id': main_names[i]})
        checked_images_ids.append(main_names[i])

os.chdir(MAIN_PATH)                

output = []
for entry in main:
    if entry['matched_to'] == 'root':
        output.append(entry)
        if copy_unique_images == 'yes':
            if os.path.exists(os.path.join(UNIQUE_PATH, entry['id'])) == False:
                copyfile(os.path.join(IMAGES_PATH, entry['id']), os.path.join(UNIQUE_PATH, entry['id']))

print('Matched ' + str(match_count) + ' images on this run through')

print('Writing databases to .csv')

with open(os.path.join(MAIN_PATH, 'images_matches.csv'), 'w+', newline='') as f:
    document = csv.DictWriter(f,output[0].keys())    
    document.writeheader()
    document.writerows(output) 


with open(os.path.join(MAIN_PATH, 'checked_images.csv',), 'w+', newline='') as f:
    document = csv.DictWriter(f,checked_images[0].keys())    
    document.writeheader()
    document.writerows(checked_images) 
