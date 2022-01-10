# Extract information from sudoku grids

Detecting sudoku grids patterns and recognizing digits using computer vision. In the training folder three type of sudoku grids pictures are given: classic, jigsaw and jigsaw colored. <code>run_project.py</code> script outputs txt file with whether or not there is a digit in a cell and the digit predicted. For the jigsaw grids, the zone of the cell is also detected, like shown in the examples bellow. Check Doc.pdf for mor detailed information over solution.

<div min-width=820>
  <div float='left'><img src='training/clasic/06.jpg' width=250 float='left'>
    <br>ooo5ooooo<br>
    9oo482oo5<br>
    o753o1o6o<br>
    8o7oo4o2o<br>
    o39oooooo<br>
    4oo7oo6oo<br>
    3oo82o9oo<br>
    oo8oooo4o<br>
    o9ooo6o3o<br>
  </div>
  <div float='right'><img src='training/jigsaw/01.jpg' width=250 float='left'>
    <br>1o2o2o262o272o2o24<br>
    1o1o193o3o3o254o42<br>
    12333o3o5o5o564o4o<br>
    1o1o683o3o315o444o<br>
    1o1o626o6o5o5o4o4o<br>
    6o6o6o637o5o5o8o4o<br>
    9o9o7o6o7o7o578o8o<br>
    969o7o747o7o8o858o<br>
    979893959o7o8o8o8o<br>
  </div>
  <div float='left'><img src='training/jigsaw/03.jpg' width=250 float='left'>
    <br>1o1o1o262o2o212o3o<br>
    421o1o2o25273o2o3o<br>
    454o1o1o5o5o3o3o3o<br>
    4o4o1o195o513o333o<br>
    4o494o5o5o5o5o686o<br>
    79714o7o7o536o6o6o<br>
    7o7o7o7o8o8o8o6o67<br>
    9o9o9o7384858o6o69<br>
    9o959o919o9o8o8o8o<br>
  </div>  
</div>
<figure>
  <img src="training/clasic/06.jpg"  width=250 alt="my img"/>
  <figcaption>
    <br>1o2o2o262o272o2o24<br>
    1o1o193o3o3o254o42<br>
    12333o3o5o5o564o4o<br>
    1o1o683o3o315o444o<br>
    1o1o626o6o5o5o4o4o<br>
    6o6o6o637o5o5o8o4o<br>
    9o9o7o6o7o7o578o8o<br>
    969o7o747o7o8o858o<br>
    979893959o7o8o8o8o<br>
  </figcaption>
</figure>
<figure>
  <img src="training/clasic/06.jpg"  width=250 alt="my img"/>
  <figcaption>
    <br>1o2o2o262o272o2o24<br>
    1o1o193o3o3o254o42<br>
    12333o3o5o5o564o4o<br>
    1o1o683o3o315o444o<br>
    1o1o626o6o5o5o4o4o<br>
    6o6o6o637o5o5o8o4o<br>
    9o9o7o6o7o7o578o8o<br>
    969o7o747o7o8o858o<br>
    979893959o7o8o8o8o<br>
  </figcaption>
</figure>
<br>
The libraries required to run the project
<ul>
  <li>python==3.9.5</li>
  <li>numpy==1.19.5</li>
  <li>opencv_python==4.5.4.58</li>
  <li>tqdm==4.62.3</li>
</ul>
