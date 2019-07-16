# pokemon-web-scraper

Scrap the image and basic information of the 809 Pokemon from the https://www.pokemon.com site. This repository is only for didactic purposes.

## Resourses

- Check the **Pokedex site**: https://www.pokemon.com/us/pokedex/

- **Beautiful Soup** library: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## Step by step

### 1. Set the Python 3 environment.

Set a new virtual environment with the required libraries.

```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install requests beautifulsoup4 lxml pandas
```

Remember you can also use the `requirements.txt` file.

```bash
$ pip install -r requirements.txt
```

The required **libraries** for this exercise are:

```python
import os
import re
import requests

import bs4 as bs
import pandas as pd
pd.set_option('display.max_columns', 20)
```

### 2. Building a CSV file with all the Pokemons.

Out of the blue, from the [pokemon-pokedex site](https://www.pokemon.com/us/pokedex/), generate a csv-file listing all the pokemons, the number and the **url location** where all the information of the Pokemon exists.

The csv-file should look like this:

| number | name        | ref                     |
|--------|-------------|-------------------------|
| 1      | bulbasaur   | /us/pokedex/bulbasaur   |
| 2      | ivysaur     | /us/pokedex/ivysaur     |
| 3      | venusaur    | /us/pokedex/venusaur    |
| 4      | charmander  | /us/pokedex/charmander  |
| 5      | charmeleon  | /us/pokedex/charmeleon  |
| ...    | ...         | ...                     |
| 806    | blacephalon | /us/pokedex/blacephalon |
| 807    | zeraora     | /us/pokedex/zeraora     |
| 808    | meltan      | /us/pokedex/meltan      |
| 809    | melmetal    | /us/pokedex/melmetal    |

The pokedex site is `https://www.pokemon.com/us/pokedex/`.

```python
# 1. Get the HTML Source File.
url = "https://www.pokemon.com/us/pokedex/"
r = requests.get(url)
soup = bs.BeautifulSoup(r.content, 'lxml')

# 2. Extract the data and append it to a list.
pokedex = []
for sec in soup.find_all('li'):
    for link in sec.find_all('a'):
        if 'href' in link.attrs.keys():
            if re.search(r'/pokedex/(.+)', link['href']):
                pokemon = link.text
                pokemon = pokemon.split(' - ')
                pokemon = [x.strip() for x in pokemon]
                pokedex.append({
                    'name': pokemon[1].lower(),
                    'number': int(pokemon[0]),
                    'ref': link['href']
                })

# 3. Generate a dataframe.
pokedex = pd.DataFrame(pokedex)[['number', 'name', 'ref']].copy()

# 4. Download the file as csv.
pokedex.to_csv('files/pokedex.csv', index=False)
```

### 3. Get the Pokemon Types.

Using only the first 15 Pokemons, extract the pokemon types. Generate a new csv-file with the information of the pokemon name, number, href, type and image location url.

The result of this section must be a file with 15 rows, one for each Pokemon.

| number | name       | ref                    | img_url                                                         | type         |
|--------|------------|------------------------|-----------------------------------------------------------------|--------------|
| 1      | bulbasaur  | /us/pokedex/bulbasaur  | https://assets.pokemon.com/assets/cms2/img/pokedex/full/001.png | grass-poison |
| 2      | ivysaur    | /us/pokedex/ivysaur    | https://assets.pokemon.com/assets/cms2/img/pokedex/full/002.png | grass-poison |
| 3      | venusaur   | /us/pokedex/venusaur   | https://assets.pokemon.com/assets/cms2/img/pokedex/full/003.png | grass-poison |
| 4      | charmander | /us/pokedex/charmander | https://assets.pokemon.com/assets/cms2/img/pokedex/full/004.png | fire         |
| 5      | charmeleon | /us/pokedex/charmeleon | https://assets.pokemon.com/assets/cms2/img/pokedex/full/005.png | fire         |

```python
def getPokemonType():

    pok_url = "https://www.pokemon.com"
    img_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{}.png"

    pokedex = pd.read_csv('files/pokedex.csv').head(15)

    pokemon_type = []
    for index, row in pokedex.iterrows():

        # 1. Get the HTML file from each pokemon.
        full_pok_url = pok_url + row['ref']
        r = requests.get(full_pok_url)
        soup = bs.BeautifulSoup(r.content, 'lxml')

        # 2. Append the types to the list.
        type_list = []
        for section in soup.find_all('ul'):
            for link in section.find_all('a'):
                if link['href'] == row['ref']:
                    for _type in link.find_all('li'):
                        type_list.append(_type.text.lower())

        type_str = '-'.join(type_list)

        # 3. Generate the image url.
        old_img_name = "{0:0=3d}".format(int(row['number']))
        full_img_url = img_url.format(old_img_name)

        pokemon_type.append({
            'name': row['name'],
            'number': row['number'],
            'ref': row['ref'],
            'type': type_str,
            'img_url': full_img_url
        })

    pokemon_type = pd.DataFrame(pokemon_type)
    pokemon_type.to_csv('files/pokedex_types.csv', index=False)
```

### 4. Download the Pokemon image.

Generating a file-directory structure as follows:

```text
images/
├── ok
│   ├── bug
│   │   ├── 010-caterpie.png
│   │   ├── 011-metapod.png
│   │   ├── 012-butterfree.png
│   │   ├── 013-weedle.png
│   │   ├── 014-kakuna.png
│   │   └── 015-beedrill.png
│   ├── fire
│   │   ├── 004-charmander.png
│   │   ├── 005-charmeleon.png
│   │   └── 006-charizard.png
│   ├── grass
│   │   ├── 001-bulbasaur.png
│   │   ├── 002-ivysaur.png
│   │   └── 003-venusaur.png
│   └── water
│       ├── 007-squirtle.png
│       ├── 008-wartortle.png
│       └── 009-blastoise.png
└── raw
```

Containing the main pokemon type as containing folder, and the number and the name as the image name. This step requires 2 processes. First, generate the structure of the directories using the main pokemon type. Then, download the image into each of the folders. The first process is described in the **setDirs**() function, and the latter in the **downloadImages**() function.

```python
def setDirs(pokedex):

    if not os.path.isdir('./images/'):
        os.mkdir('./images/')

    if not os.path.isdir('./images/ok/'):
        os.mkdir('./images/ok/')

    types_list = pokedex['type'].tolist()
    all_types = list(set([x.split('-')[0] for x in types_list]))

    for _type in all_types:
        directory = './images/ok/{}'.format(_type)
        if not os.path.isdir(directory):
            os.mkdir(directory.format(_type))

def downloadImages(pokedex):

    for index, row in pokedex.iterrows():

        from_location = row['img_url']

        poke_num = "{0:0=3d}".format(int(row['number']))
        poke_type = row['type'].split('-')[0]
        img_name = "{}-{}".format(poke_num, row['name'])

        to_location = "./images/ok/{}/{}.png"
        to_location = to_location.format(poke_type, img_name)

        if not os.path.exists(to_location):
            response = requests.get(from_location)
            if response.status_code == 200:
                with open(to_location, 'wb') as f:
                    f.write(response.content)
```
