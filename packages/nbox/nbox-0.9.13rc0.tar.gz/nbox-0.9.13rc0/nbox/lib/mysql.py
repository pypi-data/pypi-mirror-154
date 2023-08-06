import pandas as pd
from sqlalchemy import create_engine

db_name = "nimblebox_revamp"

engine = create_engine(f"mysql+pymysql://root:Nimblebox666123@127.0.0.1:3306/{db_name}",echo=True)

conn = engine.connect()
curr = conn.connection.cursor()

df = pd.read_sql('''select
	j.id as job_id,
	jl.created_time,
	r.id as run_id,
	r.dag, r.end_time, jl.action
from jobs j
	inner join runs r on r.job_id = j.id
	inner join job_log jl on jl.job_id = j.id
where
	j.dag != "UNSET" and
	r.dag != "NOT_SET" and
	r.dag != "{}" and
	jl.action = "RESOURCES_CREATED"
order by j.id, jl.created_time''', engine)

print(df)

conn.close()