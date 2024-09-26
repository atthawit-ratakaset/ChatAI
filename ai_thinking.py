import re

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
