
# TODO
- Export as a raised STL so that the label can be 3d printed?
- Automaticaly find the main axis of a part (seearch the local axis)
    - https://dev.opencascade.org/content/how-do-i-find-local-axis-shape
    - We want to find the [eigen vectors](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors), or at least the vector that are the least impacted by a given rotation
- Rotate the part around its center of gravity?
    - https://dev.opencascade.org/content/center-gravity
    - https://dev.opencascade.org/content/center-gravity-api



How to build the proper environnement:
```bash
conda create -n pyoccenv python=3.8
conda activate pyoccenv
conda install -c conda-forge pythonocc-core
```

Then once installed, just activate using:
```bash
conda activate pyoccenv
```




