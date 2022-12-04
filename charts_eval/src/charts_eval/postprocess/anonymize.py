
import charts_eval.evaluation.tools as tools

def anonimize_data(charts_db):
    new_db=[]
    keys=charts_db.getKeys()
    
    for key in keys:
        chart_info={}
        for tool in tools.tools_list:
            if tool in charts_db[key]:
                chart_info[tool] = charts_db[key][tool]
        new_db.append(chart_info)
    
    return new_db
