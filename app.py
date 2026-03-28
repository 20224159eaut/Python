import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI

# 🔑 Thay API KEY của bạn vào đây
client = OpenAI(api_key="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")

def sinh_code_ai():
    yeu_cau = txt_nhap.get("1.0", tk.END).strip()

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là AI chuyên viết code Python đơn giản, dễ hiểu cho sinh viên. Chỉ trả về code, không giải thích."
                },
                {
                    "role": "user",
                    "content": yeu_cau
                }
            ],
            temperature=0.2
        )

        code = response.choices[0].message.content

    except Exception as e:
        code = "Lỗi: " + str(e)

    txt_ket_qua.delete("1.0", tk.END)
    txt_ket_qua.insert(tk.END, code)


# GUI
app = tk.Tk()
app.title("ChatGPT Mini - Sinh Code Python")
app.geometry("700x550")

# Nhập yêu cầu
lbl1 = tk.Label(app, text="Nhập yêu cầu bài toán:")
lbl1.pack()

txt_nhap = scrolledtext.ScrolledText(app, height=5)
txt_nhap.pack(padx=10, pady=5)

# Nút
btn = tk.Button(app, text="Sinh code bằng AI", command=sinh_code_ai)
btn.pack(pady=10)

# Kết quả
lbl2 = tk.Label(app, text="Code Python:")
lbl2.pack()

txt_ket_qua = scrolledtext.ScrolledText(app, height=20)
txt_ket_qua.pack(padx=10, pady=5)

# Chạy
app.mainloop()