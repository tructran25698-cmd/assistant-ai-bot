import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Cấu hình API Key của Gemini
genai.configure(api_key="AQ.Ab8RN6Jcu2qJy44u7JpgRqgt9Gjvchcyn3TYsFK-qWv6H25XdA")

PROMPT_GOC = """
Bạn là trợ lý AI quản lý lịch trình cá nhân. Hãy dựa vào tình trạng sức khỏe và giấc ngủ của người dùng để đưa ra lịch trình 1 ngày dạng văn bản ngắn gọn, tập trung vào việc khuyên họ nên làm gì vào buổi sáng (chạy bộ hay nghỉ ngơi) và tối từ 19h-21h (ôn kỹ năng, tập piano, hay đi chơi).

Khung giờ cố định của họ:
- 4h30 thức dậy.
- 6h30 đi làm + ăn sáng. 7h50 làm việc. 12h05 nghỉ trưa. 12h55 làm việc đến 17h.
- 17h - 19h: Về nhà, nấu cơm, vệ sinh, giặt đồ.
- 19h - 21h: Việc riêng (chọn 1 trong 3: ôn kỹ năng, tập piano, hoặc đi chơi tùy sức khỏe).
- 21h30: Đi ngủ.

Hãy trả về câu trả lời bằng tiếng Việt, ngắn gọn để điện thoại có thể đọc thành giọng nói (Text-to-Speech) một cách tự nhiên, mạch lạc, không chứa các ký tự đặc biệt như dấu sao (*), dấu gạch đầu dòng (-).
"""

@app.route('/get_schedule', methods=['POST'])
def get_schedule():
    data = request.json
    user_status = data.get("status", "Bình thường") # Ví dụ: "Đêm qua thiếu ngủ, mệt mỏi"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"{PROMPT_GOC}\nTình trạng hôm nay của người dùng: {user_status}")
        
        # Trả kết quả về cho MacroDroid
        return jsonify({"schedule": response.text.strip()})
    except Exception as e:
        return jsonify({"schedule": "Có lỗi xảy ra khi kết nối với bộ não AI."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
