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

    if "ในภาษาอังกฤษคือ" in text:
        text = text.replace("ในภาษาอังกฤษคือ", "").strip()
    if "ในภาษาอังกฤษ" in text:
        text = text.replace("ในภาษาอังกฤษ", "").strip()
    if "ภาษาอังกฤษคือ" in text:
        text = text.replace("ภาษาอังกฤษคือ", "").strip()
    if "ภาษาอังกฤษ" in text:
        text = text.replace("ภาษาอังกฤษ", "").strip()
    if "แปล" in text:
        text = text.replace("แปล", "").strip()
    if "คำว่า" in text:
        text = text.replace("คำว่า", "").strip()
    if "ช่วย" in text:
        text = text.replace("ช่วย", "").strip()
    if "หน่อย" in text:
        text = text.replace("หน่อย", "").strip()
    
    translator = Translator()
    result = translator.translate(text, src='th', dest='en')
    return result.text, text

