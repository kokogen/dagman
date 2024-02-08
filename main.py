import asyncio
from db.repo import RepoDag
import db.sessions
import db.models

async def main():
    print('dagman started.')
    
    await RepoDag.del_dags_all()
    
    dag = db.models.Dag(name='first dag', params=['a', 'b'])
    print(dag)
    
    dag = await RepoDag.add_dag(dag)
    print(dag)
    
    r = await RepoDag.select_dags()
    print(r)
    
    print('dagman finished')
    

if __name__ == '__main__':
    asyncio.run(main())
        