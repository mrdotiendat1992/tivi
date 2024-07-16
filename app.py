from flask import Flask, render_template,request, flash, redirect,get_flashed_messages
from flask_cors import CORS
from datetime import datetime
from ultils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

CORS(app)

@app.route('/')
def index():
    cacxuong = ["1P01","1P02","2P01","2P02","2P03"]
    xuong = request.args.get('xuong')
    # Lấy thòi gian khi request được gủi đến, làm tròn thời gian lùi về trước 30 phút
    giohientai = datetime.now().hour
    giohienthi = f"{giohientai-1}:30"
    data = lay_data_theo_xuong(xuong) 
    return render_template('index.html',cacxuong=cacxuong,thoigian=giohienthi,data = data)

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
        data = lay_data_goi_y()
        xuong = lay_cac_xuong()
        ngay = datetime.now().strftime("%d-%m-%Y")
        flash_messages = get_flashed_messages()
        if flash_messages is None:
            flash_messages = []
        return render_template('input.html',data=data,xuong=xuong,ngay=ngay,flash_messages=flash_messages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=82)