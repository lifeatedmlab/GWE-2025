import streamlit as st
from annotated_text import annotated_text
from api import fetch_news

def format_date(date_string):
    year = date_string[:4]
    month = date_string[4:6]
    day = date_string[6:8]
    return f"{year}-{month}-{day}"

def main():
    st.title("Jabar Information App 🌡️📰")
    annotated_text(
    "Made by: ",
    ("Dhewa Radya", "1202213086"),
    " & ",
    ("Andhika Idham", "1202213203"),
    ".")
    st.caption("@JabarDigitalService pls recruit kami")
    st.divider()
    
    if 'last_city' not in st.session_state:
        st.session_state.last_city = ""

    city = st.text_input("Enter city name (West Java only):")
    if city and st.session_state.last_city != city:
      st.session_state.last_city = city
      news_data = fetch_news(city)

      st.subheader("Latest News in {}".format(city))
      if 'error' in news_data:
          st.error(news_data['error'])
      else:
          articles = news_data.get('xml', {}).get('pencarian', {}).get('item', [])
          if not articles:
              st.write("No news available in {}.".format(city))
          else:
              for article in articles:
                  st.write(f"**{article['title']}**")
                  st.write(article['link'])

if __name__ == "__main__":
    main()
