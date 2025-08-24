## COMMON ERRORS

# axis=1 exceeds the depth of this array (1): You're applying axis=1 on a flat array.
#             - Only use `axis=1` on jagged arrays (e.g., arrays like `Muon_pt` with structure [events][muons]).
#             - Check structure with `print(ak.type(array))`.

# TypeError: cannot convert [...] to numpy array → Awkward arrays aren't NumPy arrays.
#             - Use `ak.to_numpy()` or `ak.flatten()` when needed.

## ValueError or TypeError when plotting jagged arrays.
#             - You're trying to plot an Awkward jagged array directly with matplotlib.
#             - Flatten the array first with `ak.flatten(array)`.
#             - Example: `plt.hist(ak.flatten(low_eta_jets), bins=40, range=(0,200))`.
#             - Check array structure with `print(low_eta_jets)` or `ak.type(low_eta_jets)`.

# Error running code: module 'awkward' has no attribute 'abs'
#             - use `absolute_value = abs(value)`, no need for `ak.abs`.

