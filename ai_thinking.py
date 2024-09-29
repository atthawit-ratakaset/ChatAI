import re
import contractions
from googletrans import Translator

def calculate_ai(text):
    try:
        text = text.replace('บวก', '+')
        text = text.replace('ลบ', '-')
        text = text.replace('คูณ', '*')
        text = text.replace('หาร', '/')
        
        text = text.replace(',', '')
        
        expression = ''.join(re.findall(r'[0-9+\-*/.]+', text))
        
        if expression:
            result = eval(expression)
            
            if isinstance(result, int) or result.is_integer():
                response = f"คำตอบคือ {int(result)}"
            else:
                response = f"คำตอบคือ {result:.2f}"
        else:
            response = "ไม่สามารถตอบได้ค่ะ ขอโทษด้วยค่ะ"
        
        return response
    except Exception as e:
        return f"ไม่สามารถตอบได้ค่ะ ขอโทษด้วยค่ะ"

def word_translator(text):
    start_phrases = [
        "ช่วยแปลคำว่า", "ช่วยแปลประโยค", "แปลประโยค", "แปลคำว่า", 
        "ช่วยแปล", "แปล", "คำว่า", "ประโยค"
    ]
    for phrase in start_phrases:
        if text.startswith(phrase):
            text = text[len(phrase):].strip()
            break
    
    end_phrases = [
        "เป็นภาษาอังกฤษให้ฟังหน่อย", "เป็นภาษาอังกฤษให้ฟังที", "เป็นภาษาอังกฤษให้หน่อย", 
        "เป็นภาษาอังกฤษหน่อย", "ในภาษาอังกฤษคืออะไร", "ในภาษาอังกฤษคือ", 
        "ในภาษาอังกฤษ", "ภาษาอังกฤษคืออะไร", "เป็นภาษาอังกฤษ", 
        "ภาษาอังกฤษให้ฟังที", "ภาษาอังกฤษให้ฟังหน่อย", "ภาษาอังกฤษคือ", "ภาษาอังกฤษ"
    ]
    for phrase in end_phrases:
        if phrase in text:
            text = text.replace(phrase, "").strip()
    
    translator = Translator()
    result = translator.translate(text, src='th', dest='en')
    
    translated_text = result.text
    expanded_text = contractions.fix(translated_text)

    return expanded_text, text
