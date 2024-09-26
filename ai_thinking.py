import re

def calculate_ai(text):
    try:
        text = text.replace(',', '')
        
        expression = re.findall(r'[0-9+\-*/.]+', text)
        
        expression = ' '.join(expression)
        
        if expression:
            result = eval(expression)
            
            if isinstance(result, int) or result.is_integer():
                response = f"คำตอบคือ {int(result)}"
            else:
                response = f"คำตอบคือ {expression} = {result:.2f}"
        else:
            response = "ไม่พบสมการในข้อความที่คุณป้อน"
        
        return response
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"