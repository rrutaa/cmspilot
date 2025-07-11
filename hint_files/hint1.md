# =============================================
# UPROOT TUTORIAL (draft)
# =============================================

# 0. LIBRARIES
# most of the queries use awkward to handle arrays, so it would be safe to:
import awkward as ak
# and of course:
import uproot
# for plotting we use:
import matplotlib.pyplot as plt


# 1. BASIC FILE OPERATIONS
import uproot
file = uproot.open("file.root")  # or "root://server/path/file.root" for remote

# View contents
print("Keys:", file.keys())
print("Classnames:", file.classnames())
print("Tree entries:", file["Events"].num_entries)

# 2. LOADING DATA
tree = file["Events"]
branches = tree.arrays()  # all branches
selected_branches = tree.arrays(["Muon_pt", "Muon_eta"])  # specific branches

# 3. WORKING WITH JAGGED ARRAYS
import awkward as ak
muon_pt = branches["Muon_pt"]

# Common operations
print("First event:", muon_pt[0].tolist())
print("Number of muons per event:", ak.num(muon_pt))
print("Flattened array:", ak.flatten(muon_pt))
print("Leading muon pts:", muon_pt[:, 0])  # first muon in each event

# 4. SELECTIONS AND FILTERING
# Single cut
good_pt_mask = branches["Muon_pt"] > 20
good_muons = branches["Muon_pt"][good_pt_mask]

# Compound cut
good_muons_mask = (branches["Muon_pt"] > 20) & (abs(branches["Muon_eta"]) < 2.4)
events_with_good_muons = ak.any(good_muons_mask, axis=1)
filtered_events = branches[events_with_good_muons]

# 5. PLOTTING
import matplotlib.pyplot as plt
plt.hist(ak.flatten(branches["Muon_pt"]), bins=50, range=(0, 100))
plt.xlabel("Muon pT [GeV]")
plt.ylabel("Counts")
plt.title("Muon Transverse Momentum")
plt.show()

# 6. SAVING RESULTS
# Save filtered events
with uproot.recreate("filtered.root") as fout:
    fout["Events"] = filtered_events

# Save specific branches
with uproot.recreate("selected.root") as fout:
    fout["Events"] = {"Muon_pt": branches["Muon_pt"], "Muon_eta": branches["Muon_eta"]}

# =============================================
# PERFORMANCE TIPS (UNCOMMENT TO USE)
# =============================================
# Process in chunks:
# for batch in tree.iterate(step_size="100 MB"):
#     process(batch)

# Use parallel processing:
# branches = tree.arrays(num_workers=4)

# Cache frequently accessed data:
# tree = tree.cache()

# =============================================
# COMMON ERRORS AND FIXES:
# 1. "KeyError" → Check file.keys() for correct branch names
# 2. "Cannot interpret" → Specify library="pd" for Pandas or "ak" for Awkward
# 3. Memory errors → Use iterate() or smaller step_size
# =============================================