import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

Default_person_info = '''You are Pratham Mittal, a passionate and skilled software and machine learning developer based in New Delhi. 
                        With a strong foundation in Computer Science (CGPA: 9.11), hands-on experience at DRDO as a Machine Learning Intern, 
                        and over 600 DSA problems solved, you bring robust analytical and coding capabilities to the table.'''

Default_proj_info = '''You’ve built and deployed multiple impactful projects, including:
            - An Amazon Review Sentiment Analyzer with a Streamlit UI and 93.49% accuracy,
            - A Transaction Analyzer with visual breakdowns for financial insights,
            - EventVerse, a full-stack React + Firebase event listing app,
            - Cold Mail Generator with toggling system and Geneative AI.
            '''


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://careers.nike.com/software-engineer/job/R-61132")






    use_defaults = st.toggle("Use Pratham's default info", value=True)

    # User inputs
    if use_defaults:
        person_info = Default_person_info
        project_desc = Default_proj_info
    else:
        person_info = st.text_area("Enter your personal bio:", height=150)
        project_desc = st.text_area("Enter your project description:", height=150)

        # Upload Portfolio CSV
        uploaded_file = st.file_uploader("Upload your portfolio.csv", type=["csv"])
        if uploaded_file is not None:
            with open("assets/portfolio.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Portfolio updated successfully!")






    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links, person_info, project_desc)
                st.code(email, language='markdown')
        except Exception as e:
            import traceback
            st.error(f"An Error Occurred: {e}")
            st.text(traceback.format_exc())



if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)