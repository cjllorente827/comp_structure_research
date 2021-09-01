# Results of testing the projection plot memory usage
# Test 1


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    26    127.1 MiB    127.1 MiB           1   @profile
    27                                         def test_func1():
    28                                             
    29    131.9 MiB      4.8 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    30                                             
    31   1889.8 MiB      0.0 MiB           2       for i in range(nframes):
    32    132.0 MiB      0.1 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    33   1880.0 MiB   1748.0 MiB           1           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    34                                         
    35   1889.7 MiB      9.7 MiB           1           frame = np.array(plot.frb['density'])
    36                                         
    37   1889.8 MiB      0.1 MiB           1           frame_data[i] =  frame[:]
    38   1889.8 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    26    129.3 MiB    129.3 MiB           1   @profile
    27                                         def test_func1():
    28                                             
    29    129.3 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    30                                             
    31   4240.3 MiB      0.0 MiB          11       for i in range(nframes):
    32   3956.9 MiB      0.7 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    33   4225.7 MiB   3964.8 MiB          10           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    34                                         
    35   4235.4 MiB     96.7 MiB          10           frame = np.array(plot.frb['density'])
    36                                         
    37   4240.3 MiB     48.8 MiB          10           frame_data[i] =  frame[:]
    38   4240.3 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    26    128.4 MiB    128.4 MiB           1   @profile
    27                                         def test_func1():
    28                                             
    29    128.4 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    30                                             
    31  36288.9 MiB   -286.5 MiB         301       for i in range(nframes):
    32  36285.3 MiB   -260.1 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    33  36285.5 MiB  33046.3 MiB         300           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    34                                         
    35  36285.5 MiB   1051.9 MiB         300           frame = np.array(plot.frb['density'])
    36                                         
    37  36288.9 MiB   1142.0 MiB         300           frame_data[i] =  frame[:]
    38  36288.9 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
# Test 2


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    40    133.3 MiB    133.3 MiB           1   @profile
    41                                         def test_func2():
    42                                             
    43    139.5 MiB      6.2 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    44    139.5 MiB      0.0 MiB           1       gc.disable()
    45                                             
    46   1867.8 MiB      0.0 MiB           2       for i in range(nframes):
    47    139.6 MiB      0.1 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    48   1858.1 MiB   1718.5 MiB           1           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    49                                         
    50   1867.9 MiB      9.7 MiB           1           frame = np.array(plot.frb['density'])
    51                                         
    52   1867.9 MiB      0.0 MiB           1           frame_data[i] =  frame[:]
    53                                         
    54   1867.9 MiB      0.0 MiB           1           del frame
    55   1867.9 MiB      0.0 MiB           1           del next_slab
    56   1867.9 MiB      0.0 MiB           1           del plot
    57                                         
    58   1867.8 MiB     -0.0 MiB           1           gc.collect()
    59                                         
    60   1867.8 MiB      0.0 MiB           1       gc.enable()
    61   1867.8 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    40    139.0 MiB    139.0 MiB           1   @profile
    41                                         def test_func2():
    42                                             
    43    139.0 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    44    139.0 MiB      0.0 MiB           1       gc.disable()
    45                                             
    46   2534.9 MiB      0.0 MiB          11       for i in range(nframes):
    47   2451.5 MiB      0.1 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    48   2520.1 MiB   2249.9 MiB          10           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    49                                         
    50   2529.8 MiB     96.2 MiB          10           frame = np.array(plot.frb['density'])
    51                                         
    52   2534.6 MiB     48.8 MiB          10           frame_data[i] =  frame[:]
    53                                         
    54   2534.9 MiB      0.5 MiB          10           del frame
    55   2534.9 MiB      0.0 MiB          10           del next_slab
    56   2534.9 MiB      0.0 MiB          10           del plot
    57                                         
    58   2534.9 MiB      0.3 MiB          10           gc.collect()
    59                                         
    60   2534.9 MiB      0.0 MiB           1       gc.enable()
    61   2534.9 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    40    133.0 MiB    133.0 MiB           1   @profile
    41                                         def test_func2():
    42                                             
    43    133.0 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    44    133.0 MiB      0.0 MiB           1       gc.disable()
    45                                             
    46  12893.6 MiB    -91.5 MiB         301       for i in range(nframes):
    47  12861.8 MiB    -91.3 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    48  12879.0 MiB   9343.2 MiB         300           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    49                                         
    50  12888.9 MiB   2735.3 MiB         300           frame = np.array(plot.frb['density'])
    51                                         
    52  12893.8 MiB   1463.1 MiB         300           frame_data[i] =  frame[:]
    53                                         
    54  12893.8 MiB      1.0 MiB         300           del frame
    55  12893.8 MiB      0.5 MiB         300           del next_slab
    56  12893.8 MiB      0.2 MiB         300           del plot
    57                                         
    58  12893.6 MiB   -874.4 MiB         300           gc.collect()
    59                                         
    60  12893.6 MiB      0.0 MiB           1       gc.enable()
    61  12893.6 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
# Test 3


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    63    131.0 MiB    131.0 MiB           1   @profile
    64                                         def test_func3():
    65                                             
    66    135.9 MiB      4.9 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    67    136.0 MiB      0.1 MiB           1       next_slab = ds.r[:,:,0 : dL]
    68   1883.3 MiB   1747.3 MiB           1       plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    69                                         
    70   2107.0 MiB      0.0 MiB           2       for i in range(nframes):
    71   1883.3 MiB      0.0 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    72   2097.8 MiB    214.5 MiB           1           plot._switch_ds(ds, data_source=next_slab)
    73                                         
    74   2106.8 MiB      9.0 MiB           1           frame = np.array(plot.frb['density'])
    75                                         
    76   2107.0 MiB      0.2 MiB           1           frame_data[i] =  frame[:]
    77   2107.0 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    63    134.3 MiB    134.3 MiB           1   @profile
    64                                         def test_func3():
    65                                             
    66    134.3 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    67    134.4 MiB      0.0 MiB           1       next_slab = ds.r[:,:,0 : dL]
    68   1881.7 MiB   1747.3 MiB           1       plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    69                                         
    70   4444.7 MiB      0.0 MiB          11       for i in range(nframes):
    71   4185.0 MiB      0.8 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    72   4435.7 MiB   2466.6 MiB          10           plot._switch_ds(ds, data_source=next_slab)
    73                                         
    74   4439.9 MiB     46.9 MiB          10           frame = np.array(plot.frb['density'])
    75                                         
    76   4444.7 MiB     48.8 MiB          10           frame_data[i] =  frame[:]
    77   4444.7 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    63    130.9 MiB    130.9 MiB           1   @profile
    64                                         def test_func3():
    65                                             
    66    130.9 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    67    131.1 MiB      0.2 MiB           1       next_slab = ds.r[:,:,0 : dL]
    68   1881.0 MiB   1749.9 MiB           1       plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    69                                         
    70  38191.0 MiB   -288.8 MiB         301       for i in range(nframes):
    71  38188.0 MiB   -265.1 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    72  38188.0 MiB  33929.4 MiB         300           plot._switch_ds(ds, data_source=next_slab)
    73                                         
    74  38188.0 MiB    336.1 MiB         300           frame = np.array(plot.frb['density'])
    75                                         
    76  38191.0 MiB   1154.4 MiB         300           frame_data[i] =  frame[:]
    77  38191.0 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
# Test 4


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    79    132.6 MiB    132.6 MiB           1   @profile
    80                                         def test_func4():
    81                                         
    82    136.6 MiB      4.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    83    136.7 MiB      0.1 MiB           1       next_slab = ds.r[:,:,0 : dL]
    84                                             
    85   1867.6 MiB      0.0 MiB           2       for i in range(nframes):
    86    136.7 MiB      0.0 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    87   1865.2 MiB   1728.5 MiB           1           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
    88   1865.2 MiB      0.0 MiB           1           frb = plot.to_frb(1, 800)
    89   1867.6 MiB      2.4 MiB           1           frame = np.array(frb['density'])
    90                                         
    91   1867.6 MiB      0.0 MiB           1           frame_data[i] =  frame[:]
    92   1867.6 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    79    140.5 MiB    140.5 MiB           1   @profile
    80                                         def test_func4():
    81                                         
    82    140.5 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    83    140.7 MiB      0.2 MiB           1       next_slab = ds.r[:,:,0 : dL]
    84                                             
    85   4117.5 MiB      0.0 MiB          11       for i in range(nframes):
    86   3848.0 MiB      1.1 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    87   4110.4 MiB   3902.5 MiB          10           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
    88   4110.4 MiB      0.0 MiB          10           frb = plot.to_frb(1, 800)
    89   4112.6 MiB     24.5 MiB          10           frame = np.array(frb['density'])
    90                                         
    91   4117.5 MiB     48.7 MiB          10           frame_data[i] =  frame[:]
    92   4117.5 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    79    132.6 MiB    132.6 MiB           1   @profile
    80                                         def test_func4():
    81                                         
    82    132.8 MiB      0.2 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    83    132.9 MiB      0.0 MiB           1       next_slab = ds.r[:,:,0 : dL]
    84                                             
    85  65941.4 MiB      0.0 MiB         301       for i in range(nframes):
    86  65718.1 MiB     19.8 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    87  65934.4 MiB  63599.7 MiB         300           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
    88  65934.4 MiB      1.8 MiB         300           frb = plot.to_frb(1, 800)
    89  65936.5 MiB    723.5 MiB         300           frame = np.array(frb['density'])
    90                                         
    91  65941.4 MiB   1463.7 MiB         300           frame_data[i] =  frame[:]
    92  65941.4 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
# Test 5


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    94    132.9 MiB    132.9 MiB           1   @profile
    95                                         def test_func5():
    96                                         
    97    137.9 MiB      5.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    98    137.9 MiB      0.0 MiB           1       gc.disable()
    99                                             
   100   1840.3 MiB      0.0 MiB           2       for i in range(nframes):
   101    138.1 MiB      0.2 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
   102   1837.7 MiB   1699.7 MiB           1           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
   103   1837.7 MiB      0.0 MiB           1           frb = plot.to_frb(1, 800)
   104   1840.1 MiB      2.4 MiB           1           frame = np.array(frb['density'])
   105                                         
   106   1840.3 MiB      0.2 MiB           1           frame_data[i] =  frame[:]
   107                                         
   108   1840.3 MiB      0.0 MiB           1           del frame
   109   1840.3 MiB      0.0 MiB           1           del frb
   110   1840.3 MiB      0.0 MiB           1           del plot
   111   1840.3 MiB      0.0 MiB           1           del next_slab
   112   1840.3 MiB      0.0 MiB           1           gc.collect()
   113                                         
   114   1840.3 MiB      0.0 MiB           1       gc.enable()
   115   1840.3 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    94    133.2 MiB    133.2 MiB           1   @profile
    95                                         def test_func5():
    96                                         
    97    133.2 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    98    133.2 MiB      0.0 MiB           1       gc.disable()
    99                                             
   100   2502.2 MiB      0.0 MiB          11       for i in range(nframes):
   101   2419.0 MiB      0.2 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
   102   2495.0 MiB   2293.7 MiB          10           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
   103   2495.0 MiB      0.0 MiB          10           frb = plot.to_frb(1, 800)
   104   2497.2 MiB     25.0 MiB          10           frame = np.array(frb['density'])
   105                                         
   106   2502.1 MiB     48.7 MiB          10           frame_data[i] =  frame[:]
   107                                         
   108   2502.1 MiB      0.0 MiB          10           del frame
   109   2502.1 MiB      0.0 MiB          10           del frb
   110   2502.1 MiB      0.0 MiB          10           del plot
   111   2502.1 MiB      0.0 MiB          10           del next_slab
   112   2502.2 MiB      1.4 MiB          10           gc.collect()
   113                                         
   114   2502.2 MiB      0.0 MiB           1       gc.enable()
   115   2502.2 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```

## Creating 300 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    94    131.2 MiB    131.2 MiB           1   @profile
    95                                         def test_func5():
    96                                         
    97    131.2 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    98    131.2 MiB      0.0 MiB           1       gc.disable()
    99                                             
   100  12859.3 MiB      0.0 MiB         301       for i in range(nframes):
   101  12827.8 MiB      0.0 MiB         300           next_slab = ds.r[:,:,i*vel : i*vel+dL]
   102  12852.3 MiB  10517.2 MiB         300           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
   103  12852.3 MiB      1.9 MiB         300           frb = plot.to_frb(1, 800)
   104  12854.3 MiB    708.4 MiB         300           frame = np.array(frb['density'])
   105                                         
   106  12859.2 MiB   1463.7 MiB         300           frame_data[i] =  frame[:]
   107                                         
   108  12859.2 MiB      0.5 MiB         300           del frame
   109  12859.2 MiB      0.0 MiB         300           del frb
   110  12859.2 MiB      0.0 MiB         300           del plot
   111  12859.2 MiB      0.5 MiB         300           del next_slab
   112  12859.3 MiB     35.8 MiB         300           gc.collect()
   113                                         
   114  12859.3 MiB      0.0 MiB           1       gc.enable()
   115  12859.3 MiB      0.0 MiB           1       return frame_data


Final product is 1464.8438720703125 MB
```
