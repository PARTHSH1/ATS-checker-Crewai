import json 
from typing import List,Dict
from pydantic import BaseModel,Field
from crewai import LLM
from crewai.flow.flow import Flow,start,listen
import os
import pdfplumber
import docx
from bs4 import BeautifulSoup
import requests
from crews.crew import ResumeCrew

import re

## adding the agents
class State(BaseModel):
    technical_skills : float = Field(...,description="Technical skills percentage of the person ")
    soft_skills : float = Field(...,description="Soft skills percentage of the person")
    tools : float = Field(...,description="Tools percentage of the person")
class Matching_algorith(BaseModel):
    similarity_score : float = Field(...,description="similarity score between the two sentences")
    matched_keywords : List[str] = Field(...,description="matched keywords between the two sentences")
    missing_keywords : List[str] = Field(...,description="missing keywords between the two sentences")
    extra_keywords_in_resume : List[str] = Field(...,description="extra keywords to add in resume to improve score")
    catergory_scores : List[State] = Field(...,description="category scores of the resume")
class MultidimensionalScore(BaseModel):
    Content_match : str = Field(...,description="exactly how much the resume matches the job description")
    Format_compatibility : str = Field(...,description="exactly how much the resume format is compatible with the job description")
    Section_specific_scores : str = Field(...,description="exactly how much the resume matches the job description in each section")
    Combined_score : str =Field(description="Overall score of the resume")
    Recommendation_engine : str = Field(description="Recommended keywords or skills required to make it more impressive")
class ATS(BaseModel):
    content: str = Field("",description="content of the resume")
    keywordsfromResume: str = Field("",description="keywords of the job description")
    keywordsFromJob : str = Field("",description="keywords of the job description")
    matching : Matching_algorith = None
    multidimentionalscore : MultidimensionalScore = None
class ATSmaking(Flow[ATS]):
    """Flow to make the ATS matching"""
    @start()
    def get_user_input(self):
        """get file path from the user"""
        file_path=input("Enter the file path ")
        print("\n ====Extracting content from the resume====")
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.pdf':
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text=page.extract_text()
                        if page_text:
                            cleaned_text=re.sub(r'[\n|]',' ',page_text)
                            self.ATS = ATS(content="")
                            self.ATS.content+=cleaned_text
            except Exception as e:
                print(f"Error parsing PDF:{str(e)}")
        if file_extension == '.docx':
            try:
                doc = docx.Document(file_path)
                for paragraph in doc.paragraphs:
                    self.ATS = ATS(content="")
                    self.ATS.content+= paragraph.text 
            except Exception as e:
                print(f"Error parsing DOCX: {str(e)}")
        if file_extension == '.html':
            try:
                with open(file_path, 'r',encoding="utf-8") as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    text = soup.get_text()
                    self.ATS.content+=text
            except Exception as e:
                print(f"Error parsing HTML: {str(e)}")
        return self.ATS.content
    @listen(get_user_input)
    def keyword_finding(self):
        llm = LLM(model="groq/llama-3.3-70b-versatile",api_key=os.environ.get("GROQ_API_KEY"))
        messages = [
                {"role": "system","content":"You are a heelpful assistant designed to give keywords from the given resume content"},
                {"role":"user","content":f"""
                Give all the keywords that are given in the resume content  {self.ATS.content}
                1. Keyword should be relevent 
                2. No personal info should be taken 
                3. Should only give software used , framework used in project
                4.Give keywords like this only [Python,Flask,GO,Streamlit]
                """}]
        response = llm.call(messages=messages)
        self.ATS.keywordsfromResume = response
        return self.ATS.keywordsfromResume
    @listen(keyword_finding)
    def Keyword_job(self):
        link = input ("Enter the job link ")
        response=requests.get(link)
        response.raise_for_status
        soup=BeautifulSoup(response.text,"html.parser")
        keywordsjob= soup.get_text()
        llm = LLM(model="groq/llama-3.3-70b-versatile")
        messages = [
                {"role": "system","content":"You are a heelpful assistant designed to give keywords from the job description ans post."},
                {"role":"user","content":f"""
                Give all the keywords that are given in the job description content  {keywordsjob}
                1. Keyword should be relevent 
                2. No company description should be taken 
                3. Should only give software used , framework described in the post 
                4.Give keywords like this only [Python,Flask,GO,Streamlit]
                """}]
        response = llm.call(messages=messages)
        print(response)
        keywords = response
        self.ATS.keywordsFromJob = keywords
        return self.ATS.keywordsFromJob
    @listen(Keyword_job)
    def Matching_both(self):
        """Matching algorithm and scoring the resume in different perspective"""
        llm=LLM(model="groq/llama-3.3-70b-versatile",response_format=Matching_algorith)
        messages = [
            {"role": "system","content":"You are a heelpful assistant designed to give similarity score ,matched_keywords,missing_keywords,extra_keywords_in_resume,catergory_scores containing techinical skill ,soft_skills,tools ."},
            {"role":"user","content":f"""
            Give score for every expect of the resume content  {self.ATS.keywordsfromResume} and job description content {self.ATS.keywordsFromJob}


            """}
        
        ]
        response=llm.call(messages=messages)
        print(response)
        self.ATS.matching = response
    @listen(Matching_both)
    def Multidimensional_matching(self):
        """Multidimensional matching algorithm and scoring the resume in different perspective"""
        result=ResumeCrew().crew().kickoff(
            inputs={
                "Content":self.ATS.content,
                "keywordsfromResume":self.ATS.keywordsfromResume,
                "keywordsFromJob":self.ATS.keywordsFromJob
            }
        )
        self.ATS.multidimentionalscore = result.raw
        print("\n Completed the analysis of the resume throughly")
        return self.ATS.multidimentionalscore
def kickoff():
    ATSmaking().kickoff()
    print("\n flow complete ")
if __name__ == "__main__":
    kickoff()