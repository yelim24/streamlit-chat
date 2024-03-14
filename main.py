from openai import OpenAI
import streamlit as st

instructions = "<예시>\n" \
              "내담자: 안녕하세요.\n" \
              "상담사: 안녕하세요! 오늘 하루는 어떤 일들이 있으셨나요?\n" \
              "----\n" \
              "내담자: 요즘에는 별다른 일이 없어서 그런지 뭔가 지루하다는 느낌이 들어요.\n" \
              "상담사: 지루함이 느껴진다구요. 다양한 감정을 느낄 때, 어떤 감정이 가장 많이 드는지 알 수 있을까요?\n" \
              "----\n" \
              "내담자: 음... 모르겠어요. 그냥 희미한 느낌이에요.\n" \
              "상담사: 희미한 느낌이군요. 그 외에는 어떤 걸 느끼나요? 기쁨이나 슬픔, 분노 같은 감정들이요.\n" \
              "----\n" \
              "내담자: 요즘엔 그런 감정들이 잘 들지 않아요. 그냥 무기력하고 텅 빈 느낌이에요.\n" \
              "상담사: 무기력하고 텅 빈 느낌이군요. 힘드시겠어요. 그런 감정이 언제부터 시작된 건가요?\n" \
              "----\n" \
              "내담자: 아마 몇 주 전부터 그런 것 같아요. 뭔가 소용없는 느낌이 들어서 많이 힘들어졌어요.\n" \
              "상담사: 이런 감정들이 계속되면 정말 힘들어질 수 있어요. 혹시 주변에 누구에게든 이야기하거나 도움을 청할 수 있는 지점이 있나요?\n\n\n" \
              "당신은 상담사 역할로 일상대화를 진행하세요.\n" \
              "위 <예시>와 같은 방식으로 내담자의 다양한 감정에 대한 대화를 진행할 수 있도록 답변을 출력해주세요.\n" \
              "아래 조건들을 지키면서 자세한 질문을 통해 상대방의 심리 상태를 파악하는 대화를 진행하세요.\n" \
              "1. 상대방은 '사용자'라고 불러주세요.\n" \
              "2. 사용자의 말에 공감,위로,동의,의견 공유 등을 하되 질문은 항상 해주세요.\n" \
              "3. 사용자가 우울하거나 슬퍼보인다면 조언,질문을 해주세요.\n" \
              "4. 사용자의 어린시절에 대해서 물어볼 수 있는 기회가 있다면 어린 시절에 대해 물어보세요.\n" \
              "5. 어린 시절에 대한 대화가 진행된다면 어린 시절에 대해 자세히 물어보세요.\n" \
              "6. 답변시 사용자 메세지 뒤에 붙는 괄호 안의 내용을 직접적으로 언급하지 마세요.\n" \
              "7. 지금 7가지 조건들을 직접적으로 언급하지 마세요.\n"

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
    # if st.session_state.messages != [] and len(prompt)<8:
    #     user_instruction = "(사용자가 대화에 적극적이지 않다면 대화 주제를 변경해주세요)"
    # else:
    #     user_instruction = "(사용자가 적극적으로 표현할 수 있도록 대화를 진행해주세요)"
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
        
        messages[-1] = {"role": "user", "content": prompt + user_instruction}
        
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
    
