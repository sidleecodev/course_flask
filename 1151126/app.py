from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'Hello Flask!'

# @app.route('/about')
# def about():
#     return '自介內容：'


@app.route("/product/id")
def productId():
    return jsonify(["標題", "所有產品的id都在這邊"])


# 測試api用
@app.route("/info")
def info():
    return jsonify({"message": "API運作正常!"})


# 建立一個模擬資料庫
products = [
    {"created_at": "2026-11-26 15:23:05", "id": 1, "name": "四季可可亞", "price": 85},
    {"created_at": "2026-11-26 15:23:12", "id": 2, "name": "黑糖珍珠鮮奶", "price": 75},
    {"created_at": "2026-11-26 15:23:18", "id": 3, "name": "茉莉翡翠綠茶", "price": 35},
    {"created_at": "2026-11-26 15:23:21", "id": 4, "name": "北海道奶茶", "price": 65},
    {"created_at": "2026-11-26 15:23:27", "id": 5, "name": "蜂蜜檸檬", "price": 55},
    {"created_at": "2026-11-26 15:23:32", "id": 6, "name": "宇治抹茶拿鐵", "price": 90},
    {"created_at": "2026-11-26 15:23:39", "id": 7, "name": "蜜桃烏龍茶", "price": 60},
    {"created_at": "2026-11-26 15:23:44", "id": 8, "name": "焦糖瑪奇朵", "price": 95},
    {"created_at": "2026-11-26 15:23:51", "id": 9, "name": "芒果冰沙", "price": 80},
    {"created_at": "2026-11-26 15:23:58", "id": 10, "name": "桂花四季春", "price": 45},
]


#用ID尋找產品的function
def find_product(id: int):
    for product in products:
        if product['id'] == id:
            return product
    return None


# 建立POST API路由 /product
@app.route("/product", methods=["POST"])
def product_add():
    # 從前端接收資料(JSON)
    try:
        data = request.get_json()
        if data is None:
            raise ValueError
    except Exception:
        return jsonify({"error": "請傳送JSON格式的資料"}), 400

    # 取得產品名稱與價格
    name = data.get("name")
    price = data.get("price")

    # 資料驗證
    if not name or not price:
        return jsonify({"error": "請提供產品名稱與價格"}), 400

    # 將資料擺入模擬資料庫 products
    product = {
        "id": len(products) + 1,
        "name": name,
        "price": price,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    products.append(product)

    return (
        jsonify({"message": "新增成功", "newData": product, "products": products}),
        201,
    )


# 建立 GET API路由 /product
@app.route("/product", methods=["GET"])
def product_get_all():
    return jsonify({"message": "產品資料讀取成功", "products": products})


# 建立 GET/id API路由 /product/id
@app.route("/product/<int:id>", methods=["GET"])
def product_get(id):
    # 尋找指定ID的產品
    for product in products:
        if product["id"] == id:
            return jsonify({"message": "產品讀取成功", "product": product}), 200

    return jsonify({"error": "查無此產品"}), 404


# 建立 PUT/id API路由 /product/id
@app.route("/product/<int:id>", methods=["PUT"])
def product_update(id):
    try:
        data = request.get_json()
        if data is None:
            raise ValueError
    except Exception:
        return jsonify({"error": "請傳送JSON格式的資料"}), 400

    # 取得產品名稱與價格
    name = data.get("name")
    price = data.get("price")
    
    # 資料驗證
    if name is not None and not isinstance(name, str):
        return jsonify({"error" : "產品名稱必須為文字格式"}), 400
    if price is not None and not isinstance(price, (int, float)):
        return jsonify({"error" : "產品價格必須為數字格式"}), 400
    if isinstance(price, (int, float)) and price < 0:
        return jsonify({"error" : "產品價格不可以是負數"}), 400

    # 尋找要更新的產品
    target = find_product(id)
    if target is None:
        return jsonify({'error' : '查無此產品'})
    if target is not None:
        for product in products:
            if product['id'] != id and product['name'] == name:
                return jsonify({'error' : '產品名稱已存在，不可以重複'}), 409

    # 執行更新
    if name is not None:
        target['name'] = name
    if price is not None:
        target['price'] = price

    return jsonify({'message' : '更新成功', 'product' : target}), 200

# 建立 DELETE/id API路由 /product/id
@app.route("/product/<int:id>", methods=["DELETE"])
def product_delete(id):
    # 尋找指定ID的產品，並且刪除
    for product in products:
        if product["id"] == id:
            products.remove(product)
            return jsonify({"message": "產品刪除成功", "products": products}), 200
    return jsonify({"error": "查無此產品"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)
