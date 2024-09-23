import streamlit as st
from gtts import gTTS
import os
import json
import time
from datetime import datetime, timedelta
import base64
from mutagen.mp3 import MP3
import tempfile
import pandas as pd
from streamlit_mic_recorder import speech_to_text
from streamlit_option_menu import option_menu

class Chatbot:
    def __init__(self):
        self.responses = self.load_responses()
        self.person_data = self.load_person_data()
        self.history = self.load_history()
        self.stage = 1

    def load_responses(self):
        try:
            if os.path.exists("responses.json"):
                with open("responses.json", "r", encoding="utf-8") as file:
                    responses = json.load(file)
                    return responses
            else:
                st.write("responses.json not found, loading default responses")
                return {
                    "สวัสดี": "สวัสดีค่ะ! มีอะไรให้ช่วยไหม?",
                    "คุณชื่ออะไร": "ฉันคือ Chatbot ค่ะ",
                    "ขอบคุณ": "แล้วพบกันใหม่ค่ะ"
                }
        except Exception as e:
            st.write(f"Error loading responses.json: {e}")
            return {}

    def save_responses(self):
        try:
            with open("responses.json", "w", encoding="utf-8") as file:
                json.dump(self.responses, file, ensure_ascii=False, indent=4)
        except Exception as e:
            st.write(f"Error saving responses.json: {e}")

    def load_person_data(self):
        try:
            if os.path.exists("data_person.json"):
                with open("data_person.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    return data
            else:
                return []
        except Exception as e:
            st.write(f"Error loading history.json: {e}")
            return {}

    def save_person_data(self):
        with open("data_person.json", "w", encoding="utf-8") as file:
            json.dump(self.person_data, file, ensure_ascii=False, indent=4)

    def load_history(self):
        try:
            if os.path.exists("history.json"):
                with open("history.json", "r", encoding="utf-8") as file:
                    history = json.load(file)
                    return history
            else:
                return []
        except Exception as e:
            st.write(f"Error loading history.json: {e}")
            return []

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as file:
            json.dump(self.history, file, ensure_ascii=False, indent=4)
    
    def show_json(self, json_data, title):
        st.write(f"### {title}")
        st.json(json_data)

    def convert_list_to_string(self, value):
        if isinstance(value, list):
            return ', '.join(map(str, value)) 
        return value

    def show_history_json_as_table(self, json_data, title):
        st.write(f"### {title}")
        df = pd.DataFrame(json_data)
        df.index += 1
        df = df.rename(columns={'timestamp': 'Timestamp', 'bot_input': 'Bot Input', 'user_input': 'User Input'})
        df['Bot Input'] = df['Bot Input'].apply(self.convert_list_to_string)
        st.dataframe(df)

    def add_to_history(self, user_input, bot_input):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history.append({
            "timestamp": timestamp,
            "user_input": user_input,
            "bot_input": bot_input
        })
        self.save_history()

    def add_to_history_bot_fisrt(self, bot_input, user_input):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history.append({
            "timestamp": timestamp,
            "bot_input": bot_input,
            "user_input": user_input
        })
        self.save_history()

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang='th')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                tts.save(temp_audio.name)
                
                audio = MP3(temp_audio.name)
                audio_length = audio.info.length
            
                with open(temp_audio.name, "rb") as f:
                    mp3_data = f.read()

            b64_encoded_audio = base64.b64encode(mp3_data).decode("utf-8")
            
            if self.stage == 1:
                audio_html = f"""
                <audio id="chatbot-audio" autoplay="true" style="display:none;">
                    <source src="data:audio/mp3;base64,{b64_encoded_audio}" type="audio/mp3">
                </audio>
                """
            elif self.stage == 2:
                audio_html = f"""
                <audio id="chatbot-audio1" autoplay="true" style="display:none;">
                    <source src="data:audio/mp3;base64,{b64_encoded_audio}" type="audio/mp3">
                </audio>
                """
            elif self.stage == 3:
                audio_html = f"""
                <audio id="chatbot-audio2" autoplay="true" style="display:none;">
                    <source src="data:audio/mp3;base64,{b64_encoded_audio}" type="audio/mp3">
                </audio>
                """
            elif self.stage == 4:
                audio_html = f"""
                <audio id="chatbot-audio3" autoplay="true" style="display:none;">
                    <source src="data:audio/mp3;base64,{b64_encoded_audio}" type="audio/mp3">
                </audio>
                """

            elif self.stage == 5:
                audio_html = f"""
                <audio id="chatbot-audio4" autoplay="true" style="display:none;">
                    <source src="data:audio/mp3;base64,{b64_encoded_audio}" type="audio/mp3">
                </audio>
                """

            return audio_html, audio_length
        
        except Exception as e:
            st.write(f"Error in speak function: {e}")
            return ""

    def get_thai_date(self, offset):
        target_date = datetime.now() + timedelta(days=offset)
        months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 
                  'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
        thai_year = target_date.year + 543
        return f"วันที่ {target_date.day} {months[target_date.month - 1]} {thai_year}"

    def check_birthday(self):
        if self.person_data.get('birthday', 'ไม่ทราบ'):
            months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 
                      'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
            
            today = f"{datetime.now().day} {months[datetime.now().month - 1]}"
            birthday = " ".join(self.person_data['birthday'].split()[:2])

            if today == birthday:
                self.add_to_history_bot_fisrt(f"สุขสันต์วันเกิดค่ะ คุณ{self.person_data['nickname']} ขอให้วันนี้เป็นวันที่ดีสำหรับคุณค่ะ!", '-')
                bot = self.update_chat_history("", f"สุขสันต์วันเกิดค่ะ คุณ{self.person_data['nickname']} ขอให้วันนี้เป็นวันที่ดีสำหรับคุณค่ะ!")
                self.display_chat()
                time.sleep(bot)
                return True
        
        return False

    def get_time(self):
        #now = datetime.now() + timedelta(hours=7) # for build
        now = datetime.now()
        hours = now.strftime('%H นาฬิกา')
        minutes = now.strftime('%M')
        
        if minutes == "00":
            return f"ตอนนี้เวลา {hours}ตรง ค่ะ"
        else:
            return f"ตอนนี้เวลา {hours} {minutes} นาที ค่ะ"

    def process_input(self, user_input):
        user_input = user_input.strip()
        if user_input.endswith("ครับ"):
            return user_input[:-4].strip()
        elif user_input.endswith("คะ"):
            return user_input[:-2].strip()
        elif user_input.endswith("ค่ะ"):
            return user_input[:-3].strip()
        return user_input

    def chatbot_response(self, user_input):
        grouped_responses = {
            "สวัสดี": ["สวัสดี", "สวัสดีค่ะ", "หวัดดี", "ดี"],
            "คุณชื่ออะไร": ["คุณชื่ออะไร", "บอกชื่อหน่อย", "ชื่อของคุณ"],
            "คุณเกิดที่ไหน" : ["คุณเกิดที่ไหน"],
            "สองวันก่อนหน้าวันอะไร" : ["2 วันก่อนหน้าเป็น", "2 วันก่อนหน้าวัน"],
            "สองวันข้างหน้าหน้าวันอะไร" : ["2 วันข้างหน้าเป็น", "2 วันข้างหน้าวัน"],
            "ตอนนี้เวลา": ["ตอนนี้เวลา", "บอกเวลา", "เวลาเท่าไหร่", "ตอนนี้เวลากี่โมง", "เวลาเท่าไร", "เวลา", "ตอนนี้กี่โมง", "วันนี้กี่โมง"],
            "ฉันชื่ออะไร": ["ผมชื่ออะไร", "ฉันชื่ออะไร", "บอกชื่อผม", "บอกชื่อฉัน", "เราชื่ออะไรนะ"],
            "ฉันชื่อเล่นอะไร" : ["ผมชื่อเล่นอะไร", "ฉันชื่อเล่นอะไร", "บอกชื่อเล่นผม", "บอกชื่อเล่นฉัน", "ผมชื่อเล่นว่า", "ฉันชื่อเล่นว่า", "ชื่อเล่นของฉัน", "ชื่อเล่นของผม", "ชื่อเล่นฉัน", "ชื่อเล่นผม"],
            "ฉันเกิดวันไหน" : ["ผมเกิดวันไหน", "ฉันเกิดวันไหน", "บอกวันเกิดผม", "บอกวันเกิดฉัน", "ผมเกิดวันที่", "ฉันเกิดวันที่", "วันไหนฉันเกิด", "วันไหนผมเกิด", "ฉันเกิดตอนไหน", "ผมเกิดตอนไหน", "ฉันเกิดวันอะไร"],
            "วันนี้วันอะไร" : ["วันนี้วันที่"]
        }

        additional_responses = {
            "สวัสดี": "สวัสดีค่ะ! มีอะไรให้ช่วยไหม?",
            "คุณชื่ออะไร": "ฉันคือ Chatbot ค่ะ",
            "คุณเกิดที่ไหน" : "ฉันไม่รู้ว่าตัวเองเกิดที่ไหนคะ",
            "สองวันก่อนหน้าวันอะไร": f"สองวันก่อนหน้าเป็น {self.get_thai_date(-2)} ค่ะ",
            "เมื่อวานวันอะไร": f"เมื่อวาน {self.get_thai_date(-1)} ค่ะ",
            "วันนี้วันอะไร": f"วันนี้ {self.get_thai_date(0)} ค่ะ",
            "พรุ่งนี้วันอะไร": f"พรุ่งนี้ {self.get_thai_date(1)} ค่ะ",
            "สองวันข้างหน้าหน้าวันอะไร": f"สองวันข้างหน้าเป็น {self.get_thai_date(2)} ค่ะ",
            "ตอนนี้เวลา": self.get_time(),
            "ฉันชื่ออะไร" : f"คุณชื่อ {self.person_data.get('name', 'ไม่ทราบ')} ค่ะ",
            "ฉันชื่อเล่นอะไร" : f"คุณชื่อเล่นว่า {self.person_data.get('nickname', 'ไม่ทราบ')} ค่ะ",
            "ฉันเกิดวันไหน" : f"คุณเกิดวันที่ {self.person_data.get('birthday', 'ไม่ทราบ')} ค่ะ"
        }

        self.responses.update(additional_responses)

        for response, keywords in grouped_responses.items():
            for keyword in keywords:
                if keyword in user_input:
                    self.add_to_history(user_input, self.responses[response])
                    return self.responses[response]

        for keyword in self.responses:
            if keyword in user_input:
                self.add_to_history(user_input, self.responses[keyword])
                return self.responses[keyword]

        response = "ขอโทษค่ะ ฉันไม่เข้าใจสิ่งที่คุณพูด"
        self.add_to_history(user_input, response)
        return response

    def update_chat_history(self, user_message, bot_message):
        if 'messages' not in st.session_state:
            st.session_state['messages'] = []

        if user_message != "":
            st.session_state['messages'].append(f'<div style="text-align: right;">👤: {user_message}</div>')
            self.stage = 1

        if bot_message != "":
            audio_button, audio_lenght = self.speak(bot_message)

            if self.stage == 1:
                sound1(audio_button)
            elif self.stage == 2:
                sound2(audio_button)
            elif self.stage == 3:
                sound3(audio_button)
            elif self.stage == 4:
                sound4(audio_button)
            elif self.stage == 5:
                sound5(audio_button)

            st.session_state['messages'].append(f'<div style="text-align: left;">🤖: {bot_message}</div>')
            return audio_lenght
            
    def display_chat(self):
        with chat_placeholder:
            chat_html = "<br>".join(st.session_state['messages'])
            st.markdown(
                f"""
                <div id="chat-container" style="height: 40vh; overflow-y: auto; border: 5px solid #ccc; padding: 10px;">
                    {chat_html}
                </div>
                """,
                unsafe_allow_html=True
            )
  
    def run_chatbot(self):
        st.session_state['messages'] = []
        st.session_state.text_received = []
        self.display_chat()
        self.greet()

    def greet(self):
        if self.person_data.get("name"):
            st.session_state['bot_state'] = "prepare"
            update_status_display()
            response = f"สวัสดีค่ะ ใช่ คุณ{self.person_data['name']} ไหมคะ"
            bot = self.update_chat_history("", response)
            self.display_chat()
            time.sleep(bot)
            st.session_state['bot_state'] = "greeting"
            update_status_display()

    def review_person_data(self):
        st.session_state['bot_state'] = "prepare"
        update_status_display()
        bot = self.update_chat_history("", "ขอบคุณสำหรับข้อมูลค่ะ ข้อมูลที่คุณให้มามีดังนี้")
        self.display_chat()
        time.sleep(bot)
        list_data = []
        
        for field in ['name', 'nickname', 'birthday']:
            text = ''
            if field == 'name':
                text = 'ชื่อ'
            elif field == 'nickname':
                text = 'ชื่อเล่น'
            elif field == 'birthday':
                text = 'วันเกิด'
            list_data.append(f"{text}: {self.person_data.get(field, 'ไม่ทราบ')}")
            response = f"{text}: {self.person_data.get(field, 'ไม่ทราบ')}"
            bot = self.update_chat_history("", response)
            self.display_chat()
            time.sleep(bot)

        self.add_to_history_bot_fisrt(list_data, '-')
        
        bot = self.update_chat_history("", "ข้อมูลถูกต้องหรือไม่คะ?")
        self.display_chat()
        time.sleep(bot)
        st.session_state['bot_state'] = "comfirmInfo"
        update_status_display()
        
if 'bot_state' not in st.session_state:
    st.session_state['bot_state'] = ""

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'text_received' not in st.session_state:
    st.session_state.text_received = []

def update_status_display():
    status_text = st.session_state['bot_state']
    status_colors = {
        "": "#808080",        
        "greeting": "#4CAF50",
        "active": "#4CAF50",  
        "new_name": "#FF0000",
        "new_nickname": "#FF0000",
        "new_birthday": "#FF0000",
        "prepare": "#00BFFF",
        "comfirmInfo": "#4CAF50"
    }

    status_messages = {
        "": "ไม่ได้ทำงาน",
        "greeting": "โหมดทักทาย(พูดได้เลย)",
        "active": "โหมดปกติ(พูดได้เลย)",
        "new_name": "โหมดเก็บข้อมูล(พูดได้เลย)",
        "new_nickname": "โหมดเก็บข้อมูล(พูดได้เลย)",
        "new_birthday": "โหมดเก็บข้อมูล(พูดได้เลย)",
        "prepare": "กำลังประมวลผล...(ห้ามพูด)",
        "comfirmInfo": "โหมดยืนยัน(พูดได้เลย)"
    }

    status_placeholder.markdown(
        f"""
        <div style="text-align: center; padding: 5px; border-radius: 5px; background-color: {status_colors[status_text]}; color: white; font-size: 18px; font-weight: bold;">
            {status_messages[status_text]}
        </div>
        """,
        unsafe_allow_html=True
    )

def sound1(html):
    sound_placeholder1.markdown(html, unsafe_allow_html=True)
    chatbot.stage = 2

def sound2(html):
    sound_placeholder2.markdown(html, unsafe_allow_html=True)
    chatbot.stage = 3

def sound3(html):
    sound_placeholder3.markdown(html, unsafe_allow_html=True)
    chatbot.stage = 4

def sound4(html):
    sound_placeholder4.markdown(html, unsafe_allow_html=True)
    chatbot.stage = 5

def sound5(html):
    sound_placeholder5.markdown(html, unsafe_allow_html=True)
    chatbot.stage = 1


chatbot = Chatbot()

with st.sidebar:
    selected = option_menu(
        menu_title= "Menu",
        options=["Home", 
                "Show history", 
                "Show responses", 
                "Show personal data"],
        icons=["wechat", "clock-history", "database", "file-person"],
        menu_icon=["house-door-fill"],
        default_index=0,

    )

if selected == "Home":
    st.markdown(
        """
        <h1 style='text-align: center;'>🤖 Chatbot AI</h1>
        """, 
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 2])

    with col1:
        st.button("🎤Start & Reset", on_click= chatbot.run_chatbot)

    with col2:
        status_placeholder = st.empty()
        update_status_display()

    st.write("")
    microphone_st = speech_to_text(start_prompt="🎤 Talking", stop_prompt="Stop Talking", language='th', use_container_width=True, just_once=True, key='STT')

    chat_placeholder = st.empty()

    col3, col4, col5, col6, col7 = st.columns([1,1,1,1,1])
    with col3:
        sound_placeholder1 = st.empty()
    with col4:
        sound_placeholder2 = st.empty()
    with col5:
        sound_placeholder3 = st.empty()
    with col6:
        sound_placeholder4 = st.empty()
    with col7:
        sound_placeholder5 = st.empty()
    chatbot.display_chat()

    if microphone_st:
        if st.session_state["bot_state"] == "prepare":
            update_status_display()
            pass

        elif st.session_state["bot_state"] == "active":
            st.session_state.text_received.append(microphone_st)
            text = st.session_state.text_received[-1]
            if text:
                st.session_state["bot_state"] = "prepare"
                update_status_display()
                chatbot_response = chatbot.chatbot_response(text)
                chatbot.update_chat_history(text, "")
                chatbot.display_chat()
                if "ขอบคุณ" in text:
                    bot= chatbot.update_chat_history("",chatbot_response)
                    chatbot.display_chat()
                    time.sleep(bot)
                else:
                    bot = chatbot.update_chat_history("",chatbot_response)
                    chatbot.display_chat()
                    time.sleep(bot)
                st.session_state["bot_state"] = "active"
                update_status_display()
        
        elif st.session_state["bot_state"] == "greeting":
            st.session_state.text_received.append(microphone_st)
            text = st.session_state.text_received[-1]
            if text:
                if "ไม่ใช่" in text or "ผิด" in text:
                    st.session_state["bot_state"] = "prepare"
                    update_status_display()
                    chatbot.update_chat_history(text, "")
                    chatbot.display_chat()
                    chatbot.add_to_history_bot_fisrt(f"สวัสดีค่ะ ใช่ คุณ{chatbot.person_data['name']} ไหมคะ", text)
                    bot = chatbot.update_chat_history("", "ขอโทษค่ะ ไม่ทราบว่าชื่ออะไรหรอคะ?")
                    chatbot.display_chat()
                    time.sleep(bot)
                    st.session_state["bot_state"] = "new_name"
                    update_status_display()

                elif "ใช่" in text or "ครับ" in text or "คะ" in text or "ค่ะ" in text:
                    st.session_state["bot_state"] = "prepare"
                    update_status_display()
                    chatbot.update_chat_history(text, "")
                    chatbot.display_chat()

                    chatbot.add_to_history_bot_fisrt(f"สวัสดีค่ะ ใช่ คุณ{chatbot.person_data['name']} ไหมคะ", text)

                    if not chatbot.check_birthday():
                        pass

                    chatbot.add_to_history_bot_fisrt("ไม่ทราบว่าวันนี้ต้องการอะไรหรอกคะ?", '-')
                    bot = chatbot.update_chat_history("", "ไม่ทราบว่าวันนี้ต้องการอะไรหรอกคะ?")
                    chatbot.display_chat()
                    time.sleep(bot)
                    st.session_state["bot_state"] = "active"
                    update_status_display()

        elif st.session_state["bot_state"] == "new_name":
            chatbot.person_data = {}
            st.session_state.text_received.append(microphone_st)
            text = st.session_state.text_received[-1]
            if text:
                st.session_state["bot_state"] = "prepare"
                update_status_display()
                chatbot.update_chat_history(text, "")
                chatbot.display_chat()
                chatbot.add_to_history_bot_fisrt("ขอโทษค่ะ ไม่ทราบว่าชื่ออะไรหรอคะ?", text)
                chatbot.person_data['name'] = chatbot.process_input(text)
                if "ชื่อ" in chatbot.process_input(text):
                    name = chatbot.process_input(text).replace("ชื่อ", "")
                    chatbot.person_data['name'] = name
                chatbot.save_person_data()
                bot = chatbot.update_chat_history("", "ชื่อเล่นของคุณคืออะไรคะ?")
                chatbot.display_chat()
                time.sleep(bot)
                st.session_state["bot_state"] = "new_nickname"
                update_status_display()

        elif st.session_state["bot_state"] == "new_nickname":
            st.session_state.text_received.append(microphone_st)
            text = st.session_state.text_received[-1]
            if text:
                st.session_state["bot_state"] = "prepare"
                update_status_display()
                chatbot.update_chat_history(text, "")
                chatbot.display_chat()
                chatbot.add_to_history_bot_fisrt("ชื่อเล่นของคุณคืออะไรคะ?", text)
                chatbot.person_data['nickname'] = chatbot.process_input(text)
                if "ชื่อ" in chatbot.process_input(text):
                    nickname = chatbot.process_input(text).replace("ชื่อ", "")
                    chatbot.person_data['nickname'] = nickname
                chatbot.save_person_data()
                bot = chatbot.update_chat_history("", "วันเกิดของคุณคืออะไรคะ?")
                chatbot.display_chat()
                time.sleep(bot)
                st.session_state["bot_state"] = "new_birthday"
                update_status_display()

        elif st.session_state["bot_state"] == "new_birthday":
            st.session_state.text_received.append(microphone_st)
            text = st.session_state.text_received[-1]
            if text:
                st.session_state["bot_state"] = "prepare"
                update_status_display()
                chatbot.update_chat_history(text, "")
                chatbot.display_chat()
                chatbot.add_to_history_bot_fisrt("วันเกิดของคุณคืออะไรคะ?", text)
                chatbot.person_data['birthday'] = chatbot.process_input(text)
                if "วันที่" in chatbot.process_input(text):
                    date = chatbot.process_input(text).replace("วันที่", "")
                    chatbot.person_data['birthday'] = date
                chatbot.save_person_data()

                chatbot.person_data = chatbot.load_person_data()

                chatbot.review_person_data()
        
        elif st.session_state["bot_state"] == "comfirmInfo":
            st.session_state.text_received.append(microphone_st)
            text = st.session_state.text_received[-1]
            if text:
                if "ไม่ถูก" in text or "ไม่ใช่" in text:
                    chatbot.add_to_history_bot_fisrt("ไม่ทราบว่าวันนี้ต้องการอะไรหรอกคะ?", '-')
                    bot = chatbot.update_chat_history("", "ไม่ทราบว่าวันนี้ต้องการอะไรหรอกคะ?")
                    chatbot.display_chat()
                    time.sleep(bot)
                    st.session_state["bot_state"] = "active"
                    update_status_display()
                elif "ใช่" in text or "ครับ" in text or "คะ" in text or "ค่ะ" in text or "ถูก" in text:
                    chatbot.update_chat_history(text, "")
                    chatbot.display_chat()
                    chatbot.save_person_data()
                    response = f"เข้าใจแล้วค่ะ! สวัสดีค่ะ {chatbot.person_data['nickname']} ยินดีที่ได้รู้จักค่ะ!"
                    bot = chatbot.update_chat_history("", response)
                    chatbot.display_chat()
                    time.sleep(bot)

                    if not chatbot.check_birthday():
                        pass
                    
                    chatbot.add_to_history_bot_fisrt("ไม่ทราบว่าวันนี้ต้องการอะไรหรอกคะ?", '-')
                    bot = chatbot.update_chat_history("", "ไม่ทราบว่าวันนี้ต้องการอะไรหรอกคะ?")
                    chatbot.display_chat()
                    time.sleep(bot)
                    st.session_state["bot_state"] = "active"
                    update_status_display()

elif selected == "Show history":
    chatbot.show_history_json_as_table(chatbot.history, "Chat History")

elif selected == "Show responses":
    st.write("Showing responses data")
    chatbot.show_json(chatbot.responses, "responses.json")

elif selected == "Show personal data":
    st.write("แก้ไขข้อมูลส่วนตัว")
    chatbot.person_data = chatbot.load_person_data()

    name = st.text_input("ชื่อ", value=chatbot.person_data.get('name', ''))
    nickname = st.text_input("ชื่อเล่น", value=chatbot.person_data.get('nickname', ''))
    birthday = st.text_input("วันเกิด", value=chatbot.person_data.get('birthday', ''))

    if st.button("บันทึกข้อมูล"):
        chatbot.person_data['name'] = name
        chatbot.person_data['nickname'] = nickname
        chatbot.person_data['birthday'] = birthday
        chatbot.save_person_data()    
        st.toast("Success!")
    chatbot.person_data = chatbot.load_person_data()
