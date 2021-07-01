# Results of testing the projection plot memory usage
# Test 1


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    25    131.1 MiB    131.1 MiB           1   @profile
    26                                         def test_func1():
    27                                             
    28    136.1 MiB      5.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    29                                             
    30   1893.6 MiB      0.0 MiB           2       for i in range(nframes):
    31    136.2 MiB      0.1 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    32   1883.9 MiB   1747.7 MiB           1           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    33                                         
    34   1893.6 MiB      9.7 MiB           1           frame = np.array(plot.frb['density'])
    35                                         
    36   1893.6 MiB      0.0 MiB           1           frame_data[i] =  frame[:]
    37   1893.6 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    25    132.0 MiB    132.0 MiB           1   @profile
    26                                         def test_func1():
    27                                             
    28    132.0 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    29                                             
    30   4244.3 MiB      0.0 MiB          11       for i in range(nframes):
    31   3961.7 MiB      1.0 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    32   4230.4 MiB   3965.8 MiB          10           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    33                                         
    34   4240.1 MiB     96.5 MiB          10           frame = np.array(plot.frb['density'])
    35                                         
    36   4244.3 MiB     49.0 MiB          10           frame_data[i] =  frame[:]
    37   4244.3 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```
# Test 2


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    39    130.3 MiB    130.3 MiB           1   @profile
    40                                         def test_func2():
    41                                             
    42    136.3 MiB      6.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    43    136.3 MiB      0.0 MiB           1       gc.disable()
    44                                             
    45   1864.7 MiB      0.0 MiB           2       for i in range(nframes):
    46    136.4 MiB      0.0 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    47   1854.9 MiB   1718.6 MiB           1           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    48                                         
    49   1864.7 MiB      9.8 MiB           1           frame = np.array(plot.frb['density'])
    50                                         
    51   1864.7 MiB      0.0 MiB           1           frame_data[i] =  frame[:]
    52                                         
    53   1864.7 MiB      0.0 MiB           1           del frame
    54   1864.7 MiB      0.0 MiB           1           del next_slab
    55   1864.7 MiB      0.0 MiB           1           del plot
    56                                         
    57   1864.7 MiB      0.0 MiB           1           gc.collect()
    58                                         
    59   1864.7 MiB      0.0 MiB           1       gc.enable()
    60   1864.7 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    39    132.2 MiB    132.2 MiB           1   @profile
    40                                         def test_func2():
    41                                             
    42    132.2 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    43    132.2 MiB      0.0 MiB           1       gc.disable()
    44                                             
    45   2528.1 MiB      0.0 MiB          11       for i in range(nframes):
    46   2446.1 MiB      0.1 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    47   2514.7 MiB   2249.7 MiB          10           plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    48                                         
    49   2524.2 MiB     96.5 MiB          10           frame = np.array(plot.frb['density'])
    50                                         
    51   2528.0 MiB     49.3 MiB          10           frame_data[i] =  frame[:]
    52                                         
    53   2528.0 MiB      0.0 MiB          10           del frame
    54   2528.0 MiB      0.0 MiB          10           del next_slab
    55   2528.0 MiB      0.0 MiB          10           del plot
    56                                         
    57   2528.1 MiB      0.2 MiB          10           gc.collect()
    58                                         
    59   2528.1 MiB      0.0 MiB           1       gc.enable()
    60   2528.1 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```
# Test 3


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    62    130.8 MiB    130.8 MiB           1   @profile
    63                                         def test_func3():
    64                                             
    65    137.0 MiB      6.2 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    66    137.2 MiB      0.2 MiB           1       next_slab = ds.r[:,:,0 : dL]
    67   1883.2 MiB   1746.0 MiB           1       plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    68                                         
    69   2106.2 MiB      0.0 MiB           2       for i in range(nframes):
    70   1883.2 MiB      0.0 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    71   2097.1 MiB    213.8 MiB           1           plot._switch_ds(ds, data_source=next_slab)
    72                                         
    73   2106.1 MiB      9.0 MiB           1           frame = np.array(plot.frb['density'])
    74                                         
    75   2106.2 MiB      0.2 MiB           1           frame_data[i] =  frame[:]
    76   2106.2 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    62    130.3 MiB    130.3 MiB           1   @profile
    63                                         def test_func3():
    64                                             
    65    130.3 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    66    130.5 MiB      0.2 MiB           1       next_slab = ds.r[:,:,0 : dL]
    67   1879.9 MiB   1749.4 MiB           1       plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')
    68                                         
    69   4442.2 MiB      0.0 MiB          11       for i in range(nframes):
    70   4182.9 MiB      0.5 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    71   4433.6 MiB   2465.9 MiB          10           plot._switch_ds(ds, data_source=next_slab)
    72                                         
    73   4437.7 MiB     47.1 MiB          10           frame = np.array(plot.frb['density'])
    74                                         
    75   4442.2 MiB     48.7 MiB          10           frame_data[i] =  frame[:]
    76   4442.2 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```
# Test 4


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    81    133.0 MiB    133.0 MiB           1   @profile
    82                                         def test_func4():
    83                                         
    84    137.7 MiB      4.8 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    85    137.9 MiB      0.1 MiB           1       next_slab = ds.r[:,:,0 : dL]
    86                                             
    87   1869.8 MiB      0.0 MiB           2       for i in range(nframes):
    88    137.9 MiB      0.0 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    89   1867.2 MiB   1729.3 MiB           1           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
    90   1867.2 MiB      0.0 MiB           1           frb = plot.to_frb(1, 800)
    91   1869.7 MiB      2.5 MiB           1           frame = np.array(frb['density'])
    92                                         
    93   1869.8 MiB      0.2 MiB           1           frame_data[i] =  frame[:]
    94   1869.8 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    81    134.3 MiB    134.3 MiB           1   @profile
    82                                         def test_func4():
    83                                         
    84    134.3 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    85    134.3 MiB      0.0 MiB           1       next_slab = ds.r[:,:,0 : dL]
    86                                             
    87   4108.5 MiB      0.0 MiB          11       for i in range(nframes):
    88   3839.2 MiB      0.9 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
    89   4101.5 MiB   3900.0 MiB          10           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
    90   4101.5 MiB      0.0 MiB          10           frb = plot.to_frb(1, 800)
    91   4103.7 MiB     24.5 MiB          10           frame = np.array(frb['density'])
    92                                         
    93   4108.5 MiB     48.8 MiB          10           frame_data[i] =  frame[:]
    94   4108.5 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```
# Test 5


## Creating 1 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    94    130.3 MiB    130.3 MiB           1   @profile
    95                                         def test_func5():
    96                                         
    97    135.1 MiB      4.8 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    98    135.1 MiB      0.0 MiB           1       gc.disable()
    99                                             
   100   1837.5 MiB      0.0 MiB           2       for i in range(nframes):
   101    135.3 MiB      0.2 MiB           1           next_slab = ds.r[:,:,i*vel : i*vel+dL]
   102   1835.0 MiB   1699.6 MiB           1           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
   103   1835.0 MiB      0.0 MiB           1           frb = plot.to_frb(1, 800)
   104   1837.5 MiB      2.5 MiB           1           frame = np.array(frb['density'])
   105                                         
   106   1837.5 MiB      0.0 MiB           1           frame_data[i] =  frame[:]
   107                                         
   108   1837.5 MiB      0.0 MiB           1           del frame
   109   1837.5 MiB      0.0 MiB           1           del frb
   110   1837.5 MiB      0.0 MiB           1           del plot
   111   1837.5 MiB      0.0 MiB           1           del next_slab
   112   1837.5 MiB      0.0 MiB           1           gc.collect()
   113                                         
   114   1837.5 MiB      0.0 MiB           1       gc.enable()
   115   1837.5 MiB      0.0 MiB           1       return frame_data


Final product is 4.8829345703125 MB
```

## Creating 10 frame(s) from dataset

```
Filename: test.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    94    127.0 MiB    127.0 MiB           1   @profile
    95                                         def test_func5():
    96                                         
    97    127.0 MiB      0.0 MiB           1       frame_data = np.zeros((nframes, 800, 800))
    98    127.0 MiB      0.0 MiB           1       gc.disable()
    99                                             
   100   2496.1 MiB      0.0 MiB          11       for i in range(nframes):
   101   2412.8 MiB      0.2 MiB          10           next_slab = ds.r[:,:,i*vel : i*vel+dL]
   102   2488.8 MiB   2294.4 MiB          10           plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
   103   2488.8 MiB      0.0 MiB          10           frb = plot.to_frb(1, 800)
   104   2490.9 MiB     24.3 MiB          10           frame = np.array(frb['density'])
   105                                         
   106   2495.9 MiB     48.9 MiB          10           frame_data[i] =  frame[:]
   107                                         
   108   2495.9 MiB      0.0 MiB          10           del frame
   109   2495.9 MiB      0.0 MiB          10           del frb
   110   2495.9 MiB      0.0 MiB          10           del plot
   111   2495.9 MiB      0.0 MiB          10           del next_slab
   112   2496.1 MiB      1.2 MiB          10           gc.collect()
   113                                         
   114   2496.1 MiB      0.0 MiB           1       gc.enable()
   115   2496.1 MiB      0.0 MiB           1       return frame_data


Final product is 48.8282470703125 MB
```
