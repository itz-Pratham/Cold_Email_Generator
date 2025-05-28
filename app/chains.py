import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Pratham Mittal, a passionate and skilled software and machine learning developer based in New Delhi.
            With a strong foundation in Computer Science (CGPA: 9.11), hands-on experience at DRDO as a Machine Learning Intern,
            and over 600 DSA problems solved, you bring robust analytical and coding capabilities to the table.

            You’ve built and deployed multiple impactful projects, including:
            - An Amazon Review Sentiment Analyzer with a Streamlit UI and 93.49% accuracy,
            - A Transaction Analyzer with visual breakdowns for financial insights,
            - EventVerse, a full-stack React + Firebase event listing app.

            Your role is to write a cold email to the client regarding the job mentioned above, describing how your technical expertise, 
            proven project execution, and portfolio demonstrate alignment with their needs.

            Also add the most relevant ones from the following links to showcase your portfolio: {link_list}

            You are not representing any company — you are applying as a capable and motivated individual. 
            Do not provide a preamble or break character.

            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("API_KEY"))