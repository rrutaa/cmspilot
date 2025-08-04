import uproot
import awkward as ak
import matplotlib.pyplot as plt

# 1. Open the ROOT file
file = uproot.open("4AAF4AB2-171D-F54C-8FE3-0D709B049A8A.root")

# 2. Access the "Events" tree and load the Muon_pt branch as an awkward array
tree = file["Events"]
muon_pt = tree["Muon_pt"].array()  # jagged array: one entry per event, possibly multiple muons/event

# 3. Flatten the jagged array to get all Muon pT values
pt_flat = ak.flatten(muon_pt)

# 4. Plot histogram
plt.hist(pt_flat, bins=50, range=(0, 100))
plt.xlabel("Muon pT [GeV]")
plt.ylabel("Counts")
plt.title("Muon Transverse Momentum")
plt.show()