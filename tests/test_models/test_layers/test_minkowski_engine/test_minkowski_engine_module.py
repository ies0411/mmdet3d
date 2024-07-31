# Copyright (c) OpenMMLab. All rights reserved.
import pytest
import torch

from mmdet3d.models.layers.minkowski_engine_block import \
    IS_MINKOWSKI_ENGINE_AVAILABLE

if IS_MINKOWSKI_ENGINE_AVAILABLE:
    from MinkowskiEngine import SparseTensor

    from mmdet3d.models.layers.minkowski_engine_block import (
        MinkowskiBasicBlock, MinkowskiBottleneck, MinkowskiConvModule)
else:
    pytest.skip('test requires Minkowski Engine.', allow_module_level=True)


def test_MinkowskiConvModule():
    if not torch.cuda.is_available():
        pytest.skip('test requires GPU and torch+cuda')
    voxel_features = torch.tensor(
        [[6.56126, 0.9648336, -1.7339306, 0.315],
         [6.8162713, -2.480431, -1.3616394, 0.36],
         [11.643568, -4.744306, -1.3580885, 0.16],
         [23.482342, 6.5036807, 0.5806964, 0.35]],
        dtype=torch.float32).cuda()  # n, point_features
    coordinates = torch.tensor(
        [[0, 12, 819, 131], [0, 16, 750, 136], [1, 16, 705, 232],
         [1, 35, 930, 469]],
        dtype=torch.int32).cuda()  # n, 4(batch, ind_x, ind_y, ind_z)

    # test
    input_sp_tensor = SparseTensor(voxel_features, coordinates)

    self = MinkowskiConvModule(4, 4, kernel_size=2, stride=2).cuda()

    out_features = self(input_sp_tensor)
    assert out_features.F.shape == torch.Size([4, 4])


def test_MinkowskiResidualBlock():
    if not torch.cuda.is_available():
        pytest.skip('test requires GPU and torch+cuda')
    voxel_features = torch.tensor(
        [[6.56126, 0.9648336, -1.7339306, 0.315],
         [6.8162713, -2.480431, -1.3616394, 0.36],
         [11.643568, -4.744306, -1.3580885, 0.16],
         [23.482342, 6.5036807, 0.5806964, 0.35]],
        dtype=torch.float32).cuda()  # n, point_features
    coordinates = torch.tensor(
        [[0, 12, 819, 131], [0, 16, 750, 136], [1, 16, 705, 232],
         [1, 35, 930, 469]],
        dtype=torch.int32).cuda()  # n, 4(batch, ind_x, ind_y, ind_z)

    # test
    input_sp_tensor = SparseTensor(voxel_features, coordinates)

    sparse_block0 = MinkowskiBasicBlock(4, 4, kernel_size=3).cuda()
    sparse_block1 = MinkowskiBottleneck(
        4,
        4,
        downsample=MinkowskiConvModule(4, 16, kernel_size=1, act_cfg=None),
        kernel_size=3).cuda()

    # test forward
    out_features0 = sparse_block0(input_sp_tensor)
    out_features1 = sparse_block1(input_sp_tensor)
    assert out_features0.F.shape == torch.Size([4, 4])
    assert out_features1.F.shape == torch.Size([4, 16])
