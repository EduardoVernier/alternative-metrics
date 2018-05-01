# alternative-metrics

### Pearson correlation

```
python3 Main.py correlation-matrix $(cat sw_datasets.txt)
```

```
for d in $(cat sw_datasets.txt); 
    do echo $d; 
    python3 Main.py correlation-scatter $d; 
    done;
```

### Unavoidable movement

```
python3 Main.py unavoidable-matrix $(cat sw_datasets.txt)
```

```
for d in $(cat sw_datasets.txt); 
    do echo $d; 
    python3 Main.py unavoidable-boxplots $d; 
    done;
```

```    
python3 Main.py unavoidable-envelope
```

### Delta vis and delta data combinations

```
python3 Main.py delta-ratio-matrix $(cat sw_datasets.txt)
```

```
for d in $(cat sw_datasets.txt); 
    do echo $d; 
    python3 Main.py delta-ratio-boxplots $d; 
    done;
```

```
python3 Main.py delta-diff-matrix $(cat sw_datasets.txt)
```

```
for d in $(cat sw_datasets.txt); 
    do echo $d; 
    python3 Main.py delta-diff-boxplots $d; 
    done;
```

### Aspect Ratios
```
python3 Main.py ar-matrix $(cat sw_datasets.txt)
```

```
for d in $(cat sw_datasets.txt); 
    do echo $d; 
    python3 Main.py ar-boxplots $d; 
    done;
```