import streamlit as st
import pandas as pd
from google_play_scraper import Sort, reviews
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from texts import texts
import time

# --- Page Config ---
st.set_page_config(page_title="Google Play Reviews Scraper", page_icon="📱", layout="centered")

# --- Top bar with right-aligned language selector ---
col1, col2 = st.columns([8, 2])
with col2:
    language = st.selectbox(
        "🌐",
        ["English", "Türkçe", "Deutsch"],
        index=0,
        label_visibility="collapsed"
    )

t = texts[language]

st.title(t["title"])

# --- App ID & Comment Count ---
app_id = st.text_input(t["enter_app_id"], "")
count = st.number_input(t["num_comments"], min_value=100, max_value=100000, value=5000, step=500)

# --- Session State ---
if "reviews_df" not in st.session_state:
    st.session_state.reviews_df = None
if "total_avg_time" not in st.session_state:
    st.session_state.total_avg_time = 0

# --- Fetch Comments ---
if st.button(t["fetch_comments"]):
    progress_msg = st.empty()
    progress_msg.info(t["fetching"])

    all_reviews = []
    batch_size = 200
    next_token = None
    max_retries = 3
    retries = 0

    progress_bar = st.progress(0)
    progress_text = st.empty()
    step = 0
    animation = ["⏳", "🔄", "⚙️", "💬"]

    st.session_state.total_avg_time = 0

    while len(all_reviews) < count:
        try:
            batch_start = time.time()
            batch, next_token = reviews(
                app_id,
                lang="tr" if language=="Türkçe" else "tr" if language=="English" else "tr",
                country="tr" if language=="Türkçe" else "tr" if language=="English" else "tr",
                sort=Sort.NEWEST,
                count=min(batch_size, count - len(all_reviews)),
                continuation_token=next_token
            )
            batch_time = time.time() - batch_start
        except Exception as e:
            retries += 1
            if retries > max_retries:
                st.warning(f"Fetching stopped due to repeated errors: {e}")
                break
            time.sleep(2)
            continue

        if not batch:
            st.info("No more reviews available, stopping fetch.")
            break

        all_reviews.extend(batch)
        retries = 0

        # Update average time per review
        st.session_state.total_avg_time = (
            (st.session_state.total_avg_time * (len(all_reviews) - len(batch)) + batch_time) / len(all_reviews)
        )

        # Update progress
        processed = len(all_reviews)
        percent = min((processed / count) * 100, 100)
        remaining_reviews = max(count - processed, 0)
        est_seconds_left = remaining_reviews * st.session_state.total_avg_time
        minutes_left = int(est_seconds_left // 60)
        seconds_left = int(est_seconds_left % 60)

        progress_bar.progress(int(percent))
        emoji = animation[step % len(animation)]
        progress_text.markdown(
            f"{emoji} **{t['progress']}:** %{percent:.1f}   ⏱️ {t['eta']}: {minutes_left} min {seconds_left} sec"
        )
        step += 1
        time.sleep(0.2)

        if not next_token:
            break

    all_reviews = all_reviews[:count]
    progress_bar.progress(100)
    progress_text.empty()
    progress_msg.success(t["fetch_complete"].format(count=len(all_reviews)))

    # --- DataFrame ---
    reviews_data = [{
        "User Name": r["userName"],
        "Review": r["content"],
        "Rating": r["score"],
        "Date": r["at"].strftime("%Y-%m-%d %H:%M:%S")
    } for r in all_reviews]

    df = pd.DataFrame(reviews_data)
    df.index += 1
    st.dataframe(df)
    st.session_state.reviews_df = df

    # --- Save & Download Excel ---
    excel_file = "google_play_reviews.xlsx"
    df.to_excel(excel_file, index=False)
    st.success(t["excel_saved"])
    st.download_button(
        label=t["download_excel"],
        data=open(excel_file, "rb").read(),
        file_name=excel_file,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Sentiment Analysis & Word Cloud ---
if st.session_state.reviews_df is not None:
    if st.button(t["analyze_button"]):
        progress_msg = st.empty()
        progress_msg.info(t["analyzing"])
        df = st.session_state.reviews_df.copy()

        def get_sentiment(text):
            score = TextBlob(text).sentiment.polarity
            if score > 0.1:
                if language == "English":
                    return "Positive"
                elif language == "Türkçe":
                    return "Pozitif"
                else:  # Deutsch
                    return "Positiv"
            elif score < -0.1:
                if language == "English":
                    return "Negative"
                elif language == "Türkçe":
                    return "Negatif"
                else:  # Deutsch
                    return "Negativ"
            else:
                if language == "English":
                    return "Neutral"
                elif language == "Türkçe":
                    return "Nötr"
                else:  # Deutsch
                    return "Neutral"

        df["Sentiment"] = df["Review"].apply(get_sentiment)
        st.write(t["sentiment_results"])
        st.dataframe(df[["Review", "Sentiment"]])

        # --- Prepare text for WordCloud ---
        if language == "English":
            text_positive = " ".join(df[df["Sentiment"]=="Positive"]["Review"].tolist())
            text_negative = " ".join(df[df["Sentiment"]=="Negative"]["Review"].tolist())
        elif language == "Türkçe":
            text_positive = " ".join(df[df["Sentiment"]=="Pozitif"]["Review"].tolist())
            text_negative = " ".join(df[df["Sentiment"]=="Negatif"]["Review"].tolist())
        else:  # Deutsch
            text_positive = " ".join(df[df["Sentiment"]=="Positiv"]["Review"].tolist())
            text_negative = " ".join(df[df["Sentiment"]=="Negativ"]["Review"].tolist())

        # --- WordCloud Positive ---
        if text_positive.strip():
            wc_pos = WordCloud(width=800, height=400, background_color="white").generate(text_positive)
            st.subheader(t["positive_wc"])
            fig, ax = plt.subplots(figsize=(10,5))
            ax.imshow(wc_pos, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info(t["no_positive"])

        # --- WordCloud Negative ---
        if text_negative.strip():
            wc_neg = WordCloud(width=800, height=400, background_color="white").generate(text_negative)
            st.subheader(t["negative_wc"])
            fig, ax = plt.subplots(figsize=(10,5))
            ax.imshow(wc_neg, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info(t["no_negative"])

        progress_msg.success(t["analysis_complete"])