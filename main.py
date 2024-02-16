import asyncio
from db.repo import RepoDag, RepoNode
import db.sessions
import db.models


async def main():
    print('dagman started.')
    
    lst = await RepoDag.select_dags()
    print(lst)
    
    #await RepoDag.del_dags_all()
    
    # node1 = db.models.Node(name='node1', node_type=db.models.NodeType.DAG_OP)
    # dag = db.models.Dag(name='first dag', params=['a', 'b'])
    # dag_operation1 = db.models.DagOperation(dag=dag, node=node1, step=1, params = [])
    # print(dag)
    
    # dag = await RepoDag.add_dag(dag)
    # print(dag)
    
    # r = await RepoDag.select_dags()
    # print(r)
    
    # node = await RepoNode.select_node_by_id(7)
    # dag = node.operation.dag
    # print(node)
    
    print('dagman finished')
    
if __name__ == '__main__':
    asyncio.run(main())
        