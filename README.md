# mitobender

mitobender is a script to remove ambient mtDNA signal from [mgatk](github.com/caleblareau/mgatk) output based on [cellbender](github.com/broadinstitute/CellBender). it's provided here as 
standalone tool for easier installation and maintenance (otherwise identical to `mgatk remove-background`).

# installation

mitobender needs python (with click), R (with optparse, tidyr, hdf5r, Matrix and data.table) as well as CellBender. this is ideally done with conda:

```
conda create -n mitobender python=3.7
conda activate mitobender
conda install -c conda-forge hdf5 r-optparse r-tidyr r-hdf5r r-matrix r-data.table
pip install cellbender==0.2.0
pip install git+https://github.com/bihealth/mitobender.git
```

# preparation

in order to estimate ambient mtDNA levels, mgatk needs to be run on nearly-empty droplets as well as barcodes called by cellranger as proper nuclei-containing droplets. by default, we recommend using the top 20000 barcodes ranked by peak_region_fragments (column 18 in singlecell.csv) while removing barcodes with nonzero mitochondrial count (column 7 in singlecell.csv):

```
sort -rgk 18 -t ',' cellranger_output/outs/singlecell.csv | awk -F "\"*,\"*" '$7  > 0 {print}' | head -n 20000 | cut -f 1 -d ',' > top20k_barcodes.tsv
mgatk bcall -i cellranger_output/outs/possorted_bam.bam -n sample_id -o mgatk -c 8 -bt CB -b top20k_barcodes.tsv  --nsamples 1000
```

# usage

```
mitobender remove-background -m mgatk/final --expected-cells ${ncells}
```

where `${ncells}` is the actual expected cell number as determined by cellranger. mitobender will correct allele counts for variable sites and create a rds object called `mitobender_results.rds` similar to the one created by mgatk but with counts for those sites corrected. the selection of variable sites can be controlled via arguments `--n-cells-conf-detected`, `--strand-correlation` and `--vmr`, or by an explicit list of variants (like 263A>G) in a text file (one per line) passed to `--variable-sites`.

