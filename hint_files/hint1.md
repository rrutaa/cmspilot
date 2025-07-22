# 0. LIBRARIES
import uproot
import awkward as ak
import matplotlib.pyplot as plt

# 1. BASIC FILE OPERATIONS
file = uproot.open("file.root")
print(file.keys())
print(file.classnames())
print(file["Events"].num_entries)

# 2. LOADING DATA
tree = file["Events"]
branches = tree.arrays()
selected = tree.arrays(["Muon_pt", "Muon_eta"])

# 3. WORKING WITH JAGGED ARRAYS
muon_pt = branches["Muon_pt"]
print(muon_pt[0].tolist())
print(ak.num(muon_pt))
print(ak.flatten(muon_pt))
first_muon_pt = ak.firsts(muon_pt)
print(first_muon_pt)

# 4. SELECTIONS AND FILTERING
good_pt = branches["Muon_pt"] > 20
good_muons = branches["Muon_pt"][good_pt]

mask = (branches["Muon_pt"] > 20) & (abs(branches["Muon_eta"]) < 2.4)
events_with_good_muons = ak.any(mask, axis=1)
filtered_events = branches[events_with_good_muons]

# 5. PLOTTING
plt.hist(ak.flatten(branches["Muon_pt"]), bins=50, range=(0, 100))
plt.xlabel("Muon pT [GeV]")
plt.ylabel("Counts")
plt.title("Muon Transverse Momentum")
plt.show()

# COMMON ERRORS
KeyError → check file.keys()
cannot interpret → specify library="pd" or "ak"
Memory errors → use iterate() or smaller step_size
