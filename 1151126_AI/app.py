from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4
import math

app = Flask(__name__)
CORS(app)

# 模擬資料庫：每次重新啟動時建立初始資料
products = [
    {
        "id": str(uuid4()),
        "name": "霓虹墨鏡",
        "category": "街頭服飾",
        "price": 45,
        "num": 32,
        "remark": "夜城限定款"
    },
    {
        "id": str(uuid4()),
        "name": "海灘襯衫",
        "category": "街頭服飾",
        "price": 55,
        "num": 18,
        "remark": "熱帶印花"
    },
    {
        "id": str(uuid4()),
        "name": "霓虹車燈",
        "category": "車輛配件",
        "price": 85,
        "num": 8,
        "remark": "改裝專用"
    },
    {
        "id": str(uuid4()),
        "name": "能量飲料",
        "category": "日常補給",
        "price": 25,
        "num": 60,
        "remark": "冰涼飲用"
    },
    {
        "id": str(uuid4()),
        "name": "無線耳機",
        "category": "電子裝備",
        "price": 95,
        "num": 12,
        "remark": "附充電盒"
    },
    {
        "id": str(uuid4()),
        "name": "街頭帽T",
        "category": "街頭服飾",
        "price": 80,
        "num": 7,
        "remark": "限量配色"
    },
    {
        "id": str(uuid4()),
        "name": "復古球鞋",
        "category": "街頭服飾",
        "price": 90,
        "num": 24,
        "remark": "經典復刻款"
    },
    {
        "id": str(uuid4()),
        "name": "棕櫚棒球帽",
        "category": "街頭服飾",
        "price": 35,
        "num": 45,
        "remark": "海岸系列"
    },
    {
        "id": str(uuid4()),
        "name": "夜行皮夾克",
        "category": "街頭服飾",
        "price": 100,
        "num": 5,
        "remark": "夜店聯名款"
    },
    {
        "id": str(uuid4()),
        "name": "賽車貼紙",
        "category": "車輛配件",
        "price": 15,
        "num": 80,
        "remark": "防水耐曬"
    },
    {
        "id": str(uuid4()),
        "name": "合金輪圈",
        "category": "車輛配件",
        "price": 100,
        "num": 6,
        "remark": "輕量化設計"
    },
    {
        "id": str(uuid4()),
        "name": "方向盤套",
        "category": "車輛配件",
        "price": 40,
        "num": 28,
        "remark": "防滑材質"
    },
    {
        "id": str(uuid4()),
        "name": "車用香氛",
        "category": "車輛配件",
        "price": 30,
        "num": 56,
        "remark": "熱帶水果香"
    },
    {
        "id": str(uuid4()),
        "name": "碳纖維尾翼",
        "category": "車輛配件",
        "price": 98,
        "num": 3,
        "remark": "競速限定款"
    },
    {
        "id": str(uuid4()),
        "name": "椰子冰飲",
        "category": "日常補給",
        "price": 20,
        "num": 75,
        "remark": "海灘熱銷品"
    },
    {
        "id": str(uuid4()),
        "name": "雙層漢堡",
        "category": "日常補給",
        "price": 35,
        "num": 48,
        "remark": "建議趁熱食用"
    },
    {
        "id": str(uuid4()),
        "name": "旅行水壺",
        "category": "日常補給",
        "price": 45,
        "num": 22,
        "remark": "耐熱防漏"
    },
    {
        "id": str(uuid4()),
        "name": "運動飲料",
        "category": "日常補給",
        "price": 18,
        "num": 100,
        "remark": "快速補充水分"
    },
    {
        "id": str(uuid4()),
        "name": "智慧手機",
        "category": "電子裝備",
        "price": 100,
        "num": 15,
        "remark": "夜城通訊系列"
    },
    {
        "id": str(uuid4()),
        "name": "行動電源",
        "category": "電子裝備",
        "price": 65,
        "num": 36,
        "remark": "支援快速充電"
    },
    {
        "id": str(uuid4()),
        "name": "運動相機",
        "category": "電子裝備",
        "price": 90,
        "num": 9,
        "remark": "防水防震"
    },
    {
        "id": str(uuid4()),
        "name": "車載音響",
        "category": "電子裝備",
        "price": 88,
        "num": 20,
        "remark": "重低音強化"
    }
]

# 允許新增與更新的欄位
fields = ["name", "category", "price", "num", "remark"]


# 用 ID 尋找產品
def find_product(id: str):
    for product in products:
        if product["id"] == id:
            return product
    return None


# 驗證資料；成功回傳整理後的資料、None、200
# 失敗回傳 None、錯誤訊息、HTTP 狀態碼
# partial=True 表示 PATCH，只要求傳入需要更新的欄位
def validate_product(data, id=None, partial=False):
    if not isinstance(data, dict) or not data:
        return None, "請傳送非空的 JSON Object", 400

    if "id" in data:
        return None, "不允許自行設定或修改產品 ID", 400

    for key in data:
        if key not in fields:
            return None, "不支援的欄位：" + key, 400

    if not partial:
        for key in fields:
            if key not in data:
                return None, "缺少欄位：" + key, 400

    # 複製資料，避免驗證時直接修改原始產品
    result = data.copy()

    for key in ["name", "category"]:
        if key in data:
            if not isinstance(data[key], str) or not data[key].strip():
                return None, key + " 必須為非空白文字", 400
            result[key] = data[key].strip()

    if "remark" in data:
        if not isinstance(data["remark"], str):
            return None, "產品備註必須為文字", 400

    # 相容 jQuery .val() 傳入的數字字串
    if "price" in data:
        price = data["price"]
        if type(price) not in (int, float, str):
            return None, "產品價格必須為非負數", 400
        try:
            price = float(price)
        except (ValueError, OverflowError):
            return None, "產品價格必須為非負數", 400
        if not math.isfinite(price) or price < 0:
            return None, "產品價格必須為非負數", 400
        if price.is_integer():
            price = int(price)
        result["price"] = price

    if "num" in data:
        num = data["num"]
        if isinstance(num, str):
            try:
                num = int(num)
            except ValueError:
                return None, "庫存數量必須為非負整數", 400
        if type(num) is not int or num < 0:
            return None, "庫存數量必須為非負整數", 400
        result["num"] = num

    # 更新時排除自己，避免原本的名稱被判斷為重複
    if "name" in result:
        for product in products:
            if product["id"] != id and product["name"] == result["name"]:
                return None, "產品名稱已存在，不可以重複", 409

    return result, None, 200


# 測試 API 是否正常運作
@app.route("/info")
def info():
    return jsonify({"message": "API運作正常!"}), 200


# GET：讀取全部產品
@app.route("/product", methods=["GET"])
def product_get_all():
    return jsonify(products), 200


# GET：讀取指定產品
@app.route("/product/<id>", methods=["GET"])
def product_get(id):
    target = find_product(id)
    if target is None:
        return jsonify({"error": "查無此產品"}), 404
    return jsonify(target), 200


# POST：新增產品
@app.route("/product", methods=["POST"])
def product_add():
    data = request.get_json(silent=True)
    result, error, status = validate_product(data)
    if error is not None:
        return jsonify({"error": error}), status

    product = {"id": str(uuid4())}
    product.update(result)
    products.append(product)
    return jsonify(product), 201


# PUT：完整更新產品
@app.route("/product/<id>", methods=["PUT"])
def product_update(id):
    target = find_product(id)
    if target is None:
        return jsonify({"error": "查無此產品"}), 404

    data = request.get_json(silent=True)
    result, error, status = validate_product(data, id)
    if error is not None:
        return jsonify({"error": error}), status

    target.update(result)
    return jsonify(target), 200


# PATCH：部分更新產品
@app.route("/product/<id>", methods=["PATCH"])
def product_patch(id):
    target = find_product(id)
    if target is None:
        return jsonify({"error": "查無此產品"}), 404

    data = request.get_json(silent=True)
    result, error, status = validate_product(data, id, partial=True)
    if error is not None:
        return jsonify({"error": error}), status

    target.update(result)
    return jsonify(target), 200


# DELETE：刪除指定產品，回傳被刪除的產品
@app.route("/product/<id>", methods=["DELETE"])
def product_delete(id):
    target = find_product(id)
    if target is None:
        return jsonify({"error": "查無此產品"}), 404

    products.remove(target)
    return jsonify(target), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4001)
