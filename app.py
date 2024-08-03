from flask import Flask, render_template,request, flash, redirect,get_flashed_messages
from flask_cors import CORS
from datetime import datetime, timedelta
from ultils import *
from waitress import serve
import time
import subprocess
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

CORS(app)

def round_down_time(dt):
    hour = dt.hour
    minute = dt.minute

    # Define the intervals: 0:00, 0:30, 1:00, 1:30, ...
    intervals = [0, 30]

    # Find the closest past interval
    closest_past_interval = max([i for i in intervals if i <= minute])

    # Adjust the hour if necessary
    if minute < 30:
        rounded_hour = hour
    else:
        rounded_hour = hour

    # Create the new datetime object
    new_dt = datetime(dt.year, dt.month, dt.day, rounded_hour, closest_past_interval)

    # If the new time is greater than the original, subtract 30 minutes
    if new_dt > dt:
        new_dt -= timedelta(minutes=30)
    
    if new_dt.minute == 0:
        new_dt = new_dt - timedelta(minutes=30)

    return new_dt.strftime("%H:%M")

@app.route('/')
def index():
    cacxuong = ["1P01","1P02","1P03","2P01","2P02","2P03","2P04", "2P05"]
    giohientai = datetime.now()
    giohienthi = round_down_time(giohientai)
    xuong = request.args.get('xuong')
    if not xuong:
        xuong = "1P01"
    data_xuong = lay_data_theo_xuong(xuong) 
    data_nhamay = lay_data_theo_nhamay(xuong) 
    data_toan_congty = lay_data_toan_congty()
    return render_template('index.html',cacxuong=cacxuong,
                           thoigian=giohienthi,
                           data_xuong = data_xuong,
                           data_nhamay = data_nhamay,
                           data_toan_congty= data_toan_congty)

@app.route('/nhapvao',methods=['GET','POST'])
def input_data():
    if request.method == 'POST':
        giobatdau = request.form.get('giobatdau')
        gioketthuc = request.form.get('gioketthuc')
        chuyen = request.form.get('chuyen')
        xuong = request.args.get('xuong')
        tongcnmay = request.form.get('tongcnmay')
        cnmaydilam = request.form.get('socndilam')
        socntinhsah = request.form.get('socntinhsah')
        if capnhatthongtincongnhan(chuyen,xuong,tongcnmay,cnmaydilam,socntinhsah,giobatdau,gioketthuc):
            flash('Cập nhật thành công')
        else:
            flash('Cập nhật thất bại')
        return redirect("nhapvao?xuong="+xuong)
    else:
        cac_xuong = lay_cac_xuong()
        xuong = request.args.get('xuong')
        data = lay_data_goi_y(xuong)
        ngay = datetime.now().strftime("%d-%m-%Y")
        flash_messages = get_flashed_messages()
        if flash_messages is None:
            flash_messages = []
        if not xuong:
            xuong = "1P01"
            return redirect("nhapvao?xuong="+xuong)
        return render_template('input.html',data=data,cac_xuong=cac_xuong,ngay=ngay,flash_messages=flash_messages)

@app.route('/nhapfile',methods=['POST'])
def nhapdulieutuexcel():
    try:
        kieufile = request.form.get('kieufile')
        file = request.files['file']
        if int(kieufile) == 1: # Nhập số lượng công nhân
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filepath = os.path.join(os.getcwd(),f"upload/soluong_congnhan_{timestamp}.xlsx")
            file.save(filepath)
            print("Upload file success !!!")
            data = pd.read_excel(filepath).to_dict(orient="records")
            for row in data:
                values = [value for key, value in row.items()]
                gio_bat_dau_str = str(values[7]).split(":")
                gio_bat_dau = f"{int(gio_bat_dau_str[0])}:{gio_bat_dau_str[1]}"
                print(gio_bat_dau)
                query = f"""UPDATE TGLV_TRONG_NGAY_GOI_Y
                            SET TONG_CN_MAY = '{values[3]}', SO_CN_DI_LAM = '{values[4]}', SO_CN_NGHI = '{values[5]}', CN_TINH_SAH = '{values[6]}', GIO_BAT_DAU = '{gio_bat_dau}', GIO_KET_THUC = '{str(values[8])[:5]}'
                            WHERE NHA_MAY = '{values[0]}' AND CHUYEN = '{values[2]}' AND XUONG = '{values[1]}'"""
                print(query)
                conn = connect_db()
                cursor = execute_query(conn,query)
                conn.commit()
                close_db(conn)
        elif int(kieufile) == 2: # Nhập style
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filepath = os.path.join(os.getcwd(),f"style_{timestamp}.xlsx")
            file.save(filepath)
            print("Upload file success !!!")
            data = pd.read_excel(filepath).to_dict(orient="records")
            for row in data:
                values = [value for key, value in row.items()]
                query = f"""INSERT INTO STYLE_A (WorkDate,Workline,Style_No) VALUES ('{values[0]}','{values[1]}','{values[2]}')"""
                print(query)
                conn = connect_db()
                cursor = execute_query(conn,query)
                conn.commit()
                close_db(conn)
        elif int(kieufile) == 3: # Nhập sản lượng
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filepath = os.path.join(os.getcwd(),f"sanluong_{timestamp}.xlsx")
            file.save(filepath)
            print("Upload file success !!!")
            data = pd.read_excel(filepath).to_dict(orient="records")
            for row in data:
                values = [value for key, value in row.items()]
                timestamp = str(values[-1])[:-3]
                query = f"INSERT INTO ETS_Qty VALUES ('{values[0]}','{values[1]}','{values[2]}','{values[3]}','{values[4]}','{timestamp}')"
                print(query)
                conn = connect_db()
                cursor = execute_query(conn,query)
                conn.commit()
                close_db(conn)
        return redirect("/nhapvao")
    except Exception as e:
        print(f"Loi khi nhap du lieu tu file: {e}")
        return redirect("/nhapvao")
    
if __name__ == "__main__":
    while True:
        try:
            app.run(debug=False, host="0.0.0.0", port=82)
        except subprocess.CalledProcessError as e:
            app.logger.error(f"Flask gap loi: {e}")
            print("Đang khoi dong flask...")
            time.sleep(1)  # Đợi một khoảng thời gian trước khi khởi động lại
        except Exception as e:
            app.logger.error(f"Loi khong xac dinh: {e}")
            print("Đang khoi dong lai flask ...")
            time.sleep(1)