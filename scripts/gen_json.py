import json, glob
from pprint import pprint as pp

CSV_PATH  = '../db.csv'
IMG_PATH  = '../docs/assets/*'
JSON_PATH = '../docs/json/{}.json'
IMG_URL   = 'https://moncock.github.io/moncock-db/assets/{}'

TITLE     = 'Moncock'
DESC      = 'We are Moncock'

# prepare image mapper
img_mapper = {}
for path in glob.glob(IMG_PATH):
    filename = path.split('/')[3]
    img_mapper[filename[:3]] = filename

# load data from csv
chars = [ line.strip().split(',') for line in open(CSV_PATH, 'r') ]
chars = chars[1:] # remove header

# create json file
for (code, holder, artist) in chars:
    no       = code[4:]
    token_id = int(no)
    img      = img_mapper[no]
    dest     = JSON_PATH.format(token_id)

    # clean up data
    if not holder:
        holder = 'N/A'

    # craft data
    metadata = {
      'name'        : '{} #{}'.format(TITLE, token_id),
      'description' : DESC,
      'image'       : IMG_URL.format(img),
      'attributes'  : [
        { 'trait_type': 'PFP No',   'value': code },
        { 'trait_type': 'Holder',   'value': holder },
        { 'trait_type': 'Artist',   'value': artist },
      ],
    }

    # write file
    print(dest)
    #pp(metadata)
    with open(dest, 'w') as f:
        json.dump(metadata, f)
