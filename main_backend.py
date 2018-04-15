
# coding: utf-8

# In[1]:


def main_proc():
    print ('Loading...')
    import pandas as pd
    import numpy as np
    import folium
    from folium import IFrame
    import base64
    import datetime
    from geojson import Feature, Polygon, FeatureCollection
    from IPython.display import display
    from branca.colormap import linear
    import branca.colormap as cm
    from ipywidgets import widgets
    from IPython.core.display import HTML
    from IPython.display import clear_output
    import calendar
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go
    plotly.offline.init_notebook_mode()
    from plotly.offline import iplot
    from plotly import tools

    data1 = pd.read_csv('06_2015.csv',  index_col=[0], parse_dates=[0])
    data2 = pd.read_csv('07_2015.csv',  index_col=[0], parse_dates=[0])
    data3 = pd.read_csv('08_2015.csv',  index_col=[0], parse_dates=[0])
    data4 = pd.read_csv('09_2015.csv',  index_col=[0], parse_dates=[0])
    data5 = pd.read_csv('10_2015.csv',  index_col=[0], parse_dates=[0])
    data6 = pd.read_csv('11_2015.csv',  index_col=[0], parse_dates=[0])
    data7 = pd.read_csv('12_2015.csv',  index_col=[0], parse_dates=[0])
    data8 = pd.read_csv('01_2016.csv',  index_col=[0], parse_dates=[0])
    data9 = pd.read_csv('02_2016.csv',  index_col=[0], parse_dates=[0])
    data10 = pd.read_csv('03_2016.csv',  index_col=[0], parse_dates=[0])
    data11 = pd.read_csv('04_2016.csv',  index_col=[0], parse_dates=[0])
    data12 = pd.read_csv('05_2016.csv',  index_col=[0], parse_dates=[0])
    data13 = pd.read_csv('06_2016.csv',  index_col=[0], parse_dates=[0])

    data = data1
    data = data.append(data2).append(data3).append(data4).append(data5).append(data6).append(data7).append(data8).append(data9).append(data10).append(data11).append(data12).append(data13)
    data.columns = data.columns.map(int)

    regions = np.array([1075, 1076, 1077, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132,
       1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182,
       1183, 1184, 1221, 1222, 1223, 1224, 1225, 1227, 1228, 1229, 1230,
       1231, 1232, 1233, 1234, 1235, 1272, 1273, 1274, 1278, 1279, 1280,
       1281, 1282, 1283, 1284, 1285, 1286, 1287, 1326, 1327, 1331, 1332,
       1333, 1334, 1335, 1336, 1337, 1338, 1339, 1376, 1377, 1378, 1380,
       1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1426, 1431,
       1434, 1435, 1436, 1437, 1438, 1439, 1441, 1442, 1480, 1482, 1483,
       1530, 1532, 1533, 1580, 1630, 1684, 1733, 1734, 1783, 2068, 2069,
       2118, 2119, 2168])

    data_target = data[regions]
    regions_data = pd.read_csv('regions.csv', delimiter=';')

    PREDICTIONS = []
    for i in range(1,7,1):
        PREDICTIONS.append(pd.read_csv('predict_'+str(i) + '.csv',  index_col=[0], parse_dates=[0]))
        PREDICTIONS[i-1].columns = PREDICTIONS[0].columns.map(int)

    from sklearn.cluster import KMeans
    data_target_normal=(data_target-data_target.mean())/data_target.std()
    data_target_trans = np.array(data_target_normal.transpose())
    
    
    fk = []
    for regnum in regions:
        rowRD = regions_data[regions_data.region == regnum ]
        temp = [[(rowRD.west.values[0],rowRD.south.values[0]),(rowRD.west.values[0],rowRD.north.values[0]),
             (rowRD.east.values[0],rowRD.north.values[0]),(rowRD.east.values[0],rowRD.south.values[0]),
             (rowRD.west.values[0],rowRD.south.values[0])]]

        my_feature = Feature(geometry=Polygon(temp), id = int(rowRD.region.values[0]))
        fk.append(my_feature)
        
    feature_collection = FeatureCollection(fk)
    
    fg_popup = folium.FeatureGroup(name = 'Regions Name')


    for item in range(0,len(feature_collection['features'])):
        folium.GeoJson(
            feature_collection[item],
            style_function=lambda feature: {
            'fillColor': '#FF000000',
            'fillOpacity': 0.4,
            'color': 'gray',
            'weight': 0.15,
            }
        ).add_child(folium.Popup(str(regions[item]))).add_to(fg_popup)
    

    clear_output()        
    print ('Done')
    
    
    
    def naturalMap(date):
        lon, lat = -73.985901, 40.768040
        zoom_start = 10

        m = folium.Map(location=[lat, lon], tiles='Cartodb dark_matter', zoom_start=zoom_start)
        
        

        meanOfCurrentDate = data_target.loc[date,:].mean()
        colormap = cm.LinearColormap(colors=['lime','red'],
                                     index=[0,meanOfCurrentDate.max() - meanOfCurrentDate.max()/3],
                                     vmin=meanOfCurrentDate.min(),vmax=meanOfCurrentDate.max())
        colors_dict = pd.DataFrame(meanOfCurrentDate)
        colors_dict['id'] = regions
        colors_dict = colors_dict.set_index('id')[0]
        


        fg = folium.FeatureGroup(name = 'Natural')
        

        folium.GeoJson(
            feature_collection,
            style_function=lambda feature: {
            'fillColor': colormap(colors_dict[feature['id']]),
            'fillOpacity': 0.4,
            'color': 'gray',
            'weight': 0.15,
            'reset': True, 
            }
        ).add_to(fg)



        meanOfCurrentDate_p = PREDICTIONS[0].loc[date,:].mean()
        colormap = cm.LinearColormap(colors=['lime','red'],
                                     index=[0,meanOfCurrentDate_p.max() - meanOfCurrentDate_p.max()/3],
                                     vmin=meanOfCurrentDate_p.min(),vmax=meanOfCurrentDate_p.max())
        colors_dict_p = pd.DataFrame(meanOfCurrentDate_p)
        colors_dict_p['id'] = regions
        colors_dict_p = colors_dict_p.set_index('id')[0]


        fg2 = folium.FeatureGroup(name = 'Predicted')

        folium.GeoJson( 
            feature_collection,
            style_function=lambda feature: {
            'fillColor': colormap(colors_dict_p[feature['id']]),
            'fillOpacity': 0.4,
            'color': 'gray',
            'weight': 0.15,
            'reset': True, 
            }
        ).add_to(fg2)

        m.add_child(fg)
        m.add_child(fg2)
        m.add_child(fg_popup)
        
        lc = folium.LayerControl()
        m.add_child(lc)



        colormap.caption = 'Averege taxi orders per day color scale'
        colormap.add_to(m)



        display(m)
    
    def wid_ShowMap():
        foot_text_wid = widgets.HTML(value=u"Ниже ползунком укажите день, данные которого необходмо отобразить:")
        button_wid = widgets.Button(description="Show")
        currentDate = [1]
        weekdayNames = list(calendar.day_name)

        def handler(sender):
            clear_output()
            curDateStr = '2016-06-' + str(currentDate[0])
            timew = pd.Timestamp(curDateStr)    
            display(foot_text_wid, slider_wid,button_wid)
            print(curDateStr)
            print(weekdayNames[timew.weekday()])


            naturalMap(curDateStr)

        def f(x=1):
            currentDate[0] = x

        slider_wid = widgets.interactive(f, x=(1,30,1))
        button_wid.on_click(lambda x: handler(x))    
        display(foot_text_wid,slider_wid,button_wid)
    
    def ShowPlot(from_date, tovalue_date, region, isPredAlso, pred_hour):
        _x = data_target.loc[from_date:tovalue_date,region].index.tolist()
        _y = data_target.loc[from_date:tovalue_date,region].values

        trace0 = go.Scatter(
            x = _x,
            y = _y,
            name='Natural Values'
        )
        trace1 = go.Scatter()
        if (isPredAlso):
            trace1 = go.Scatter(
            x = PREDICTIONS[pred_hour-1].loc[from_date:tovalue_date,region].index.tolist(),
            y = PREDICTIONS[pred_hour-1].loc[from_date:tovalue_date,region].values,
            name='Predicted Values'
            )

        data_sh = ([trace0, trace1])
        iplot(data_sh)
        
    def dateCheker(date1, date2):
        if(date1.year == 2016 and date1.month==6 and date1<date2):
            return True   

    def print_meanError(from_date, tovalue_date, region, pred_hour):        
        print("Средняя ошибка: %f" %abs((data_target.loc[from_date:tovalue_date,region] - PREDICTIONS[pred_hour-1].loc[from_date:tovalue_date,region])).mean())
    def wid_ShowPlot():
        foot_text_wid = widgets.HTML(value=u"Введите даты, в пределах июня 2016 года. Для графика предсказаний поставьте галочку и укажите на который час от текущего сделать прогноз (от 1 до 6)")
        from_date_wid = widgets.Text("2016-06-01 00:00:00", description="Begin Date")
        to_date_wid  = widgets.Text("2016-06-30 23:00:00", description="End Date")
        region_wid = widgets.Text('1075', description="Region")
        button_wid = widgets.Button(description="Show")
        isPred_wid = widgets.Checkbox(value=False, description='Show prediction', disabled=False)
        pred_hours_wid  = widgets.Text("1", description="Pred hours")
        pred_hours_wid.disabled = True

        def handler(sender):
            try:
                tmpst_1 = pd.to_datetime(from_date_wid.value)
                tmpst_2 = pd.to_datetime(to_date_wid.value)
                clear_output()
                display(foot_text_wid,from_date_wid,to_date_wid, region_wid, button_wid, isPred_wid, pred_hours_wid)
                if(dateCheker(tmpst_1, tmpst_2)):
                    if(isPred_wid.value == False):
                        ShowPlot(from_date_wid.value, to_date_wid.value, int(region_wid.value),isPred_wid.value, int(pred_hours_wid.value))                        
                    else:
                        if(int(pred_hours_wid.value)>0 and int(pred_hours_wid.value)<7):
                            ShowPlot(from_date_wid.value, to_date_wid.value, int(region_wid.value),isPred_wid.value, int(pred_hours_wid.value))
                            print_meanError(from_date_wid.value, to_date_wid.value, int(region_wid.value), int(pred_hours_wid.value))
                        else:
                            print("Something wrong. Apparently, you set wrong prediction hour")
                else:
                    print("Something wrong. Apparently, you set wrong time range")
            except:
                 print("Something wrong. Apparently, you set wrong time range")

        def handler2(sender):
            if(isPred_wid.value == True):
                pred_hours_wid.disabled = False
            else:
                pred_hours_wid.disabled = True

        button_wid.on_click(lambda x: handler(x))
        isPred_wid.observe(lambda x: handler2(x))
        display(foot_text_wid,from_date_wid,to_date_wid, region_wid, button_wid, isPred_wid, pred_hours_wid)
       
    
    def ShowMap_clust(Nclust):
        model = KMeans(n_clusters=Nclust, random_state=1)
        clusts = model.fit_predict(data_target_trans)
        data_clustered = pd.DataFrame(regions, columns=['id'])
        data_clustered['cluster'] = clusts

        lon, lat = -73.985901, 40.768040
        zoom_start = 10

        m = folium.Map(location=[lat, lon], tiles='Cartodb dark_matter', zoom_start=zoom_start)


        colormap = cm.LinearColormap(colors=['lime','gold','red'],
                                     vmin=0,vmax=Nclust - 1)

        colors_dict = data_clustered
        colors_dict = colors_dict.set_index('id')        

        fg = folium.FeatureGroup(name = 'Natural')

        folium.GeoJson(
            feature_collection,
            style_function=lambda feature: {
            'fillColor': colormap(colors_dict.loc[feature['id']][0]),
            'fillOpacity': 0.6,
            'color': 'gray',
            'weight': 0.15,
            'reset': True, 
            }
        ).add_to(fg)


        m.add_child(fg)
        m.add_child(fg_popup)
        lc = folium.LayerControl()
        m.add_child(lc)



        colormap.caption = 'Averege taxi orders per hour color scale'
        colormap.add_to(m)



        display(m)
        
    def wid_ShowMap_clust():
        foot_text_wid = widgets.HTML(value=u"Введите количество кластеров: ")
        clust_wid = widgets.Text("4", description="Clusters")
        button_wid = widgets.Button(description="Show")

        def handler(sender):
            clear_output()
            display(foot_text_wid, clust_wid, button_wid)
            try:           
                 ShowMap_clust(int(clust_wid.value))
            except:
                 print("Something wrong. Apparently, you set wrong clusters number")



        button_wid.on_click(lambda x: handler(x))
        display(foot_text_wid, clust_wid, button_wid)
        
    return (wid_ShowMap,wid_ShowPlot,wid_ShowMap_clust)


