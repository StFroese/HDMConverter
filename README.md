# HDMConverter

## Install
1. Download this repo
2. 
```bash
git submodule init
```
3.
```bash
conda env create -f environment.yaml
```

## Execute

```bash
python converter.py -o <output-file.dat>
```
Optionally, you can request only specific channels
```bash
python converter.py -o <output-file.dat> -c 'b' 'W' 'tau' ...
```
