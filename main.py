# import tabula
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
# # reading pdf file into dataframe
# df = tabula.read_pdf('x1.pdf')
# dataframe = pd.DataFrame(df[0])

# # extracting important columns and rows
# dataframe.columns = dataframe.iloc[3]
# dataframe = dataframe.iloc[6:, :]
# important_data = dataframe[['Date', '#Rooms', 'Net Room Rev']]
# for _, data in important_data.iterrows():
#     date = data['Date']
#     print(date)
#     print(date)
#     rooms = data['#Rooms']
#     netrev = data['Net Room Rev'].replace(',', '')

import pymysql.cursors
connection = pymysql.connect(host="localhost", user="root", password="", cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
cursor.execute(f"use website")
cursor.execute(f"select pid, prooms from properties inner join user on properties.uid = user.uid where user.uemail = \"hamza.abuzahra@bilgiedu.net\" and pname=\"AC Hotel\"")
result = cursor.fetchall()
pid = result[0]['pid']
prooms = result[0]['prooms']
cursor.execute(f"select * from records where (pid=3 and rdate <= \'2015-01-31\' and rdate >= \'2015-01-01\') order by rdate asc")
data = cursor.fetchall()
df = pd.DataFrame(data)
df = df[['rdate', 'rrooms', 'rrevenue']]
df['rrevenue'] = round(pd.to_numeric(df['rrevenue']) / df['rrooms'], 2)
df['rrooms'] = round(df['rrooms'] / prooms * 100, 2)
df['rrevpar'] = round(df['rrooms'] * df['rrevenue'] / 100, 2)
df.plot(x='rdate', y='rrooms')
df.plot(x='rdate', y='rrevenue')
df.plot(x='rdate', y='rrevpar')


writer = pd.ExcelWriter("technical.xlsx", engine='xlsxwriter', date_format = 'yyyy-mm-dd', datetime_format='yyyy-mm-dd')
workbook = writer.book
 
# # Create a format for a green cell
# green_cell = workbook.add_format({
#     'bg_color': '#C6EFCE',
#     'font_color': '#006100'
# })
# # Create a format for a red cell
# red_cell = workbook.add_format({
#     'bg_color': '#FFC7CE',                            
#     'font_color': '#9C0006'
# })
 
# **
# ** Occuapncy + ADR + RevPAR
# **
sheet_name = 'All'
df[['rdate', 'rrooms', 'rrevenue', 'rrevpar']].to_excel(writer, sheet_name=sheet_name)
worksheet = writer.sheets[sheet_name]
 
# Set column width of Date
worksheet.set_column(1, 1, 10)
 
 
# for col in range(1, 3):
#     # Create a conditional formatted of type formula
#     worksheet.conditional_format(1, col, len(data), col, {
#         'type': 'formula',                                    
#         'criteria': '=B2>=C2',
#         'format': green_cell
#     })
 
#     # Create a conditional formatted of type formula
#     worksheet.conditional_format(1, col, len(data), col, {
#         'type': 'formula',                                    
#         'criteria': '=B2<C2',
#         'format': red_cell
#     })
 
 
# Create a new chart object.
chart1 = workbook.add_chart({'type': 'line'})
 
# Add a series to the chart.
chart1.add_series({
        'name': 'Occupancy',
        'categories': [sheet_name, 1, 1, len(df), 1],
        'values': [sheet_name, 1, 2, len(df), 2],
})
 
# Create a new chart object.
chart2 = workbook.add_chart({'type': 'line'})
 
# Add a series to the chart.
chart2.add_series({
        'name': "ADR",
        'categories': [sheet_name, 1, 1, len(data), 1],
        'values': [sheet_name, 1, 3, len(data), 3],
})

chart3 = workbook.add_chart({'type': 'line'})
 
# Add a series to the chart.
chart3.add_series({
        'name': "RevPAR",
        'categories': [sheet_name, 1, 1, len(data), 1],
        'values': [sheet_name, 1, 4, len(data), 4],
})
# # Combine and insert title, axis names
# chart1.combine(chart2)
# chart1.set_title({'name': sheet_name + " AAPL"})
# chart1.set_x_axis({'name': 'Date'})
# chart1.set_y_axis({'name': 'Price'})
 
# Insert the chart into the worksheet.
worksheet.insert_chart('G2', chart1)
worksheet.insert_chart('G20', chart2)
worksheet.insert_chart('O2', chart3)

writer.close()