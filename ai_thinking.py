import re
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
    start_phrases = ["แปลคำว่า", "ช่วยแปลคำว่า", "คำว่า", "แปล", "ช่วยแปล"]
    for phrase in start_phrases:
        if text.startswith(phrase):
            text = text[len(phrase):].strip()
            break
    end_phrases = [
        "ในภาษาอังกฤษคือ", "ภาษาอังกฤษคือ", "ในภาษาอังกฤษคืออะไร", 
        "ภาษาอังกฤษคืออะไร", "เป็นภาษาอังกฤษให้หน่อย", "เป็นภาษาอังกฤษหน่อย", 
        "เป็นภาษาอังกฤษ"
    ]
    for phrase in end_phrases:
        if text.endswith(phrase) and len(text) > len(phrase):
            text = text[:-len(phrase)].strip()
            break
    
    translator = Translator()
    result = translator.translate(text, src='th', dest='en')
    return result.text, text

