This repo shows my experiment on different image augmentation techniques.

## Dataset
For this experiment, I used the Caltech101. <br>
This dataset is small and highly imbalanced, so hopefully all the image augmentation techniques can show their effectiveness.
<p align="center">
<img src="images/dist.png" width=60% align="center">
<em>Class distribution of Caltech101</em>
</p>

## Model
EfficientNet-B0

## Results

<table>
  <tr>
    <th></th>
    <th>Technique</th>
    <th>Acc(%)</th>
  </tr>
  <tr>
    <td></td>
    <td><span style="font-weight:400;font-style:normal">No Image Augmentation</span></td>
    <td><span style="font-weight:400;font-style:normal">54.76</span></td>
  </tr>
  <tr>
    <td rowspan="8">pyTorch</td>
    <td><span style="font-weight:400;font-style:normal">Random Erasing</span></td>
    <td><span style="font-weight:400;font-style:normal">56.95</span></td>
  </tr>
  <tr>
    <td>Vertical Flip</td>
    <td>59.37</td>
  </tr>
  <tr>
    <td>Horizontal Flip</td>
    <td><span style="font-weight:400;font-style:normal">62.48</span></td>
  </tr>
  <tr>
    <td><span style="font-weight:400;font-style:normal">Affine Transform</span></td>
    <td><span style="font-weight:400;font-style:normal">65.42</span></td>
  </tr>
  <tr>
    <td>Rotation</td>
    <td>65.82</td>
  </tr>
  <tr>
    <td><span style="font-weight:400;font-style:normal">Resized Crop</span></td>
    <td><span style="font-weight:400;font-style:normal">68.13</span></td>
  </tr>
  <tr>
    <td>Crop+Rotate</td>
    <td>70.55</td>
  </tr>
  <tr>
    <td>Affine+Flip+Crop+Rotate+Erase</td>
    <td>65.42</td>
  </tr>
  <tr>
    <td rowspan="4">Not in<br>pyTorch</td>
    <td>Cutout</td>
    <td>59.37</td>
  </tr>
  <tr>
    <td>AutoAugment</td>
    <td>65.30</td>
  </tr>
  <tr>
    <td>RandAugment</td>
    <td>70.43</td>
  </tr>
  <tr>
    <td>CutMix</td>
    <td></td>
  </tr>
</table>


## References:
<ul>
  <li><a href="https://pytorch.org/docs/stable/torchvision/transforms.html">pyTorch transformations</a></li>
  <li><a href="https://arxiv.org/abs/1708.04552">Cutout</a></li>
  <li><a href="https://arxiv.org/abs/1708.04896">RandomErasing</a></li>
  <li><a href="https://arxiv.org/abs/1805.09501">AutoAugment</a></li>
  <li><a href="https://arxiv.org/abs/1909.13719">RandAugment</a></li>
</ul>
