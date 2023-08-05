#include<ATen/ATen.h>
#include<torch/extension.h>
#include<iostream>

using namespace torch::indexing;

std::tuple<at::Tensor, at::Tensor> KNearestNeighborIdxCuda(
     const at::Tensor& p1,
     const at::Tensor& p2,
     const at::Tensor& lengths1,
     const at::Tensor& lengths2,
     const int norm,
     const int K,
     int version
);

std::tuple<at::Tensor, at::Tensor> query_cpp(
    at::Tensor& q_pts,
    at::Tensor& verts,
    at::Tensor& tets,
    at::Tensor& indexes,
    int K = 4
) {
    at::Tensor tet_verts = verts.index(tets);  // [NT,4,3]
    at::Tensor tet_verts_center = tet_verts.mean(1);  // [NT,3]

    at::Tensor lengths1 = torch::tensor({q_pts.size(0)}).to(torch::kLong).to(q_pts.device());  // [1,]
    at::Tensor lengths2 = torch::tensor({tet_verts_center.size(0)}).to(torch::kLong).to(tet_verts_center.device());  // [1,]

    std::tuple<at::Tensor, at::Tensor> res = 
    KNearestNeighborIdxCuda(q_pts.unsqueeze(0), tet_verts_center.unsqueeze(0), lengths1, lengths2, 2, K, -1);

    at::Tensor neighbor_idx = std::get<0>(res)[0];  // [Nq,K]
    at::Tensor neighbor_tets = tet_verts.index(neighbor_idx);  // [Nq,K,4,3]

    // start calculation
    at::Tensor det_verts = torch::cat({q_pts.unsqueeze(1).unsqueeze(2).expand({-1,K,-1,-1}), neighbor_tets}, 2);  // [Nq,K,5,3]
    // Need to calculate 5 determinants for barycentric calculation
    det_verts = det_verts.unsqueeze(2).expand({-1,-1,5,-1,-1});  // [Nq,K,5,5,3]
    int Nq = det_verts.size(0);
    indexes = indexes.unsqueeze(0).unsqueeze(0).expand({Nq,K,5,4,3});  // [Nq,K,5,4,3]
    at::Tensor dets = torch::gather(det_verts, 3, indexes);  // [Nq,K,5,4,3]
    dets = torch::cat({dets, torch::ones_like(dets.index({"...",Slice(None,1)}))}, 4);  // [Nq,K,5,4,4]

    at::Tensor dets_val = torch::linalg_det(dets);  // [Nq,K,5]
    
    /***********  This line can be accelerated with CUDA  ***********/
    at::Tensor uvwz = dets_val.index({"...",Slice(1,None)}) / dets_val.index({"...",Slice(0,1)});  // [Nq,K,4]
    
    at::Tensor u = uvwz.index({"...",0});
    at::Tensor v = uvwz.index({"...",1});
    at::Tensor w = uvwz.index({"...",2});
    at::Tensor z = uvwz.index({"...",3});  // [Nq,K]

    at::Tensor mask = torch::logical_and(u > 0, v > 0);  // [Nq,K]
    mask = torch::logical_and(mask, w > 0);  
    mask = torch::logical_and(mask, z > 0);  // [Nq,K]
    mask = mask.toType(torch::kInt32);  // change type

    // if not contained in any tets, set index and barys to -1, [0,0,0,0]
    mask = torch::cat({mask, torch::ones_like(mask.index({"...",Slice(None,1)}))}, 1);  // [Nq,K+1]
    at::Tensor tet_idx = torch::argmax(mask, 1);  // [Nq,]
    uvwz = torch::cat({uvwz, torch::zeros_like(uvwz.index({"...",Slice(None,1),Slice()}))}, 1);  // [Nq,K+1,4]
    at::Tensor barycentric = torch::gather(uvwz, 1, tet_idx.unsqueeze(1).unsqueeze(2).expand({-1,1,4})).permute({0,2,1});

    // tet_idx is the in local index in the K tets. Need to change to global index
    neighbor_idx = torch::cat({neighbor_idx, -1 * torch::ones_like(neighbor_idx.index({"...",Slice(None,1)}))}, 1);  // [Nq,K+1]
    tet_idx = torch::gather(neighbor_idx, 1, tet_idx.unsqueeze(1));  // [Nq,1]

    return std::make_tuple(tet_idx.squeeze(1), barycentric.squeeze(1));
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("query", &query_cpp, "cpp query function");
}