---
title: Phase Retrieval in py4DSTEM
toc: false
theme: [air, alt, wide]
---

```js
const py4dstem_svg = FileAttachment("data-files/py4dstem-phase-retrieval.svg").image();
```
  
<div class="card">

# Phase Retrieval in py4STEM

<div id="py4dstem-container"> ${py4dstem_svg} </div>

- Suite of phase retrieval algorithms, including iterative DPC, ptychograpy, and parallax (tc-BF)
- User-friendly, object-oriented code
  - Check out our [tutorial notebooks](https://github.com/py4dstem/py4DSTEM_tutorials/tree/main/notebooks) and recent preprint [arXiv:2309.05250](https://arxiv.org/abs/2309.05250)!

```python
parallax = py4DSTEM.process.phase.Parallax(
    datacube=dataset, # DataCube
    energy = 300e3, # in V
).preprocess(
    plot_average_bf=True, # plots incoherent BF-image
).reconstruct(
    alignment_bin_values=[32,32,32,32,32,32,16,16,16,16,8,8],
    regularize_shifts=True, # constrains cross-correlation shifts
    progress_bar=True,
)
```

</div>

<style type="text/css">

  p {
    max-width:100%;
}

  #py4dstem-container img {
    max-width: 100%;
}

</style>


