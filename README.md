# Extract information from sudoku grids

Detecting sudoku grids patterns and recognizing digits using computer vision. In the training folder three type of sudoku grids pictures are given: classic, jigsaw and jigsaw colored. <code>run_project.py</code> script outputs txt file with whether or not there is a digit in a cell and the digit predicted. For the jigsaw grids, the zone of the cell is also detected, as shown in the examples bellow. Check <code>Doc.pdf</code> for more detailed information over solution.

<div min-width=820>
  <img src='training/clasic/06.jpg' width=250 float='left'>
  <img src='training/jigsaw/01.jpg' width=250 float='left'>
  <img src='training/jigsaw/03.jpg' width=250 float='left'>
</div>
<br>ooo5ooooo|         1o2o2o262o272o2o24|        1o1o1o262o2o212o3o<br>
    9oo482oo5|         1o1o193o3o3o254o42|        421o1o2o25273o2o3o<br>
    o753o1o6o|         12333o3o5o5o564o4o|        454o1o1o5o5o3o3o3o<br>
    8o7oo4o2o|         1o1o683o3o315o444o|        4o4o1o195o513o333o<br>
    o39oooooo|         1o1o626o6o5o5o4o4o|        4o494o5o5o5o5o686o<br>
    4oo7oo6oo|         6o6o6o637o5o5o8o4o|        79714o7o7o536o6o6o<br>
    3oo82o9oo|         9o9o7o6o7o7o578o8o|        7o7o7o7o8o8o8o6o67<br>
    oo8oooo4o|         969o7o747o7o8o858o|        9o9o9o7384858o6o69<br>
    o9ooo6o3o|         979893959o7o8o8o8o|        9o959o919o9o8o8o8o<br>
    
<br>
The libraries required to run the project
<ul>
  <li>python==3.9.5</li>
  <li>numpy==1.19.5</li>
  <li>opencv_python==4.5.4.58</li>
  <li>tqdm==4.62.3</li>
</ul>
