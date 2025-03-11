from fastapi import FastAPI, HTTPException
from dto import DagDTO, NodeDTO, EdgeDTO
from db import repo
from db.models import Node, NodeType, Edge

app = FastAPI()

@app.get("/dags", response_model=list[DagDTO])
async def get_dags() -> list[DagDTO]:
    dags = await repo.RepoDag.select_dags()
    return dags

@app.get("/dags/{dag_id}", response_model=DagDTO)
async def get_dag_by_id(dag_id: int) -> DagDTO:
    dag = await repo.RepoDag.select_dag_by_id(dag_id)
    if not dag:
        raise HTTPException(status_code=404, detail="DAG not found")
    return dag

@app.post("/dags", response_model=DagDTO)
async def new_dag(dag: DagDTO) -> DagDTO: 
    dag = await repo.RepoDag.add_dag(dag)
    return dag

@app.delete("/dags/{dag_id}")
async def delete_dag(dag_id: int):
    dag = await repo.RepoDag.select_dag_by_id(dag_id)
    if not dag:
        raise HTTPException(status_code=404, detail="DAG not found")
    await repo.RepoDag.del_dag(dag)

@app.delete("/dags")
async def delete_all_dags():
    await repo.RepoDag.del_dags_all()

@app.get("/nodes/{node_id}", response_model=NodeDTO)
async def get_node_by_id(node_id: int) -> NodeDTO:
    node = await repo.RepoNode.select_node_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@app.get("/nodes", response_model=list[NodeDTO])
async def get_nodes() -> list[NodeDTO]:
    nodes = await repo.RepoNode.select_nodes()
    return nodes

@app.post("/nodes", response_model=NodeDTO)
async def create_node(node: NodeDTO) -> NodeDTO:
    db_node = Node(
        name=node.name,
        node_type=NodeType(node.node_type)
    )
    db_node = await repo.RepoNode.add_node(db_node)
    return db_node

@app.put("/nodes/{node_id}", response_model=NodeDTO)
async def update_node(node_id: int, node: NodeDTO) -> NodeDTO:
    db_node = await repo.RepoNode.select_node_by_id(node_id)
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    db_node.name = node.name
    db_node.node_type = NodeType(node.node_type)
    
    db_node = await repo.RepoNode.update_node(db_node)
    return db_node

@app.delete("/nodes/{node_id}")
async def delete_node(node_id: int):
    node = await repo.RepoNode.select_node_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    await repo.RepoNode.delete_node_with_edges(node)

@app.post("/edges", response_model=EdgeDTO)
async def create_edge(edge: EdgeDTO) -> EdgeDTO:
    # Проверяем существование узлов
    left_node = await repo.RepoNode.select_node_by_id(edge.left_id)
    right_node = await repo.RepoNode.select_node_by_id(edge.right_id)
    
    if not left_node or not right_node:
        raise HTTPException(status_code=404, detail="One or both nodes not found")
        
    db_edge = Edge(
        left_id=edge.left_id,
        right_id=edge.right_id,
        shift=edge.shift
    )
    db_edge = await repo.RepoEdge.add_edge(db_edge)
    return db_edge

@app.delete("/edges/{left_id}/{right_id}")
async def delete_edge(left_id: int, right_id: int):
    await repo.RepoEdge.delete_edge(left_id, right_id)