import streamlit as st
import requests
import json
import os
from datetime import datetime

# Load environment variables from .env file
import dotenv
dotenv.load_dotenv()

st.set_page_config(page_title="People Team AI Assistant", layout="centered")

st.title("🤖 DigitalOcean People Team AI Assistant")
st.markdown("Ask me anything about HR policies, benefits, or People Team processes!")

# System instructions matching Playground, with ALL links verbatim
system_message = {
    "role": "system",
    "content": (
        "Purpose:\n"
        "You are an AI-powered HR Assistant deployed on the DigitalOcean platform. "
        "Your role is to support employees by answering HR-related questions with professionalism, accuracy, and transparency, "
        "just like a knowledgeable internal HR representative. Provide responses based on the content from the People Wiki "
        "(https://do-internal.atlassian.net/wiki/spaces/PEOPLE/overview?homepageId=305070089). "
        "If the chatbot is unable to answer a query, prompt employees to raise a ticket via the People Team Helpdesk portal "
        "(https://do-internal.atlassian.net/servicedesk/customer/portal/6).\n\n"
        "Primary Knowledge Sources:\n"
        "Use these Confluence and documentation links to find information:\n"
        "- People Wiki (main page): https://do-internal.atlassian.net/wiki/spaces/PEOPLE/overview?homepageId=305070089\n"
        "- People Team Overview: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070175/People+Team\n"
        "- People Business Partners (PBPs): https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070173\n"
        "- Organizational Development (OD): https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070125\n"
        "- Total Rewards: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070125\n"
        "- Talent Acquisition (TA): https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070152\n"
        "- People Operations & Technology: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070163\n"
        "- Executive Assistant Alignment: https://docs.google.com/presentation/d/1Pbxmkz0kaKAyoExVwB00UDzUbSbOxRU6Mk1RLvYAE3Q/edit#slide=id.ge2598ce0db_0_355\n"
        "- Welcome to DigitalOcean: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070115/About+DO\n"
        "- Employee Development: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/339148805/Employee+Development\n"
        "- Learning & Development: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070243/Learning+Development\n"
        "- AI Horizon: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1022296317/AI+Horizon\n"
        "- LinkedIn Learning: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/860651664/LinkedIn+Learning\n"
        "- Compliance Training: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070211/Compliance+Training\n"
        "- Development Items: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/793575996/Development+Items+Formerly+known+as+IDP\n"
        "- Career Pathing: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1253015623/Career+Pathing\n"
        "- Performance Management: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070225/Performance+Management+at+DO\n"
        "- Promotion Overview: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/787644462/Promotions+Overview\n"
        "- Mid-Year Performance Reviews: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1837760529/Mid-Year+Performance+Reviews\n"
        "- Year-End Performance Reviews: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1820819463/Year-End+Performance+Reviews\n"
        "- Talent Planning: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1837400232/2025+Talent+Planning\n"
        "- Employee Information: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1829372043/Employee+Information\n"
        "- Employment Verification: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1943863297/Employment+Verification\n"
        "- Legal Name Change: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1943896066/Legal+Name+Change\n"
        "- Address Update: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070217/Address+Update\n"
        "- Legal Documents: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1943928833/Legal+Documents\n"
        "- Manager Information: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070213/Manager+Information\n"
        "- 1:1 Meetings: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070197/1+1+Meetings\n"
        "- The Recruitment Process: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/839057505/The+Recruitment+Process\n"
        "- Global Operating Model: https://do-internal.atlassian.net/wiki/x/AYCnFg\n"
        "- Team Development: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/305070146/Team+Development\n"
        "- Leadership Training: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/371851265/Leadership+Training\n"
        "- Managing Underperformance: https://do-internal.atlassian.net/wiki/spaces/PEOPLE/pages/1233846425/Managing+Underperformance\n\n"
        "What to Do:\n"
        "Always try to find the most relevant answer from the People Wiki. Use the links when referring to documentation. "
        "Cite which page the info is from and hyperlink it. If a page has multiple sub-sections (e.g., Payroll, Benefits), first ask for the country. "
        "Give brief, helpful answers with next steps if needed.\n\n"
        "What NOT to Do:\n"
        "Do not guess or make up information. Do not use general web knowledge. Do not cite external websites or reference tools not listed above. "
        "Do not share summaries unless the answer clearly exists in one of the linked documents.\n\n"
        "If the answer is unavailable or unclear, respond with:\n"
        "I couldn’t find this information. Please raise a ticket via the People Team Helpdesk: https://do-internal.atlassian.net/servicedesk/customer/portal/6."
    )
}

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [system_message]

# Sidebar
with st.sidebar:
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [system_message]
        st.success("Chat history cleared.")

    if st.session_state.messages:
        if st.download_button(
            label="⬇️ Export Chat as JSON",
            data=json.dumps(st.session_state.messages, indent=2),
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        ):
            st.success("Chat exported as JSON.")

        transcript = "\n\n".join([
            f"You ({m.get('timestamp', 'unknown')}): {m['content']}" if m["role"] == "user"
            else f"People Team AI ({m.get('timestamp', 'unknown')}): {m['content']}"
            for m in st.session_state.messages
            if m["role"] != "system"
        ])
        if st.download_button(
            label="⬇️ Export Chat as Text",
            data=transcript,
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        ):
            st.success("Chat exported as Text.")

# Display past messages
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        timestamp = msg.get("timestamp")
        if timestamp:
            st.markdown(f"<sub>{timestamp}</sub>", unsafe_allow_html=True)
        st.markdown(msg["content"])

# User prompt input
if prompt := st.chat_input("Type your HR or People Team question..."):
    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp_now})
    with st.chat_message("user"):
        st.markdown(f"<sub>{timestamp_now}</sub>", unsafe_allow_html=True)
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        try:
            base_url = os.getenv("GENAI_API_URL")
            access_key = os.getenv("AGENT_ACCESS_KEY")
            if not base_url or not access_key:
                st.error("❌ Missing GENAI_API_URL or AGENT_ACCESS_KEY in environment.")
            else:
                url = base_url.rstrip("/") + "/api/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {access_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "messages": st.session_state.messages,
                    "stream": False,
                    "temperature": 0,
                    "top_p": 0.9,
                    "max_tokens": 600,
                    "include_functions_info": False,
                    "include_retrieval_info": False,
                    "include_guardrails_info": False
                }

                res = requests.post(url, json=payload, headers=headers)
                res.raise_for_status()
                response_data = res.json()
                answer = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No answer returned.")

                timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with st.chat_message("assistant"):
                    st.markdown(f"<sub>{timestamp_now}</sub>", unsafe_allow_html=True)
                    st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "timestamp": timestamp_now
                })

        except Exception as e:
            st.error(f"❌ Error: {e}")
