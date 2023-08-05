'''
This is the torch code 
'''

import torch
from pytorch3d.ops import knn_points

def query(q_pts:torch.tensor, verts:torch.tensor, tets:torch.tensor, indexes:torch.tensor, K=4) -> tuple:
    tet_verts = verts[tets]  # [NT,4,3]
    tet_verts_center = tet_verts.mean(dim=1)  # [NT,3]

    knn_res = knn_points(q_pts.unsqueeze(0), tet_verts_center.unsqueeze(0), K=K)
    neighbor_idx = knn_res.idx[0]  # [Nq, K], the closest tet center to the query points
    neighbor_tets = tet_verts[neighbor_idx]  # [Nq,K,4,3]

    ##### TODO include the tetrehedra that containing the nearest vertex of query point
    
    ### start calculation. 
    det_verts = torch.cat([q_pts[:,None,None,:].expand(-1,K,-1,-1), neighbor_tets], dim=2)  # [Nq,K,5,3]
    # print("det_verts:", det_verts)
    ### Need to calculate 5 determinants for barycentric calculation
    det_verts = det_verts[:,:,None,:,:].expand(-1,-1,5,-1,-1)  # [Nq,K,5,5,3]
    indexes_shape = det_verts.shape[:2] + indexes.shape
    indexes = indexes[None,None,...].expand(*indexes_shape)  # [Nq,K,5,4,3]
    dets = torch.gather(det_verts, index=indexes, dim=3)  # [Nq,K,5,4,3]
    dets = torch.cat([dets, torch.ones_like(dets[...,:1])], dim=-1)  # [Nq,K,5,4,4]

    dets_val = torch.linalg.det(dets)  # [Nq,K,5]

    uvwz = dets_val[...,1:] / (dets_val[...,0:1] + 1e-9) # [Nq,K,4]
    u, v, w, z = uvwz[...,0], uvwz[...,1], uvwz[...,2], uvwz[...,3] # [Nq,K]
    in_tet_mask = torch.logical_and(u > 0, v > 0)
    in_tet_mask = torch.logical_and(in_tet_mask, w > 0)
    in_tet_mask = torch.logical_and(in_tet_mask, z > 0) # [Nq,K]

    in_tet_mask = torch.cat([in_tet_mask.int(), torch.ones_like(in_tet_mask[:,:1])], dim=-1) # [Nq,K+1]
    tet_idx = torch.argmax(in_tet_mask, dim=1) # [Nq,]
    uvwz = torch.cat([uvwz, torch.zeros_like(uvwz[:,:1,:])], dim=1)  # [Nq,K+1,4]
    # if not contained in any tets, set index and barys to -1, [0,0,0,0]
    barycentric = torch.gather(uvwz, dim=1, index=tet_idx[:,None,None].expand(-1,1,4)).permute(0,2,1)  # [Nq,4,1]

    ### tet_idx is the in local index in the K tets. Need to change to global index
    neighbor_idx = torch.cat([neighbor_idx, -1 * torch.ones_like(neighbor_idx[:,:1])], dim=1)  # [Nq,K+1]
    tet_idx = torch.gather(neighbor_idx, index=tet_idx[:,None], dim=1)  # [Nq, 1]
    return tet_idx.squeeze(-1), barycentric.squeeze(-1)