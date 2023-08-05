import torch
from query_cpp import query

def genIndex(use_cuda=True) -> torch.tensor:
    indexes = []
    index = torch.tensor([[1,2,3,4]],dtype=torch.long).T.expand(4,3)
    indexes.append(index.unsqueeze(0))
    index = torch.tensor([[0,2,3,4]],dtype=torch.long).T.expand(4,3)
    indexes.append(index.unsqueeze(0))
    index = torch.tensor([[1,0,3,4]],dtype=torch.long).T.expand(4,3)
    indexes.append(index.unsqueeze(0))
    index = torch.tensor([[1,2,0,4]],dtype=torch.long).T.expand(4,3)
    indexes.append(index.unsqueeze(0))
    index = torch.tensor([[1,2,3,0]],dtype=torch.long).T.expand(4,3)
    indexes.append(index.unsqueeze(0))
    indexes = torch.cat(indexes, dim=0) # [5,4,3]
    if use_cuda:
        indexes = indexes.cuda()
    return indexes


def cal_barycentric(q_pts:torch.tensor, verts:torch.tensor, tets:torch.tensor, K=4, use_cuda=True):
    """_summary_

    Args:
        q_pts (torch.tensor): the query points, [Nq,3]
        verts (torch.tensor): the vertices tethedra, [NV,3]
        tets (torch.tensor): the vertex index of each tet, [NT,4]
        K (int): the nearest neighbors for searching to accelerate query
        use_cuda (bool, optional): _description_. Defaults to True.

    Returns:
        tuple: the tet_idx and corresponding barycentric coordinates
    """
    if use_cuda:
        q_pts, verts, tets = q_pts.cuda(), verts.cuda(), tets.cuda()
    indexes = genIndex(use_cuda=use_cuda)
    res = query(q_pts, verts, tets, indexes, 4)
    return res
