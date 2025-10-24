![Screenshot 2025-10-22 at 19 43 21](https://github.com/user-attachments/assets/206659eb-6332-4489-9a26-7311f660c204)

## Tech Stack

- Python
- Streamlit
- Pandas
- Google Play Scraper
- TextBlob
- WordCloud
- Matplotlib

## Features

- 📥 Fetch reviews from any Google Play app (up to 100,000 reviews)
- 🧠 Sentiment analysis (Positive, Negative, Neutral)
- ☁️ Generate Word Clouds for positive and negative reviews
- 📊 Export reviews to Excel
- 🌐 Multi-language support (English, Turkish, German)

## Installation

Clone the repository:
``` bash
$ git clone https://github.com/engindemiray/google-play-reviews-scraper.git
cd google-play-reviews-scraper
```

Create a virtual environment (optional but recommended):
``` bash
$ python3 -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

Install required packages:
``` bash
$ pip3 install -r requirements.txt
```

Run the Streamlit app:
``` bash
$ streamlit run comment_scraper_web.py
```

You may visit the application on browser with the URL: http://localhost:8501

## Architecture

```
        User Browser (Client)
                 │
                 │ 1. Start Streamlit App
                 ▼
┌──────────────────────────────────────────────┐
│       Streamlit UI (comment_scraper_web.py)  │
│ ┌──────────────────────────────────────────┐ │
│ │ User Input: App ID, Limit, Language      │ │
│ └─────────────────┬────────────────────────┘ │
└───────────────────┬──────────────────────────┘
                    │ 2. Scrape Request
                    ▼
┌──────────────────────────────────────────────┐
│        Google Play Scraper Library           │
│ ┌──────────────────────────────────────────┐ │
│ │ Fetch Raw Review Data (up to 100k)       │ │
│ └─────────────────┬────────────────────────┘ │
└───────────────────┬──────────────────────────┘
                    │ 3. Raw Data Output
                    ▼
┌──────────────────────────────────────────────┐
│        Pandas Processing Engine              │
│ ┌──────────────────────────────────────────┐ │
│ │ Data Loading (DataFrame Creation)        │ │
│ │ Pre-Processing (NaN/Null/Basic Cleaning) │ │
│ └─────────────────┬────────────────────────┘ │
└───────────────────┬──────────────────────────┘
                    │ 4. Clean Data Input
                    ▼
┌──────────────────────────────────────────────┐
│        TextBlob Sentiment Analysis           │
│ ┌──────────────────────────────────────────┐ │
│ │ Calculate Polarity [-1.0, +1.0]          │ │
│ │ Calculate Subjectivity [0.0, 1.0]        │ │
│ └─────────────────┬────────────────────────┘ │
└───────────────────┬──────────────────────────┘
                    │ 5. Enriched DataFrame
                    ▼
┌──────────────────────────────────────────────┐
│        Streamlit Visualization Layer         │
│ ┌──────────────────────────────────────────┐ │
│ │ Classification Logic (Polarity Threshold)│ │
│ │                                          │ │
│ │ Tools:                                   │ │
│ │ - WordCloud (with Stop Words Filter)     │ │
│ │ - Matplotlib/Plotly (Distribution Charts)│ │
│ │ - Export to Excel (.xlsx)                │ │
│ └──────────────────────────────────────────┘ │
└───────────────────┬──────────────────────────┘
                    │ 6. Final Report/UI Output
                    ▼
           User Browser (Client)
```

## License

This project is licensed under the MIT License.
