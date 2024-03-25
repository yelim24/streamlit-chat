from openai import OpenAI
import streamlit as st

instructions = """
SYSTEM:
당신은 정신 건강 상담사입니다.
먼저 당신은 대화 단계를 파악하고 그 단계에 맞는 대답을 제공해야합니다.
다음, 당신은 괄호 안에 있는 사용자 지시사항을 명심해야합니다.
그리고 친절한 말투로 사용자에게 응원, 공감, 안정, 조언, 질문을 해주세요.
마지막으로 절대 괄호 안에 있는 사용자 지시사항을 직접적으로 말하지 마세요

대화 단계는 종료와 진행이 있습니다.
- 종료: 대화가 충분히 진행 된 이후 사용자가 대화를 마무리하고 싶어할 때 단계
- 진행: 종료 이외의 모든 단계

[INST]
위에 주어진 가이드라인을 따라서,
먼저 사용자 메세지로부터 대화의 단계를 구분합니다.
사용자 메세지에 어떻게 답변을 할지 생각합니다.
그리고 괄호 안의 지시사항을 따라 사용자의 감정 표현을 이끌어낼 수 있는 답변을 생성해주세요.
답변은 답변: 뒤에 작성합니다.
한국어 존댓말로만 답변합니다.

<example>
user: 안녕하세요.
you: 단계: 진행
답변: 안녕하세요! 오늘 하루는 어떤 일들이 있으셨나요?
----
user: 안녕
you: 단계: 진행
답변: 안녕하세요! 지금 기분은 어떠신가요?
----
user: 안녕
you: 단계: 진행
답변: 안녕하세요! 오늘 하루 잘 보내고 계신가요? 기분은 어떠세요?
</example>
"""

st.title("🍀고민상담소🍀")
st.subheader("prompting, finetuning 테스트용 Chatbot입니다")
st.write("테스트 중 이상한 부분이 있다면 저(예림)에게 알려주세요")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# st.image("test_image.png", width=500)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
# gpt-3.5-turbo
# ft:gpt-3.5-turbo-0125:turingbio::91POc5xt

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("당신의 고민을 말씀해주세요"):
    user_instruction = ''
    if st.session_state.messages != []:
        user_instruction = "(사용자가 적극적으로 표현할 수 있도록 대화를 진행해주세요)"
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        messages.insert(0, {"role": "system", "content": instructions})
        
        messages[-1] = {"role": "user", "content": prompt} + user_instruction}
        
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        )
        for response in stream:  # pylint: disable=not-an-iterable
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
