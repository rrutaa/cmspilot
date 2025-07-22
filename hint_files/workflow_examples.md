# CMS Analysis Combined Hint Snippets
import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np

# Load the file
file = uproot.open("file.root")
tree = file["Events"]

# --- Snippet 1: Muon Selection + Histogram + Save Filtered File ---
import uproot
import awkward as ak
import matplotlib.pyplot as plt

# Load branches
branches = tree.arrays(["Muon_pt", "Muon_eta", "Muon_charge"])

# Selection mask (jagged mask!)
mask = (branches["Muon_pt"] > 25) & (abs(branches["Muon_eta"]) < 2.1)

# Apply selection — this gives a jagged array of selected muons
selected_muons = {
    "Muon_pt": branches["Muon_pt"][mask],
    "Muon_eta": branches["Muon_eta"][mask],
    "Muon_charge": branches["Muon_charge"][mask],
}

# Plotting
plt.hist(ak.flatten(selected_muons["Muon_pt"]), bins=40, range=(0, 120))
plt.xlabel("Muon pT [GeV]")
plt.ylabel("Entries")
plt.title("Selected Muons pT")
plt.show()

# Save to ROOT
with uproot.recreate("muons_selected.root") as fout:
    fout["Events"] = selected_muons

# --- Snippet 2: Event Count Before/After Filter ---
branches = tree.arrays(["Muon_pt", "Muon_eta"])
initial_count = len(branches["Muon_pt"])

mask = (branches["Muon_pt"] > 30) & (abs(branches["Muon_eta"]) < 2.4)
filtered = branches[ak.any(mask, axis=1)]

final_count = len(filtered["Muon_pt"])
print(f"Initial event count: {initial_count}")
print(f"Filtered event count: {final_count}")

# --- Snippet 3: Using uproot.iterate() for Large Files ---
for batch in uproot.iterate("file.root:Events", step_size="50 MB"):
    muon_pt = batch["Muon_pt"]
    mask = ak.any(muon_pt > 20, axis=1)
    selected = batch[mask]
    print("Batch with good muons:", len(selected["Muon_pt"]))

# --- Snippet 4: Plotting η-φ Distribution of Muons ---
branches = tree.arrays(["Muon_eta", "Muon_phi"])

eta = ak.flatten(branches["Muon_eta"])
phi = ak.flatten(branches["Muon_phi"])

plt.hist2d(eta, phi, bins=50, range=[[-2.5, 2.5], [-np.pi, np.pi]])
plt.xlabel("Muon η")
plt.ylabel("Muon φ")
plt.title("η-φ Distribution")
plt.colorbar(label="Counts")
plt.show()

# --- Snippet 5: Combine Muon & Electron Branches for Event-level Cuts ---
branches = tree.arrays(["Muon_pt", "Electron_pt"])

muon_cut = ak.any(branches["Muon_pt"] > 25, axis=1)
electron_cut = ak.any(branches["Electron_pt"] > 20, axis=1)

has_lepton = muon_cut | electron_cut
lepton_events = branches[has_lepton]

print(f"Number of events with at least one good lepton: {len(lepton_events['Muon_pt'])}")
