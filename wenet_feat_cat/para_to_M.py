import numpy as np

def get_human_readable_count(number: int) -> str:
    """Return human_readable_count

    Originated from:
    https://github.com/PyTorchLightning/pytorch-lightning/blob/master/pytorch_lightning/core/memory.py

    Abbreviates an integer number with K, M, B, T for thousands, millions,
    billions and trillions, respectively.
    Examples:
        >>> get_human_readable_count(123)
        '123  '
        >>> get_human_readable_count(1234)  # (one thousand)
        '1 K'
        >>> get_human_readable_count(2e6)   # (two million)
        '2 M'

    Originated from:
    https://github.com/PyTorchLightning/pytorch-lightning/blob/master/pytorch_lightning/core/memory.py

    Abbreviates an integer number with K, M, B, T for thousands, millions,
    billions and trillions, respectively.
    Examples:
        >>> get_human_readable_count(123)
        '123  '
        >>> get_human_readable_count(1234)  # (one thousand)
        '1 K'
        >>> get_human_readable_count(2e6)   # (two million)
        '2 M'
        >>> get_human_readable_count(3e9)   # (three billion)
        '3 B'
        >>> get_human_readable_count(4e12)  # (four trillion)
        '4 T'
        >>> get_human_readable_count(5e15)  # (more than trillion)
        '5,000 T'
    Args:
        number: a positive integer number
    Return:
        A string formatted according to the pattern described above.
    """
    assert number >= 0
    labels = [" ", "K", "M", "B", "T"]
    num_digits = int(np.floor(np.log10(number)) + 1 if number > 0 else 1)
    num_groups = int(np.ceil(num_digits / 3))
    num_groups = min(num_groups, len(labels))  # don't abbreviate beyond trillions
    shift = -3 * (num_groups - 1)
    number = number * (10**shift)
    index = num_groups - 1
    return f"{number:.2f} {labels[index]}"
param=get_human_readable_count(76642797)
print(param)
