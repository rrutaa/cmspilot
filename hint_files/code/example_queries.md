## Q7: Plot the number of jets per event in the XYZ dataset

```python
import uproot                                     # Import uproot to read ROOT files
import matplotlib.pyplot as plt                   # Import matplotlib for plotting
import awkward as ak                              # Import awkward-array for jagged array handling

file = uproot.open("/home/ruta/irishep/test.root") # Open the ROOT file

tree = file["Events"]                            # Access the TTree named "Events"
selected = tree.arrays(["Jet_pt"])               # Load only the "Jet_pt" branch (jagged array: jets per event)

n_jets = ak.num(selected["Jet_pt"])              # Count the number of jets per event using ak.num
plt.hist(n_jets, bins=15, range=(0, 15))         # Plot histogram of jet multiplicity
plt.xlabel("Number of jets")                     # X-axis label
plt.ylabel("Number of events")                   # Y-axis label
plt.title("Jet multiplicity per event")          # Plot title
plt.show()                                       # Display the plot
```

---

## Q8: Plot the electron transverse momentum for electrons with $p_T > 25$ GeV in the first 20000 events of the XYZ dataset

```python
import uproot                                     # Import uproot for ROOT file reading
import matplotlib.pyplot as plt                   # Import matplotlib for plotting
import awkward as ak                              # Import awkward-array for jagged array handling

file = uproot.open("/home/ruta/irishep/test.root")  # Open the ROOT file

tree = file["Events"]                            # Access the TTree named "Events"
selected = tree.arrays(["Electron_pt"], entry_stop=20000)  # Load "Electron_pt" for first 20k events

good_electrons = selected["Electron_pt"][selected["Electron_pt"] > 25]  # Select electrons with certain criteria, in this case it is pT > 25 GeV
plt.hist(ak.flatten(good_electrons), bins=50, range=(25, 200))          # Flatten and plot histogram
plt.xlabel("Electron $p_T$ [GeV]")                # X-axis label
plt.ylabel("Number of electrons")                 # Y-axis label
plt.title(r"Electrons with $p_T > 25$ GeV in first 20k events")  # Plot title
plt.show()                                        # Display the plot
```

---

## Q9: Plot the leading jet $p_T$ (highest $p_T$ jet per event) in the XYZ dataset

```python
import uproot                                     # Import uproot for ROOT file access
import matplotlib.pyplot as plt                   # Import matplotlib for plotting
import awkward as ak                              # Import awkward-array for jagged array handling
import numpy as np                                # Import numpy for numerical operations

file = uproot.open("/home/ruta/irishep/test.root")  # Open the ROOT file

tree = file["Events"]                            # Access the TTree named "Events"
selected = tree.arrays(["Jet_pt"])               # Load the "Jet_pt" branch

leading_jet_pt = ak.max(selected["Jet_pt"], axis=1, initial=0)  # Find max (leading) jet pT per event
plt.hist(leading_jet_pt, bins=50, range=(0, 500))               # Plot leading jet pT histogram
plt.xlabel("Leading Jet $p_T$ [GeV]")            # X-axis label
plt.ylabel("Number of events")                   # Y-axis label
plt.title("Leading jet $p_T$ per event")         # Plot title
plt.show()                                       # Display the plot
```

---

## Q10: Plot the invariant mass of all muon pairs with the same charge in the XYZ dataset

```python
import uproot                                     # Import uproot for ROOT file access
import matplotlib.pyplot as plt                   # Import matplotlib for plotting
import awkward as ak                              # Import awkward-array for jagged array handling
import numpy as np                                # Import numpy for numerical calculations

file = uproot.open("/home/ruta/irishep/test.root")  # Open the ROOT file

tree = file["Events"]                            # Access the TTree named "Events"
selected = tree.arrays([                         # Load muon kinematic and charge branches
    "Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"
])

pairs = ak.combinations(ak.zip({                 # Build all possible muon pairs in each event
    "pt": selected["Muon_pt"],
    "eta": selected["Muon_eta"],
    "phi": selected["Muon_phi"],
    "mass": selected["Muon_mass"],
    "charge": selected["Muon_charge"]
}), 2)

mu1 = pairs["0"]                                 # Extract 1st muon in each pair
mu2 = pairs["1"]                                 # Extract 2nd muon in each pair

same_charge = mu1.charge * mu2.charge > 0        # Boolean mask for same-charge pairs

mass = np.sqrt(                                  # Compute invariant mass for each pair
    2 * mu1.pt * mu2.pt *
    (np.cosh(mu1.eta - mu2.eta) - np.cos(mu1.phi - mu2.phi))
)

plt.hist(ak.flatten(mass[same_charge]), bins=60, range=(0, 200))  # Plot histogram for same-charge pairs
plt.xlabel(r"Invariant mass $m_{\mu\mu}$ [GeV]") # X-axis label
plt.ylabel("Number of pairs")                    # Y-axis label
plt.title("Same-charge muon pair invariant mass") # Plot title
plt.show()                                       # Display the plot
```

---

## Q11: Plot the missing transverse energy for events with no jets in the XYZ dataset

```python
import uproot                                     # Import uproot for ROOT file access
import matplotlib.pyplot as plt                   # Import matplotlib for plotting
import awkward as ak                              # Import awkward-array for jagged array handling

file = uproot.open("/home/ruta/irishep/test.root")  # Open the ROOT file

tree = file["Events"]                            # Access the TTree named "Events"
selected = tree.arrays(["Jet_pt", "MET_pt"])     # Load jet pT and Missing transverse energy branches, 

n_jets = ak.num(selected["Jet_pt"])              # Count jets per event
no_jet_events = n_jets == 0                      # Boolean mask for events with zero jets
plt.hist(selected["MET_pt"][no_jet_events], bins=40, range=(0, 200))  # Plot MET for those events
plt.xlabel("Missing $p_T$ [GeV]")                # X-axis label
plt.ylabel("Number of events")                   # Y-axis label
plt.title("MET for events with zero jets")        # Plot title
plt.show()                                       # Display the plot
```


## Q12: Plot ΔR between the two leading jets for events with at least two jets in the XYZ dataset

```python
import uproot                                     # Import uproot for ROOT file access
import matplotlib.pyplot as plt                   # Import matplotlib for plotting
import awkward as ak                              # Import awkward-array for jagged array handling
import numpy as np                                # Import numpy for numerical calculations

file = uproot.open("/home/ruta/irishep/test.root")  # Open the ROOT file

tree = file["Events"]                            # Access the TTree named "Events"
selected = tree.arrays(["Jet_pt", "Jet_eta", "Jet_phi"])  # Load jet kinematics

pt = selected["Jet_pt"]                          # Get jet pT jagged array
eta = selected["Jet_eta"]                        # Get jet eta jagged array
phi = selected["Jet_phi"]                        # Get jet phi jagged array

has_two_jets = ak.num(pt) >= 2                   # Boolean mask for events with >= 2 jets

# Select kinematics of two leading jets in each event
leading_eta = eta[has_two_jets][:, :2]           # Eta of two leading jets
leading_phi = phi[has_two_jets][:, :2]           # Phi of two leading jets

delta_eta = leading_eta[:, 0] - leading_eta[:, 1]                  # Δη between leading jets
delta_phi = np.abs(leading_phi[:, 0] - leading_phi[:, 1])          # Δφ between leading jets
delta_phi = ak.where(delta_phi > np.pi, 2 * np.pi - delta_phi, delta_phi)  # Correct Δφ for periodicity

delta_r = np.sqrt(delta_eta**2 + delta_phi**2)   # Compute ΔR

plt.hist(delta_r, bins=40, range=(0, 6))         # Plot histogram of ΔR
plt.xlabel(r"$\Delta R$ between two leading jets") # X-axis label
plt.ylabel("Number of events")                   # Y-axis label
plt.title(r"Jet-jet $\Delta R$ for events with $\geq 2$ jets")  # Plot title
plt.show()                                       # Display the plot
```

---

