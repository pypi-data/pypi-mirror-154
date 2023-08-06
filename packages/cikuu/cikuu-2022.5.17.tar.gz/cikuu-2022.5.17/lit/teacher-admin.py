# 2022.6.8
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(layout='wide')
from common import * 

st.sidebar.header( hget(f"config:rid-{rid}", "title","i+1 写作智慧课堂") )
radios = json.loads(hget(f"config:rid-{rid}","radios","{}"))
item = st.sidebar.radio('',[k for k in radios.keys()]) # {"连词成句":"reorder", "句式升级":"essay", "按句润色":"sntspolish"}
st.sidebar.markdown('''---''') 

app_state['tid'] = radios[item]
x = __import__(radios[item].split('-')[0], fromlist=['run'])
x.run()
url = st.sidebar.text_input("input", "http://www.penly.cn:3000/public/dashboard/8e5329fc-6df2-4e5a-a827-79877da1ce73") 
components.iframe(url,  height = 1200) #width=1500,