## Generate De-Multiplex Setup Files (CSV) for CellRanger multi

### Requirements
- Python v3.6 or newer

### Usage
```bash
python main.py --help
```
The script supplies two modes: 

##### INIT
Prepare a basic setup for your current analysis by setting required paths and settings on BAM file creation.

```bash
python main.py -INIT \
        --setup-codename your-setup_name \    # choose freely
        --ref-human-gex "./path/to/GEX.csv" \
        --probeset-human-transcriptome "./path/to/transcriptome.csv" \
        --write-bam-files \     # optional:     not set => no BAM files
        --output-dir "./path/to/your/new/demultiplex_setup_files/"
```

This will create a new setup file under "<path/to/script>/init_files/your-setup_name.json". Subsequent calls to the GEN mode


##### GEN
Generate setup files from an initialised basic setup, adding sample-pool specific information.

```bash
python main.py -GEN \
        --setup-codename your-setup_name \  # MUST have been created before, see INIT
        --sample_pool_name pool_id \
        --fastq-path "./path/to/fastqs" \
        --sample-id-BC001 HD_ab1234 
        --sample-id-BC002 HD_cd5678 
        --sample-id-BC003 PAT_ba8765 
        --sample-id-BC004 PAT_dc4321
```


### Notes

###### Missing / planned features
- extensive failsafes, data type checks etc.  -->  handle carefully!
- features for: 
    - VDJ-T/-B, ... inclusion
    - multiple sample pools w/ equal sample-ids
    - ...


###### Feedback / Feature Requests

- Author: [Timm Kühnel](https://www.medizin.uni-muenster.de/klinik-fuer-neurologie/forschung/arbeitsgruppe-meyer-zu-hoerste/team.html) - t.kuehnel@ukmuenster.de