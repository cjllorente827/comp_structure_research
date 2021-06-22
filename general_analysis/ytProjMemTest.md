# Results of testing the projection plot memory usage
# Test 1


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    25    137.6 MiB    137.6 MiB           1   @profile
    26                                         def test_func1():
    27                                             
    28    144.4 MiB      6.7 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    29                                             
    30    275.8 MiB      0.0 MiB           2       for i in range(nframes):
    31    144.4 MiB      0.1 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    32    270.9 MiB    126.5 MiB           1           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    33                                         
    34    275.6 MiB      4.7 MiB           1           frame = np.array(plot.frb['density'])
    35                                         
    36    275.8 MiB      0.2 MiB           1           frame_data[i] =  frame[:]
    37    275.8 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    25    137.4 MiB    137.4 MiB           1   @profile
    26                                         def test_func1():
    27                                             
    28    139.4 MiB      2.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    29                                             
    30    538.0 MiB      0.0 MiB          11       for i in range(nframes):
    31    501.3 MiB      1.2 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    32    523.6 MiB    284.1 MiB          10           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    33                                         
    34    533.3 MiB     66.7 MiB          10           frame = np.array(plot.frb['density'])
    35                                         
    36    538.0 MiB     46.5 MiB          10           frame_data[i] =  frame[:]
    37    538.0 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    25    132.6 MiB    132.6 MiB           1   @profile
    26                                         def test_func1():
    27                                             
    28    132.6 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    29                                             
    30   2572.6 MiB      0.3 MiB         301       for i in range(nframes):
    31   2567.8 MiB      7.9 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    32   2567.8 MiB    817.1 MiB         300           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    33                                         
    34   2567.8 MiB    170.9 MiB         300           frame = np.array(plot.frb['density'])
    35                                         
    36   2572.6 MiB   1443.7 MiB         300           frame_data[i] =  frame[:]
    37   2572.6 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
# Test 2


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    39    140.3 MiB    140.3 MiB           1   @profile
    40                                         def test_func2():
    41                                             
    42    145.3 MiB      5.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    43    145.3 MiB      0.0 MiB           1       gc.disable()
    44                                             
    45    283.8 MiB      0.0 MiB           2       for i in range(nframes):
    46    145.5 MiB      0.2 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    47    278.9 MiB    133.4 MiB           1           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    48                                         
    49    283.6 MiB      4.7 MiB           1           frame = np.array(plot.frb['density'])
    50                                         
    51    283.8 MiB      0.2 MiB           1           frame_data[i] =  frame[:]
    52                                         
    53    283.8 MiB      0.0 MiB           1           del frame
    54    283.8 MiB      0.0 MiB           1           del next_slab
    55    283.8 MiB      0.0 MiB           1           del plot
    56                                         
    57    283.8 MiB      0.0 MiB           1           gc.collect()
    58                                         
    59    283.8 MiB      0.0 MiB           1       gc.enable()
    60    283.8 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    39    144.1 MiB    144.1 MiB           1   @profile
    40                                         def test_func2():
    41                                             
    42    146.1 MiB      2.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    43    146.1 MiB      0.0 MiB           1       gc.disable()
    44                                             
    45    339.0 MiB      0.0 MiB          11       for i in range(nframes):
    46    336.1 MiB      0.2 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    47    336.1 MiB    131.1 MiB          10           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    48                                         
    49    336.1 MiB     14.2 MiB          10           frame = np.array(plot.frb['density'])
    50                                         
    51    338.8 MiB     46.7 MiB          10           frame_data[i] =  frame[:]
    52                                         
    53    338.8 MiB      0.0 MiB          10           del frame
    54    338.8 MiB      0.0 MiB          10           del next_slab
    55    338.8 MiB      0.0 MiB          10           del plot
    56                                         
    57    339.0 MiB      0.8 MiB          10           gc.collect()
    58                                         
    59    339.0 MiB      0.0 MiB           1       gc.enable()
    60    339.0 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    39    128.2 MiB    128.2 MiB           1   @profile
    40                                         def test_func2():
    41                                             
    42    130.2 MiB      2.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    43    130.2 MiB      0.0 MiB           1       gc.disable()
    44                                             
    45   2322.5 MiB    -80.1 MiB         301       for i in range(nframes):
    46   2317.8 MiB    -79.9 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    47   2332.2 MiB   3719.3 MiB         300           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    48                                         
    49   2337.1 MiB   1702.7 MiB         300           frame = np.array(plot.frb['density'])
    50                                         
    51   2341.9 MiB   1464.5 MiB         300           frame_data[i] =  frame[:]
    52                                         
    53   2341.9 MiB      0.2 MiB         300           del frame
    54   2341.9 MiB      0.2 MiB         300           del next_slab
    55   2341.9 MiB      0.0 MiB         300           del plot
    56                                         
    57   2322.5 MiB  -4775.0 MiB         300           gc.collect()
    58                                         
    59   2322.5 MiB      0.0 MiB           1       gc.enable()
    60   2322.5 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
# Test 3


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    62    132.5 MiB    132.5 MiB           1   @profile
    63                                         def test_func3():
    64                                             
    65    137.5 MiB      5.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    66    137.5 MiB      0.1 MiB           1       next_slab = ds.r[:,:,0 : dL]
    67    271.9 MiB    134.4 MiB           1       plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    68                                         
    69    287.1 MiB      0.0 MiB           2       for i in range(nframes):
    70    271.9 MiB      0.0 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    71    282.2 MiB     10.3 MiB           1           plot._switch_ds(ds, data_source=next_slab)
    72                                         
    73    287.0 MiB      4.8 MiB           1           frame = np.array(plot.frb['density'])
    74                                         
    75    287.1 MiB      0.1 MiB           1           frame_data[i] =  frame[:]
    76    287.1 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    62    135.9 MiB    135.9 MiB           1   @profile
    63                                         def test_func3():
    64                                             
    65    135.9 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    66    136.1 MiB      0.2 MiB           1       next_slab = ds.r[:,:,0 : dL]
    67    256.7 MiB    120.6 MiB           1       plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    68                                         
    69    538.2 MiB      0.0 MiB          11       for i in range(nframes):
    70    504.4 MiB      0.4 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    71    530.4 MiB    202.3 MiB          10           plot._switch_ds(ds, data_source=next_slab)
    72                                         
    73    534.7 MiB     29.7 MiB          10           frame = np.array(plot.frb['density'])
    74                                         
    75    538.2 MiB     49.1 MiB          10           frame_data[i] =  frame[:]
    76    538.2 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    62    135.1 MiB    135.1 MiB           1   @profile
    63                                         def test_func3():
    64                                             
    65    135.1 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    66    135.2 MiB      0.0 MiB           1       next_slab = ds.r[:,:,0 : dL]
    67    265.6 MiB    130.4 MiB           1       plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    68                                         
    69   2645.1 MiB    -92.4 MiB         301       for i in range(nframes):
    70   2641.0 MiB    -91.6 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    71   2641.0 MiB    726.9 MiB         300           plot._switch_ds(ds, data_source=next_slab)
    72                                         
    73   2641.0 MiB      0.4 MiB         300           frame = np.array(plot.frb['density'])
    74                                         
    75   2645.1 MiB   1370.3 MiB         300           frame_data[i] =  frame[:]
    76   2645.1 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
# Test 4


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    78    131.6 MiB    131.6 MiB           1   @profile
    79                                         def test_func4():
    80                                         
    81    136.2 MiB      4.6 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    82    136.4 MiB      0.2 MiB           1       next_slab = ds.r[:,:,0 : dL]
    83                                             
    84    252.9 MiB      0.0 MiB           2       for i in range(nframes):
    85    136.4 MiB      0.0 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    86    243.6 MiB    107.2 MiB           1           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
    87    243.6 MiB      0.0 MiB           1           frb = plot.to_frb(1, 800)
    88    252.9 MiB      9.3 MiB           1           frame = np.array(frb['density'])
    89                                         
    90    252.9 MiB      0.0 MiB           1           frame_data[i] =  frame[:]
    91    252.9 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    78    133.0 MiB    133.0 MiB           1   @profile
    79                                         def test_func4():
    80                                         
    81    133.0 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    82    133.2 MiB      0.2 MiB           1       next_slab = ds.r[:,:,0 : dL]
    83                                             
    84    449.9 MiB      0.0 MiB          11       for i in range(nframes):
    85    426.1 MiB      0.2 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    86    436.2 MiB    180.0 MiB          10           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
    87    436.2 MiB      0.0 MiB          10           frb = plot.to_frb(1, 800)
    88    445.6 MiB     87.7 MiB          10           frame = np.array(frb['density'])
    89                                         
    90    449.9 MiB     48.8 MiB          10           frame_data[i] =  frame[:]
    91    449.9 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    78    136.9 MiB    136.9 MiB           1   @profile
    79                                         def test_func4():
    80                                         
    81    136.9 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    82    136.9 MiB      0.0 MiB           1       next_slab = ds.r[:,:,0 : dL]
    83                                             
    84   3047.5 MiB      0.0 MiB         301       for i in range(nframes):
    85   3042.9 MiB      2.0 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    86   3042.9 MiB    657.2 MiB         300           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
    87   3042.9 MiB      0.3 MiB         300           frb = plot.to_frb(1, 800)
    88   3042.9 MiB    787.9 MiB         300           frame = np.array(frb['density'])
    89                                         
    90   3047.5 MiB   1463.1 MiB         300           frame_data[i] =  frame[:]
    91   3047.5 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
# Test 5


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    93    133.6 MiB    133.6 MiB           1   @profile
    94                                         def test_func5():
    95                                         
    96    138.8 MiB      5.2 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    97    138.8 MiB      0.0 MiB           1       gc.disable()
    98                                             
    99    255.2 MiB      0.0 MiB           2       for i in range(nframes):
   100    138.9 MiB      0.1 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
   101    245.8 MiB    106.9 MiB           1           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
   102    245.8 MiB      0.0 MiB           1           frb = plot.to_frb(1, 800)
   103    255.1 MiB      9.3 MiB           1           frame = np.array(frb['density'])
   104                                         
   105    255.2 MiB      0.1 MiB           1           frame_data[i] =  frame[:]
   106                                         
   107    255.2 MiB      0.0 MiB           1           del frame
   108    255.2 MiB      0.0 MiB           1           del frb
   109    255.2 MiB      0.0 MiB           1           del plot
   110    255.2 MiB      0.0 MiB           1           del next_slab
   111    255.2 MiB      0.0 MiB           1           gc.collect()
   112                                         
   113    255.2 MiB      0.0 MiB           1       gc.enable()
   114    255.2 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    93    128.5 MiB    128.5 MiB           1   @profile
    94                                         def test_func5():
    95                                         
    96    130.5 MiB      2.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    97    130.5 MiB      0.0 MiB           1       gc.disable()
    98                                             
    99    296.4 MiB      0.0 MiB          11       for i in range(nframes):
   100    286.7 MiB      0.2 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
   101    286.7 MiB    104.7 MiB          10           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
   102    286.7 MiB      0.0 MiB          10           frb = plot.to_frb(1, 800)
   103    291.4 MiB     13.8 MiB          10           frame = np.array(frb['density'])
   104                                         
   105    296.4 MiB     47.0 MiB          10           frame_data[i] =  frame[:]
   106                                         
   107    296.4 MiB      0.0 MiB          10           del frame
   108    296.4 MiB      0.0 MiB          10           del frb
   109    296.4 MiB      0.0 MiB          10           del plot
   110    296.4 MiB      0.0 MiB          10           del next_slab
   111    296.4 MiB      0.1 MiB          10           gc.collect()
   112                                         
   113    296.4 MiB      0.0 MiB           1       gc.enable()
   114    296.4 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    93    138.9 MiB    138.9 MiB           1   @profile
    94                                         def test_func5():
    95                                         
    96    138.9 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    97    138.9 MiB      0.0 MiB           1       gc.disable()
    98                                             
    99   2320.4 MiB      0.0 MiB         301       for i in range(nframes):
   100   2313.7 MiB      0.4 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
   101   2313.7 MiB    114.9 MiB         300           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
   102   2313.7 MiB      0.0 MiB         300           frb = plot.to_frb(1, 800)
   103   2315.5 MiB    589.2 MiB         300           frame = np.array(frb['density'])
   104                                         
   105   2320.3 MiB   1465.9 MiB         300           frame_data[i] =  frame[:]
   106                                         
   107   2320.3 MiB      0.0 MiB         300           del frame
   108   2320.3 MiB      0.0 MiB         300           del frb
   109   2320.3 MiB      0.2 MiB         300           del plot
   110   2320.3 MiB      0.0 MiB         300           del next_slab
   111   2320.4 MiB     10.9 MiB         300           gc.collect()
   112                                         
   113   2320.4 MiB      0.0 MiB           1       gc.enable()
   114   2320.4 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
