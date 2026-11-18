# Olympic Data Analysis Web App

**Live dashboard:** [Open the Streamlit app](https://olympic-data-analysis-web-app-am3jfyvy4gxsad7yi4xbug.streamlit.app/)

This Streamlit application explores historical Summer Olympic data from 1896 to 2016. It provides interactive views of medal tables, participation trends, country performance and athlete demographics.

## Main features

- **Medal tally:** filter medal counts by Olympic year and country/region.
- **Overall trends:** view participating nations, events and athletes over time.
- **Country analysis:** compare a country's medal history and medal-winning sports.
- **Athlete analysis:** explore age distributions, height/weight patterns and male/female participation by edition.
- **Most successful athletes:** view medal counts overall or for a selected sport/country.

## Technology

Python, Streamlit, Pandas, NumPy, Plotly, Matplotlib and Seaborn.

## Run locally

~~~bash
git clone https://github.com/PARAG-TIWARI/olympic-data-analysis-web-app.git
cd olympic-data-analysis-web-app

python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
~~~

The application expects these files in the repository root:

- `athlete_events.csv` — athlete and event records.
- `noc_regions.csv` — NOC-to-region mapping.

The app reads the files through a cached loader, so the large athlete CSV is not reparsed on every Streamlit interaction.

## Repository structure

~~~text
olympic-data-analysis-web-app/
├── app.py                 # Streamlit dashboard
├── helper.py              # Medal, country and athlete analytics
├── preprocessor.py        # Summer Games filter and NOC mapping
├── athlete_events.csv     # Historical athlete/event data
├── noc_regions.csv        # NOC/region reference
├── requirements.txt
└── tests/                 # Helper and preprocessing unit tests
~~~

## Data source

The repository README attributes the data to Kaggle's **120 Years of Olympic History** dataset: [dataset page](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results).

The data in this repository covers Summer Olympic athlete/event records from 1896 through 2016. The application filters out Winter Games during preprocessing.

Check the dataset's current licence and terms before redistributing the CSV or using it for commercial purposes.

## Implementation notes

- Medal tallies deduplicate event/team/medal combinations to avoid counting every athlete in a team event as a separate team medal.
- Athlete participation by gender is counted once per athlete, region and Olympic year. This avoids counting an athlete only in the first edition in which they appear.
- The dataset is loaded with `st.cache_data` to reduce repeated 41 MB CSV reads during Streamlit reruns.
- The dashboard is an exploratory historical analysis tool; its counts reflect the dataset's scope and historical NOC/region mapping.

## Tests

Install the development dependencies and run:

~~~bash
pip install -r requirements-dev.txt
pytest -q
~~~

## Author

Parag Tiwari · [GitHub profile](https://github.com/PARAG-TIWARI)

**Repository:** [PARAG-TIWARI/olympic-data-analysis-web-app](https://github.com/PARAG-TIWARI/olympic-data-analysis-web-app)
