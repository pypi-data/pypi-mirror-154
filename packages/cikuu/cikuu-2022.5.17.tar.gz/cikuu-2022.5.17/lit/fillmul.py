# 2022.6.8  fillmul (cross multiple words, ... ) 
from common import * 

def run():

	tid = st.experimental_get_query_params().get('tid', ['fillmul'])[0]
	st.title(hget(f"config:rid-{rid}:tid-{tid}","title", "好词好句")) 
	st.caption(hget(f"config:rid-{rid}:tid-{tid}","subtitle")) 

	labels = [ k.split(":")[-1].strip() for k in redis.r.hkeys(f"rid-{rid}:tid-{tid}:uid-{uid}") if k.startswith("label:")]
	#st.sidebar.write(f"submitted: {len(labels)}")
	#checked = [ st.sidebar.checkbox(label) for label in labels] #agree = st.checkbox('I agree')
	st.sidebar.write(labels)

	labels= st.text_input( f"New word:", hget(f"rid-{rid}:tid-{tid}:uid-{uid}", "label") )
	if st.button("submit") and labels: 
		redis.r.hset(f"rid-{rid}:tid-{tid}:uid-{uid}", f"label:{newword}" , newword, {"rid": rid, "tid": tid,"uid": uid, "type":"fillmul"} )
		st.metric("TOTAL", len([ k for k in redis.r.hkeys(f"rid-{rid}:tid-{tid}:uid-{uid}") if k.startswith("label:")]) )

if __name__ == '__main__': run()

# select trimBoth(arrayJoin (splitByChar (',', '123,456, 142354 ,23543') )) 