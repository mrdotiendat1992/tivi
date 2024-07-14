from pyodbc import connect

def connect_db():
    conn = connect(r'DRIVER={SQL Server};SERVER=172.16.60.100;DATABASE=DW;UID=huynguyen;PWD=Namthuan@123')
    return conn

def close_db(conn):
    conn.close()
    
def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor

def lay_data_goi_y():
    conn = connect_db()
    cursor = execute_query(conn, 'select * from TGLV_TRONG_NGAY_GOI_Y').fetchall()
    result = list(cursor)
    close_db(conn)
    return result

def lay_cac_xuong():
    conn = connect_db()
    cursor = execute_query(conn, 'select distinct XUONG from TGLV_TRONG_NGAY_GOI_Y').fetchall()
    result = list(x[0] for x in cursor)
    close_db(conn)
    return result
    
def capnhatthongtincongnhan(chuyen,xuong,tongcnmay,cnmaydilam,socntinhsah):
    try:
        cnmaynghi = int(tongcnmay) - int(cnmaydilam)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"update TGLV_TRONG_NGAY_GOI_Y set TONG_CN_MAY = '{tongcnmay}', SO_CN_DI_LAM = '{cnmaydilam}', SO_CN_NGHI = '{cnmaynghi}', CN_TINH_SAH = '{socntinhsah}' where CHUYEN = '{chuyen}' and XUONG = '{xuong}'")
        conn.commit()
        close_db(conn)
        return True
    except:
        return False
    
def capnhatgiobatdaumoi(xuong,giobatdaumoi):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"update TGLV_TRONG_NGAY_GOI_Y set GIO_BAT_DAU = '{giobatdaumoi}' where XUONG = '{xuong}'")
        conn.commit()
        close_db(conn)
        return True
    except:
        return False
    
def capnhatgioketthucmoi(xuong,gioketthucmoi):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"update TGLV_TRONG_NGAY_GOI_Y set GIO_KET_THUC = '{gioketthucmoi}' where XUONG = '{xuong}'")
        conn.commit()
        close_db(conn)
        return True
    except:
        return False