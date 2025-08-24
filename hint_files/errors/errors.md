#COMMON ERRORS

axis=1 exceeds the depth of this array (1): You're applying axis=1 on a flat array.
    - Only use `axis=1` on jagged arrays (e.g., arrays like `Muon_pt` with structure [events][muons]).

TypeError: cannot convert [...] to numpy array → Awkward arrays aren't NumPy arrays.
    - Use `ak.to_numpy()` or `ak.flatten()` when needed.

Error running code: module 'awkward' has no attribute 'abs'
    - use `absolute_value = abs(value)`, no need for `ak.abs`.

