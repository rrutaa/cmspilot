## 0. LIBRARIES
import uproot  # For working with ROOT files
import awkward as ak  # For handling jagged arrays
import matplotlib.pyplot as plt  # For plotting histograms

## 1. BASIC FILE OPERATIONS
file = uproot.open("file.root")  # Open the ROOT file
print(file.keys())  # Print all object keys in the ROOT file
print(file.classnames())  # Print class names of objects (e.g., TTree, TH1)
print(file["Events"].num_entries)  # Show number of entries in the "Events" TTree

## 2. LOADING DATA
tree = file["Events"]  # Access the TTree named "Events"
branches = tree.arrays()  # Load all branches into an Awkward Array
selected = tree.arrays(["Muon_pt", "Muon_eta"])  # Load only specified branches: "Muon_pt", "Muon_eta"

## 3. WORKING WITH JAGGED ARRAYS
muon_pt = branches["Muon_pt"]  # Jagged array of muon pT values per event
first_muon_pt = ak.firsts(muon_pt)  # Take the first muon's pT in each event
num_muons = ak.count(muon_pt, axis=1)  # Count number of muons per event

## 4. SELECTIONS AND FILTERING
good_pt = branches["Muon_pt"] > 20  # Boolean mask for muons with pT > 20 GeV
good_muons = branches["Muon_pt"][good_pt]  # Filtered muon pT values

mask = (branches["Muon_pt"] > 20) & (abs(branches["Muon_eta"]) < 2.4)  # Combined selection
events_with_good_muons = ak.any(mask, axis=1)  # Keep events with at least one "good" muon
filtered_events = branches[events_with_good_muons]  # Apply event-level filter

## 5. PLOTTING
plt.hist(ak.flatten(good_muons), bins=50, range=(20, 200))  # Flatten array and plot histogram
plt.xlabel("Muon pT [GeV]")
plt.ylabel("Counts")
plt.title("Muon Transverse Momentum")
plt.show()

## 6. OTHER OPERATIONS
btag_discriminant = branches["Jet_btag"]  # Probability of jets originating from a b quark

# ΔR between two objects is defined as:
# sqrt( (Δphi)^2 + (Δeta)^2 )

# Create dimuon combinations (2 at a time) from high-pt muons
dimuons = ak.combinations(good_muons, 2, axis=0)

# Limit analysis to the first N events (e.g., 10,000)
n = 10000
events_firstN = tree.arrays(entry_stop=n)

## COMMON ERRORS
# KeyError → check file.keys()
# cannot interpret → specify library="pd" or "ak"
# Memory errors → use iterate() or smaller step_size
