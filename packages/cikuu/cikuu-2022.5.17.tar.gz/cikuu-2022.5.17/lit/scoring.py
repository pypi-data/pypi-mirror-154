# 2022.6.8
from common import *

def run():
	tid = st.experimental_get_query_params().get('tid', ['scoring-0'])[0]
	st.title(hget(f"config:rid-{rid}:tid-{tid}","title", "Scoring")) 
	st.caption(hget(f"config:rid-{rid}:tid-{tid}","subtitle")) 

	score = st.number_input('Input a score', min_value=0, max_value=100,step=1, value=int(hget(f"rid-{rid}:tid-{tid}:uid-{uid}","score", 60)))
	if st.button("submit") : 
		redis.r.hset(f"rid-{rid}:tid-{tid}:uid-{uid}","score", score, {"rid": rid, "tid": tid,"uid": uid, "type":"scoring"} )
		st.metric("SCORE", score )

if __name__ == '__main__': run()
