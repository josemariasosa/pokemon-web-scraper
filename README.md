# pokemon-web-scraper

Scrap the image and basic information of the 809 Pokemon from the https://www.pokemon.com site. This repository is only for didactic purposes.

## Resourses

Pokedex site: https://www.pokemon.com/us/pokedex/
BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

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
import re
import requests

import bs4 as bs
import pandas as pd
pd.set_option('display.max_columns', 20)

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
print(pokedex)
```


Don't forget to give access to the file using the `credentials.json` client email.

### 2. Import all the table from Google Drive using the **ConnectGoogleSheet** class.

### 3. Using the data and the urls from the table apply web scaping to get the Pokemon types.


1. From the main source, the pokedex html, extract the information of all the pokemons.
2. Save the file to a local file first, then upload the information to Google Sheets.

