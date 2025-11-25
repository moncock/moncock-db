import json, glob
from pprint import pprint as pp

CSV_PATH  = '../db.csv'
IMG_PATH  = '../docs/assets/*'
JSON_PATH = '../docs/json/{}.json'
IMG_URL   = 'https://moncock.github.io/moncock-db/assets/{}'

TITLE     = 'Moncock OG'
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
for (_, code, holder, artist, event, _, _, _, _, _, _, _) in chars:
    code     = code.strip()
    holder   = holder.strip()
    artist   = artist.strip()
    event    = event.strip()
    #
    no       = code[4:]
    token_id = int(no)
    img      = img_mapper.get(no, '999_genesis.png')
    dest     = JSON_PATH.format(token_id)

    # clean up data
    if not holder:
        holder = 'Unknown'
    if not artist:
        artist = 'Unknown'

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
    if event:
        metadata['attributes'].append({ 'trait_type': 'Event',   'value': event })

    # write file
    print(dest)
    #pp(metadata)
    with open(dest, 'w') as f:
        json.dump(metadata, f)
