---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: [remove-input]

%config InlineBackend.figure_formats = ['svg']

import numpy as np
import matplotlib.pyplot as plt
from flatspin.model import *
```

# flatspin
flatspin is a GPU-accelerated simulator for systems of interacting nanomagnet spins arranged on a 2D lattice, also known as Artificial Spin Ice (ASI).
flatspin can simulate the dynamics of large ASI systems with thousands of interacting elements.
flatspin is written in Python and uses OpenCL for GPU acceleration.
flatspin comes with extra bells and whistles for analysis and visualization.
flatspin is open-source software and released under a GNU GPL license

Some example ASI systems are shown below:

```{code-cell} ipython3
:tags: [remove-input]

params = {
    'init': 'random',
    'alpha': 1.0,
    'use_opencl': 1,
    'neighbor_distance': np.inf,
}
model = SquareSpinIceClosed(size=(10,10), **params)
model.relax()
plt.subplot(131)
plt.axis('off')
model.plot()

model = PinwheelSpinIceDiamond(size=(10,10), **params)
model.relax()
plt.subplot(132)
plt.axis('off')
model.plot()

model = KagomeSpinIce(size=(7,9), **params)
model.relax()
plt.subplot(133)
plt.axis('off')
model.plot();

plt.tight_layout();
```

Ready to learn more?
Head over to [](installation) to download and install flatspin.
Then dive into the [](quickstart) to get started using the simulator.
