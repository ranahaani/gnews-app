import streamlit as st
import pandas as pd
import base64

from gnews import GNews

def main():

    gn = GNews()

    st.markdown(
        """<h1 style='text-align:center;color:#8000C4;font-family: montserrat;font-size:50px;margin-top:-70px;'>GNews<span style='text-align:center;color:red;'>.</span></h1><h3 style='text-align:center;margin-top:-25px;'>Created by: <u><a href='https://in.linkedin.com/in/ranahaani' target="_blank">Muhammad Abdullah</u></a></h3>""",
        unsafe_allow_html=True)
    search_term = st.sidebar.text_input('Search Term:', 'Google')

    languages = tuple([language.title() for language in gn.languages[0]])
    countries = tuple(country.title() for country in gn.countries[0])
    gn.country = st.sidebar.selectbox(label='Country', options=countries)
    gn.language = st.sidebar.selectbox(label='Language', options=languages).lower()

    search = gn.get_news(search_term)
    data = pd.DataFrame.from_dict(search)
    count = st.sidebar.number_input("No. of Articles to display:", min_value=1, max_value=100, step=1, value=5)
    st.markdown(
        """<h1 style='font-family: montserrat;text-align:center;color:#8000C4;'>{} <span style='text-align:center;color:red;'>News Articles</span></h1>""".format(
            search_term), unsafe_allow_html=True)

    csv = data[['title', 'description', 'published date', 'url', 'publisher']].to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()

    for row in range(0, count):
        try:
            url = data['url'].iloc[row]
            with st.beta_expander(f"{row + 1}. {data['title'].iloc[row]}"):

                article = gn.get_full_article(url)
                if article:
                    st.image(article.top_image)
                    st.title(article.title)
                    article.text
                    st.markdown(
                        """<p style="display: inline;"> This article is published on </p><a style="color:red;font-weight:bold;font-family: montserrat;" href={} target=_blank>{}</a>. &nbsp;&nbsp;&nbsp;&nbsp; <a 
                        style="color:#8000C4;font-weight:bold;font-family: montserrat;" href={} target=_blank>{}</a> """
                            .format(
                            data['publisher'].iloc[row]['url'], data['publisher'].iloc[row]['title'], data['url'].iloc[row],
                            "Source of article"),
                        unsafe_allow_html=True)
        except Exception as error:
            st.error(error.args[0])

    st.sidebar.markdown(
        f'<a href="data:file/csv;base64,{b64}" download="{search_term} dataset.csv">Download {search_term} dataset</a>',
        unsafe_allow_html=True)

if __name__ == '__main__':
    main()