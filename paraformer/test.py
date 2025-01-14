import torch
def make_pad_mask(lengths: torch.Tensor, max_len: int = 0) -> torch.Tensor:
    """Make mask tensor containing indices of padded part.

    See description of make_non_pad_mask.

    Args:
        lengths (torch.Tensor): Batch of lengths (B,).
    Returns:
        torch.Tensor: Mask tensor containing indices of padded part.

    Examples:
        >>> lengths = [5, 3, 2]
        >>> make_pad_mask(lengths)
        masks = [[0, 0, 0, 0 ,0],
                 [0, 0, 0, 1, 1],
                 [0, 0, 1, 1, 1]]
    """
    batch_size = lengths.size(0)
    max_len = max_len if max_len > 0 else lengths.max().item()
    seq_range = torch.arange(0,
                             max_len,
                             dtype=torch.int64,
                             device=lengths.device)
    seq_range_expand = seq_range.unsqueeze(0).expand(batch_size, max_len)
    seq_length_expand = lengths.unsqueeze(-1)
    mask = seq_range_expand >= seq_length_expand
    return mask



def make_pad_mask_paraformer(lengths, xs=None, length_dim=-1, maxlen=None):
    """Make mask tensor containing indices of padded part.

     Args:
         lengths (LongTensor or List): Batch of lengths (B,).
         xs (Tensor, optional): The reference tensor.
             If set, masks will be the same shape as this tensor.
         length_dim (int, optional): Dimension indicator of the above tensor.
             See the example.

     Returns:
         Tensor: Mask tensor containing indices of padded part.
                 dtype=torch.uint8 in PyTorch 1.2-
                 dtype=torch.bool in PyTorch 1.2+ (including 1.2)

     Examples:
         With only lengths.

         >>> lengths = [5, 3, 2]
         >>> make_pad_mask(lengths)
         masks = [[0, 0, 0, 0 ,0],
                  [0, 0, 0, 1, 1],
                  [0, 0, 1, 1, 1]]

         With the reference tensor.
     >>> xs = torch.zeros((3, 2, 4))
         >>> make_pad_mask(lengths, xs)
         tensor([[[0, 0, 0, 0],
                  [0, 0, 0, 0]],
                 [[0, 0, 0, 1],
                  [0, 0, 0, 1]],
                 [[0, 0, 1, 1],
                  [0, 0, 1, 1]]], dtype=torch.uint8)
         >>> xs = torch.zeros((3, 2, 6))
         >>> make_pad_mask(lengths, xs)
         tensor([[[0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 1]],
                 [[0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1]],
                 [[0, 0, 1, 1, 1, 1],
                  [0, 0, 1, 1, 1, 1]]], dtype=torch.uint8)

         With the reference tensor and dimension indicator.

         >>> xs = torch.zeros((3, 6, 6))
         >>> make_pad_mask(lengths, xs, 1)
         tensor([[[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1]],
                 [[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1]],
                 [[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1]]], dtype=torch.uint8)
         >>> make_pad_mask(lengths, xs, 2)
         tensor([[[0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 1]],
                 [[0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1]],
                 [[0, 0, 1, 1, 1, 1],
                  [0, 0, 1, 1, 1, 1],
                  [0, 0, 1, 1, 1, 1],
                  [0, 0, 1, 1, 1, 1],
                  [0, 0, 1, 1, 1, 1],
                  [0, 0, 1, 1, 1, 1]]], dtype=torch.uint8)
    """
    if length_dim == 0:
        raise ValueError("length_dim cannot be 0: {}".format(length_dim))

    if not isinstance(lengths, list):
        lengths = lengths.tolist()
    bs = int(len(lengths))
    if maxlen is None:
        if xs is None:
            maxlen = int(max(lengths))
        else:
            maxlen = xs.size(length_dim)
    else:
        assert xs is None
        assert maxlen >= int(max(lengths))

    seq_range = torch.arange(0, maxlen, dtype=torch.int64)
    seq_range_expand = seq_range.unsqueeze(0).expand(bs, maxlen)
    seq_length_expand = seq_range_expand.new(lengths).unsqueeze(-1)
    mask = seq_range_expand >= seq_length_expand

    assert xs.size(0) == bs, (xs.size(0), bs)

    if length_dim < 0:
         length_dim = xs.dim() + length_dim
     # ind = (:, None, ..., None, :, , None, ..., None)
    ind = tuple(
         slice(None) if i in (0, length_dim) else None for i in range(xs.dim())
     )
    mask = mask[ind].expand_as(xs).to(xs.device)
    return mask
lengths=torch.tensor([5,3,2])
encoder_out=torch.rand([1,10,256])
print(encoder_out.shape,encoder_out.size(1))

mask_lengths=~make_pad_mask(lengths, max_len=encoder_out.size(1))
print(mask_lengths)
mask_lengths_paraformer=~make_pad_mask_paraformer(lengths,maxlen=encoder_out.size(1))
print(mask_lengths_paraformer)



