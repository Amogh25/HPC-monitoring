import json
import os
data=json.load(open('Node Exporter Full-1679649658993.json'))
dashboard_name="node-exporter-full"
gauge_list=[]
time_series_list=[]
stat_list=[]
inner_panel_list=[]
for panel in data['panels']:

    if panel['type']=="gauge":
        title = panel['title']
        id = str(panel['id'])
        url="http://localhost:3000/d/rYdddlPW/"+ dashboard_name +"?orgId=1&editPanel="+id+"&inspect="+id
        gauge_list.append(title)
    if panel['type']=="timeseries":
        title = panel['title']
        id = str(panel['id'])
        url="http://localhost:3000/d/rYdddlPW/"+ dashboard_name +"?orgId=1&editPanel="+id+"&inspect="+id
        time_series_list.append(title)
    if panel['type']=="stat":
        title = panel['title']
        id = str(panel['id'])
        url="http://localhost:3000/d/rYdddlPW/"+ dashboard_name +"?orgId=1&editPanel="+id+"&inspect="+id
        stat_list.append(title)

    if panel.get('panels',0) != 0:
        for pan in panel['panels']:
            if pan['type']=="gauge":
                title = pan['title']
                id = str(pan['id'])
                url="http://localhost:3000/d/rYdddlPW/"+ dashboard_name +"?orgId=1&editPanel="+id+"&inspect="+id
                gauge_list.append(title)
            if pan['type']=="timeseries":
                title = pan['title']
                id = str(pan['id'])
                url="http://localhost:3000/d/rYdddlPW/"+ dashboard_name +"?orgId=1&editPanel="+id+"&inspect="+id
                time_series_list.append(title)
            if pan['type']=="stat":
                title = pan['title']
                id = str(pan['id'])
                url="http://localhost:3000/d/rYdddlPW/"+ dashboard_name +"?orgId=1&editPanel="+id+"&inspect="+id
                stat_list.append(title)
            

print(gauge_list)
print(time_series_list)
print(stat_list)