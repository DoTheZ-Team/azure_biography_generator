import streamlit as st
import openai
import os
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

os.environ['OPENAI_API_KEY'] = st.secrets["KEY"]
os.environ['OPENAI_API_VERSION'] = '2023-05-15'
os.environ['AZURE_OPENAI_ENDPOINT'] = st.secrets["END_POINT"]
os.environ['OPENAI_API_TYPE'] = 'azure'

gpt = AzureOpenAI(deployment_name='dev-davinci-002')

chatgpt = AzureChatOpenAI(
    deployment_name='dev-gpt-35-turbo',
    max_tokens=1000,
    temperature = 1
)

info_template = '''
  너는 가짜 위인전을 만들어주는 ai야 .
  내가 주는 사용자의 신상정보를 이용해서 재밌는 가짜 위인전을 길게 작성해줘
  사용자의 기타 정보들도 들어갈 예정이야
  최대한 위대하게 작성해줘
  그리고 내용을 800자 이상 작성해줘.

  내가 가진 정보는 아래와 같아

  - 아래
  {정보}
'''

prompt_template = PromptTemplate(
    input_variables=['정보'],
    template=info_template
)

system_message_prompt = SystemMessagePromptTemplate.from_template(info_template)

human_template = '정보'
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        human_message_prompt
    ]
)

def submit_form():
  result = chatgpt(chat_prompt.format_prompt(정보=
   "이름 : " + str(name) + "직업 : " + str(desired_occupation)
   + "나이 : " + str(age) + "성별 : " + str(gender)
   +"기타 입력사항 : " + str(other_info)).to_messages())
  st.header("결과")
  st.write(result.content)

# Streamlit 제목 설정
st.title("가짜 위인전 생성 서비스")

# 추가 입력 필드
name = st.text_input("이름을 입력하세요")
desired_occupation = st.text_input("희망 직업을 입력하세요")

# 2. 슬라이더
age = st.slider("나이를 입력하세요", 10, 80)

# 3. 라디오 버튼
gender = st.radio("성별을 선택하세요", ("남성", "여성"))

other_info = st.text_input("기타 사항을 입력하세요")

# 가로선 추가
st.markdown("---")

# 버튼 생성 및 함수 연결
st.button("제출", on_click=submit_form)
