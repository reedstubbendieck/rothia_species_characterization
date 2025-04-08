# *Rothia similimucilaginosa* sp. nov., isolated from the human nasal cavity

Mercedes Pérez Pérez<sup>1</sup>, Jacobey King<sup>2</sup>, Paul A. Lawson<sup>2</sup>, Reed M. Stubbendieck<sup>1,#</sup>

<sup>1</sup> Department of Microbiology and Molecular Genetics, Oklahoma State University, Stillwater, OK 74078  
<sup>2</sup> School of Biological Sciences, University of Oklahoma, Norman, OK 73019

<sup>#</sup> Correspondence: Reed M. Stubbendieck ([stubbendieck@okstate.edu](mailto:stubbendieck@okstate.edu))

---

## Background

This repository contains raw data and scripts necessary to reproduce the analyses supporting the identification of *Rothia similimucilaginosa* as a novel *Rothia* species. All commands assume execution from the base directory.

---

## Data

- Raw data (genome sequences, 16S rRNA gene sequences): `./rawData/`
- Derived data: [Figshare](http://www.doi.org/10.6084/m9.figshare.28732967)

---

## Requirements

- [core_species_tree](https://github.com/chevrm/core_species_tree)
- [FigTree](http://tree.bio.ed.ac.uk/software/figtree/)
- [anvi'o 8](https://anvio.org/)
- [antiSMASH 7](https://antismash.secondarymetabolites.org/#!/download)
- [BiG-SCAPE](https://bigscape-corason.secondarymetabolites.org/installation/)
- [multismash](https://github.com/zreitz/multismash)
- [clinker](https://github.com/gamcil/clinker)

---

## Conda Environments

Create environments:

```bash
conda env create -f envs/antismash7.yaml
conda env create -f envs/anvio-8.yaml
conda env create -f envs/bakta.yaml
conda env create -f envs/clinker.yaml
```

---

## Generating a Core Genome Phylogeny

```bash
cd ./derivedData/core_genome_phylogeny/
perl /path/to/core_species_tree.pl ../../rawData/genomes/for_core_genome_phylogeny/*.fasta
cd ../../
```

### Visualizing Core Genome Phylogeny

1. Load `./derivedData/core_species_tree/astra.species.tre` in FigTree.
2. Root tree using *Kocuria rosea* strain DSM 20477.
3. Transform branch lengths proportional to the root.
4. Visualize in [FigTree](http://tree.bio.ed.ac.uk/software/figtree/) or [iTOL](https://itol.embl.de/).

---

## Calculating GC Content

```bash
python3 ./scripts/python/calculate_GC.py ./rawData/genomes/for_core_genome_phylogeny/
```

---

## anvi'o 8 Pipeline for Pangenomics

```bash
conda activate anvio-8
./scripts/python/run_anvio.py ./rawData/genomes/for_anvio/ ./derivedData/anvio_out/ Rothia 16
conda deactivate
```

---

## Average Amino Acid Identity

```bash
conda activate baktka
python3 ./scripts/python/run_bakta.py ./rawData/genomes/for_anvio/ ./derivedData/bakta_out/ 16
conda deactivate
```

Then use the [AAI-profiler](http://ekhidna2.biocenter.helsinki.fi/AAI/) to determine AAI values.

---

## Identifying Biosynthetic Gene Clusters and Generating Gene Cluster Families

```bash
conda activate antismash7
multismash ./rawData/rothia_bgc.config
conda deactivate
```

### Generating BGC Heatmap

1. Open `./derivedData/multismash_out/bigscape/index.html` in a browser.
2. Download Absence/Presence table (tsv) and save to:

```
./derivedData/multismash_out/bigscape/absence_presence.tsv
```

Run:

```bash
python3 ./scripts/python/clean_bigscape_presence-absence.py
```

---

## Generating BGC Synteny Map

1. Copy GBK files of interest to:

```
./derivedData/clinker_out/gbks/
```

2. Run clinker:

```bash
conda activate clinker
clinker ./derivedData/clinker_out/gbks/*.gbk -o ./derivedData/clinker_out/alignments -p ./derivedData/clinker_out/clinker_out.html --force
conda deactivate
```

---

## Generating Figures (R)

Use `Rothia_Species_Characterization.Rmd` to generate figures for ANIb, ANIm, dDDH, and GCF heatmaps.

