from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

#自動建立資料庫
def init_db():
    conn = sqlite3.connect('member.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/info')
def info():
    return jsonify({"message" : "API運作正常"})

# 會員註冊 API /member POST
@app.route('/member', methods=['POST'])
def member_add():
    # 從前端接收資料(JSON)
    try:
        data = request.get_json()
        if data is None:
            raise ValueError
    except Exception:
        return jsonify({"error": "請傳送JSON格式的資料"}), 400

    # 取得產品名稱與價格
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    # 資料驗證
    if username is None or not isinstance(username, str):
        return jsonify({"error" : "使用者名稱不符合格式"}), 400
    if password is None or not isinstance(password, str):
        return jsonify({"error" : "密碼不符合格式"}), 400
    if email is None or not isinstance(email, str):
        return jsonify({"error" : "電子信箱不符合格式"}), 400

    conn = sqlite3.connect("member.db")
    cursor = conn.cursor()

    # 檢查帳號是否已經存在
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    existing_username = cursor.fetchone()
    if existing_username:
        conn.close()
        return jsonify({
            "error" : "此帳號已經存在"
        }), 409

    # 新增資料到資料庫
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()

    return jsonify({
        "message" : "會員註冊成功",
        "username" : username
    }), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port = 4002)