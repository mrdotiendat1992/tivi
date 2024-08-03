from pyodbc import connect

def connect_db():
    conn = connect(r'DRIVER={SQL Server};SERVER=172.16.60.100;DATABASE=DW;UID=huynguyen;PWD=Namthuan@123')
    # conn = connect(r'DRIVER={SQL Server};SERVER=DESKTOP-G635SF6;DATABASE=DW;Trusted_Connection=yes')
    return conn

def close_db(conn):
    conn.close()
    
def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor

def lay_data_goi_y(xuong):
    conn = connect_db()
    cursor = execute_query(conn, f"select * from TGLV_TRONG_NGAY_GOI_Y where XUONG = '{xuong}' ORDER BY Chuyen ASC").fetchall()
    result = list(cursor)
    close_db(conn)
    return result

def lay_cac_xuong():
    conn = connect_db()
    cursor = execute_query(conn, 'select distinct XUONG from TGLV_TRONG_NGAY_GOI_Y').fetchall()
    result = list(x[0] for x in cursor)
    close_db(conn)
    return result
    
def capnhatthongtincongnhan(chuyen,xuong,tongcnmay,cnmaydilam,socntinhsah,giobatdau,gioketthuc):
    try:
        if ":" not in giobatdau or ":" not in gioketthuc:
            return False
        cnmaynghi = int(tongcnmay) - int(cnmaydilam)
        conn = connect_db()
        cursor = conn.cursor()
        query = f"update TGLV_TRONG_NGAY_GOI_Y set TONG_CN_MAY = '{tongcnmay}', SO_CN_DI_LAM = '{cnmaydilam}', SO_CN_NGHI = '{cnmaynghi}', CN_TINH_SAH = '{socntinhsah}', GIO_BAT_DAU = '{giobatdau}', GIO_KET_THUC = '{gioketthuc}' where CHUYEN = '{chuyen}' and XUONG = '{xuong}'"
        cursor.execute(query)
        conn.commit()
        close_db(conn)
        return True
    except Exception as e:
        print(e)
        return False
    
def lay_data_theo_xuong(xuong):
    conn = connect_db()
    cursor = execute_query(conn, f"select * from SAN_LUONG_HANG_GIO where XUONG = '{xuong}' ORDER BY Chuyen ASC" ).fetchall()
    result = list(cursor)
    close_db(conn)
    return result

def lay_data_theo_nhamay(xuong):
    conn = connect_db()
    cursor = execute_query(conn, f"select * from SAN_LUONG_THEO_GIO_XUONG where XUONG LIKE '{xuong[0]}%'" ).fetchall()
    result = list(cursor)
    close_db(conn)
    return result

def lay_data_toan_congty():
    conn = connect_db()
    cursor = execute_query(conn, 'select * from SAN_LUONG_THEO_GIO_NHA_MAY').fetchall()
    result = list(cursor)
    close_db(conn)
    return result