from http import server
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./iuh-20072261-firebase-adminsdk-vsfs1-6e59502f60.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-20072261').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df['YEAR_ID'] = df['YEAR_ID'].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")
df["PROFIT"] = df["SALES"]-(df["QUANTITYORDERED"]*df["PRICEEACH"])

app = Dash(__name__)
server = app.server

app.title = "Xây dựng danh mục sản phẩm tìm năng"

# Doanh so
doanhSoSale = round(sum(df['SALES']),2)

# Loi nhuan
loiNhuan = round(sum(df['PROFIT']),2)


# Top doanh so
topDoanhSo = df.groupby(['CATEGORY'])['SALES'].sum().max()

# Top Loi Nhuan
topLoiNhuan = df.groupby(['CATEGORY'])['PROFIT'].sum().max()


# doanh thu theo năm
figDoanhSo = px.histogram(df, x="YEAR_ID", y="SALES", 
barmode="group", color="YEAR_ID", title='Doanh số bán hàng theo năm', histfunc = "sum",
labels={'YEAR_ID':'Từ năm 2003, 2004 và 2005', 'SALES':'Doanh số'})
# doanh số theo danh mục trong năm
figDoanhSoTheoDanhMucTheoNam = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
color='SALES',
labels={'parent':'Năm', 'labels':'Danh mục','SALES':'Doanh số'},
title='Tỉ lệ đóng góp của doanh số theo từng danh mục trong từng năm')
                   
listLoiNhuan = df.groupby(['YEAR_ID'])['PROFIT'].agg(['sum'])
dfGroup = df.groupby('YEAR_ID').sum('SALES')
dfGroup = dfGroup.reset_index()
#lợi nhuận theo năm
figLoiNhuanTheoNam = px.line(
    dfGroup, x='YEAR_ID', y='PROFIT', title='Lợi nhuận bán hàng theo năm')


# lợi nhuận theo danh mục trong năm
figLoiNhuanTheoDanhMucTheoNam = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='PROFIT',
color='PROFIT',
labels={'parent':'Năm', 'labels':'Danh mục','PROFIT':'Lợi nhuận'},
title='Tỉ lệ đóng góp của lợi nhuận theo từng danh mục trong từng năm')


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3(
                    "XÂY DỰNG DANH MỤC SẢN PHẨM TIỀM NĂNG", className="header-title"
                ),
                html.H4(
                    "IUH-DHKTPM16A-20072261-Trần Bảo Trúc", className="header-title"
                )
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=html.Div(
                        children=[
                            html.H4(
                                "DOANH SỐ SALE",
                            ),
                            "{}".format(doanhSoSale) + " $"
                        ],
                        className="label"
                    ), className="card c1"
                ),
                html.Div(
                    children=html.Div(
                        children=[
                            html.H4(
                                "LỢI NHUẬN",
                            ),
                            "{}".format(loiNhuan) + " $"
                        ],
                        className="label"
                    ), className="card c1"
                ),
                html.Div(
                    children=html.Div(
                        children=[
                            html.H4(
                                "TOP DOANH SỐ",
                            ),
                            "{}".format(topDoanhSo) + " $"
                        ],
                        className="label"
                    ), className="card c1"
                ),
                html.Div(
                    children=html.Div(
                        children=[
                            html.H4(
                                "TOP LỢI NHUẬN",
                            ),
                            "{}".format(topLoiNhuan) + " $"
                        ],
                        className="label"
                    ), className="card c1"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=figDoanhSo,
                        className="hist"
                    ), className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=figDoanhSoTheoDanhMucTheoNam,
                        className="hist"
                    ), className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=figLoiNhuanTheoNam,
                        className="hist"
                    ), className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=figLoiNhuanTheoDanhMucTheoNam,
                        className="hist"
                    ), className="card c2"
                )
            ], className="wrapper"
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8070)
