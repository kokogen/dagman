from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class EdgeDTO(BaseModel):
    left_id: int
    right_id: int
    shift: int
    
    model_config = ConfigDict(from_attributes=True)
           
    
class NodeDTO(BaseModel):
    id: int
    name: str
    node_type: str
    operation: Optional['DagOperationDTO']
    dataversion: Optional['DataVersion']
    
    left_edges: List['EdgeDTO']
    right_edges: List['EdgeDTO']
    
    model_config = ConfigDict(from_attributes=True)

    
class DagDTO(BaseModel):
    id: int
    name: str
    params: List[str]
    
    model_config = ConfigDict(from_attributes=True)

    
class DagOperationDTO(BaseModel):
    node_id: int
    dag: DagDTO
    step: int
    params: List[str]
    
    model_config = ConfigDict(from_attributes=True)

    
class DataVersion(BaseModel):
    node_id: int
    entity_name: str
    
    model_config = ConfigDict(from_attributes=True)

    
    

