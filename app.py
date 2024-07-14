from flask import Flask, render_template,request, flash, redirect,get_flashed_messages
from flask_cors import CORS
from datetime import datetime
from ultils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

CORS(app)

@app.route('/')
def index():
    xuong = ["1P01","1P02","2P01","2P02","2P03"]
    # Lấy thòi gian khi request được gủi đến, làm tròn thời gian lùi về trước 30 phút
    giohientai = datetime.now().hour
    print(giohientai)
    giohienthi = f"{giohientai-1}:30"
    return render_template('index.html',xuong=xuong,thoigian=giohienthi)

@app.route('/nhapvao',methods=['GET','POST'])
def input_data():
    if request.method == 'POST':
        giobatdaumoi = request.form.get('giobatdaumoi')
        if giobatdaumoi:
            xuong= request.args.get('xuong')
            capnhatgiobatdaumoi(xuong,giobatdaumoi)
            flash('Cập nhật thành công')
            return redirect("nhapvao?xuong="+xuong)
        gioketthucmoi = request.form.get('gioketthucmoi')
        if gioketthucmoi:
            xuong= request.args.get('xuong')
            capnhatgioketthucmoi(xuong,gioketthucmoi)
            flash('Cập nhật thành công')
            return redirect("nhapvao?xuong="+xuong)
        chuyen = request.form.get('chuyen')
        xuong = request.args.get('xuong')
        tongcnmay = request.form.get('tongcnmay')
        cnmaydilam = request.form.get('socndilam')
        socntinhsah = request.form.get('socntinhsah')
        if capnhatthongtincongnhan(chuyen,xuong,tongcnmay,cnmaydilam,socntinhsah):
            flash('Cập nhật thành công')
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
    app.run(debug=True, host='0.0.0.0', port=80)