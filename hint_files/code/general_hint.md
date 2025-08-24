## 0. LIBRARIES

```python
import uproot  # For working with ROOT files
import awkward as ak  # For handling jagged arrays
import matplotlib.pyplot as plt  # For plotting histograms
```

---
## 1. BASIC FILE OPERATIONS

```python
file = uproot.open("file.root")  # Open the ROOT file
print(file.keys())  # Print all object keys in the ROOT file
print(file.classnames())  # Print class names of objects (e.g., TTree, TH1)
print(file["Events"].num_entries)  # Show number of entries in the "Events" TTree

```

---
## 2. LOADING DATA

```python
tree = file["Events"]  # Access the TTree named "Events"
branches = tree.arrays()  # Load all branches into an Awkward Array
selected = tree.arrays(["Muon_pt", "Muon_eta"])  # Load only specified branches: "Muon_pt", "Muon_eta"

```

---
## 3. WORKING WITH JAGGED ARRAYS

```python
muon_pt = branches["Muon_pt"]  # Jagged array of muon pT values per event
first_muon_pt = ak.firsts(muon_pt)  # Take the first muon's pT in each event
num_muons = ak.count(muon_pt, axis=1)  # Count number of muons per event

```

---
## 4. SELECTIONS AND FILTERING

```python
good_pt = branches["Muon_pt"] > 20  # Boolean mask for muons with pT > 20 GeV
good_muons = branches["Muon_pt"][good_pt]  # Filtered muon pT values

mask = (branches["Muon_pt"] > 20) & (abs(branches["Muon_eta"]) < 2.4)  # Combined selection
events_with_good_muons = ak.any(mask, axis=1)  # Keep events with at least one "good" muon
filtered_events = branches[events_with_good_muons]  # Apply event-level filter

```

---
## 5. PLOTTING

```python
plt.hist(ak.flatten(good_muons), bins=50, range=(20, 200))  # Flatten array and plot histogram
plt.xlabel("Muon pT [GeV]")
plt.ylabel("Counts")
plt.title("Muon Transverse Momentum")
plt.show()

```

---
## 6. OTHER OPERATIONS

```python
btag_discriminant = branches["Jet_btag"]  # Probability of jets originating from a b quark
absolute_value = abs(value)               # Absolute value of a parameter, ak.abs() is incorrect.

```

---
## 7. HANDLING JAGGED ARRAYS: LEADING OBJECTS SAFELY

# Assume we have a jagged array of some physics object, e.g., "Muon_eta"

```python
muon_eta = tree["Muon_eta"].array()  # Jagged array: one list per event

```

---
# Limit to first N events

```python
n = 5000
muon_eta_subset = muon_eta[:n]

```

---
# Filter out events with no entries (e.g., 0 muons)

```python
nonempty = muon_eta_subset[ak.num(muon_eta_subset) > 0]

```

---
# Extract leading value (first element in each non-empty event)

```python
leading_muon_eta = nonempty[:, 0]

```

---
# Plot the distribution of the leading value

```python
plt.hist(leading_muon_eta, bins=50, range=(-3.2, 3.2))
plt.xlabel("Leading Muon Eta")
plt.ylabel("Counts")
plt.title("Leading Muon Eta")
plt.show()

```

---
# ΔR between two objects is defined as:
# sqrt( (Δphi)^2 + (Δeta)^2 )

# Create dimuon combinations (2 at a time) from high pt muons

```python
dimuons = ak.combinations(good_muons, 2, axis=0)

```

---
# Limit analysis to the first N events (e.g., 10,000)

```python
n = 10000
events_firstN = tree.arrays(entry_stop=n)

```

---

