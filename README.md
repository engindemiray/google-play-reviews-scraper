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

- Fetch reviews from any Google Play app (up to 100,000 reviews)
- Sentiment analysis (Positive, Negative, Neutral)
- Generate Word Clouds for positive and negative reviews
- Export reviews to Excel
- Multi-language support (English, Turkish, German)

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
## Usage

Run the Streamlit app:
``` bash
$ streamlit run comment_scraper_web.py
```

You may visit the application on browser with the URL: http://localhost:8501

## License

This project is licensed under the MIT License.
