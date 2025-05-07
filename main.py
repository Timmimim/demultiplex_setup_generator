import argparse
import json
import os
from os.path import dirname, exists, join as pjoin

class BadCallError(ValueError):
    pass

INIT_SETUP_PATH = pjoin(dirname(__file__), "init_files")
os.makedirs(INIT_SETUP_PATH, exist_ok=True)

parser = argparse.ArgumentParser("CellRanger De-Multiplex Setup Generator", 
                                    usage="Generate demultiplex setup files for CellRanger per pool with; currently only human reference supported.\n"\
                                            "\tStep 1 (optional): init -> Initialise (if not done before) to store your library paths and output path under a convenient codeword.\n"\
                                            "\tStep 2 (real deal): gen -> Generate a new demultiplex setup CSV file per pool.")


parser.add_argument("--setup-codename", required=True, type=str, help="Name under which to store this setup file initialisation; no spaces (only use \'-\' or \'_\' as separators), no special characters, no file type suffix (\'file.ending\')")

modi = parser.add_mutually_exclusive_group(required=True)
modi.add_argument("-INIT", action='store_true', help="Set the mode to INIT -> create a JSON file JSON to inform future setup files with common information (e.g. transcriptome paths).")
modi.add_argument("-GEN", action='store_true', help="Set the mode to GEN -> create a new setup file for a specific sample pool.")

init_group = parser.add_argument_group("Step 1: INIT",
                                "Initialise your current round of demultiplex setup generation by creating a local file to store;" \
                                    "store paths to genome libs etc. once under a codeword, and load them by that codeword as a shortcut" \
                                    "for every setup file created which uses these libraries!")

init_group.add_argument("--ref-human-gex", type=str, help="Absolute Path to your required Human Genome Reference")
init_group.add_argument("--probeset-human-transcriptome", type=str, help="Absolute Path to your required Human Genome Reference")
init_group.add_argument("--write-bam-files", action='store_true', help="Optional: Write .BAM / .BAI files for deeper analysis.\n")
init_group.add_argument("--output-dir", type=str)

gen_group = parser.add_argument_group("Step 2: GEN",
                                "Generate demultiplex setup CSV files for your pools.")

gen_group.add_argument("--sample_pool_name", type=str, help="Sample/Pool Name as used as the `prefix` for the FastQ files for this sample / pool.")
gen_group.add_argument("--fastq-path", type=str, help="Absolute path to the FastQ files for this sample / pool.")
gen_group.add_argument("--sample-id-BC001", type=str, help="ID of Sample with probe barcode BC001")
gen_group.add_argument("--sample-id-BC002", type=str, help="ID of Sample with probe barcode BC002")
gen_group.add_argument("--sample-id-BC003", type=str, help="ID of Sample with probe barcode BC003")
gen_group.add_argument("--sample-id-BC004", type=str, help="ID of Sample with probe barcode BC004")

args = parser.parse_args()
# parser.print_help()

mode = None
if args.INIT: 
    mode = "init"
elif args.GEN: 
    mode = "gen"
else:
    raise(BadCallError("At least one mode (INIT | GEN) must be chosen."))


setup_code = args.setup_codename

ref_human_gex = args.ref_human_gex
probeset_human_transcriptome = args.probeset_human_transcriptome
write_bam = args.write_bam_files
output_dir = args.output_dir

sample_pool_name = args.sample_pool_name
fastq_path  = args.fastq_path
sample_id_BC001 = args.sample_id_BC001
sample_id_BC002 = args.sample_id_BC002
sample_id_BC003 = args.sample_id_BC003
sample_id_BC004 = args.sample_id_BC004


if mode == "init":
    os.makedirs(output_dir, exist_ok=True)

    # generate and write a JSON file
    setup_dict = {
        'ref_human_gex'                 :   ref_human_gex,
        'probeset_human_transcriptome'  :   probeset_human_transcriptome,
        'write_bam'                     :   write_bam,
        'output_dir'                    :   output_dir,
    }
    setup_output_file = pjoin(INIT_SETUP_PATH, setup_code+'.json')
    print(f"Creating a setup json file at {setup_output_file} with: \n\
        {json.dumps(setup_dict, indent=4, sort_keys=False)}"
    )
    with open(setup_output_file, 'w') as json_file:
        json.dump(setup_dict, json_file, indent=4)
    print(f"Setup is done. You can safely proceed with step 2: GEN to generate de-multiplex setup files using data stored under setup code {setup_code}.")
    exit()

elif mode == "gen":

    # read JSON file and populate necessary variables re-used for all
    with open(pjoin(INIT_SETUP_PATH, setup_code+".json")) as json_file:
        setup_dict = json.load(json_file)

    ref_human_gex = setup_dict["ref_human_gex"]
    probeset_human_transcriptome = setup_dict["probeset_human_transcriptome"]
    write_bam = str(setup_dict["write_bam"]).lower()
    output_dir = setup_dict["output_dir"]

    os.makedirs(output_dir, exist_ok=True)

    new_demultiplex_setup_file_contents = f""\
    f"[gene-expression],,\n"\
    f"reference,{ref_human_gex},\n"\
    f"probe-set,{probeset_human_transcriptome},\n"\
    f"create-bam,{write_bam},\n"\
    f",,\n"\
    f"[libraries],,\n"\
    f"fastq_id,fastqs,feature_types\n"\
    f"{sample_pool_name},{fastq_path},Gene Expression\n"\
    f",,\n"\
    f"[samples],,\n"\
    f"sample_id,probe_barcode_ids,description\n"\
    f"{sample_id_BC001},BC001,{sample_id_BC001}\n"\
    f"{sample_id_BC002},BC002,{sample_id_BC002}\n"\
    f"{sample_id_BC003},BC003,{sample_id_BC003}\n"\
    f"{sample_id_BC004},BC004,{sample_id_BC004}\n"\
    

    output_file = pjoin(output_dir, "demultiplex_setup_"+sample_pool_name+".csv")
    if exists(output_file):
        print(f"WARNING: Target file for {sample_pool_name} exists in path {output_dir}!\nPlease (re-)move or rename the existing file; no files will be overwritten to avoid loss of information.")
        exit()

    with open(output_file, 'w') as demultiplex_setup_file:
        demultiplex_setup_file.write(new_demultiplex_setup_file_contents)
    print(f"Setup file for {sample_pool_name} successfully created.")
    exit()

else:
    print(parser.format_help())

"""
EXTENSIONS for future: 
add VDJ-T, VDJ-B, ... for libraries
# libraries = []
# TEMPLATE libraries
# 2410_Pool1_hdura_MS,/home/timm/CellRanger/ALB_hdura_FASTQs_merged,Gene Expression
# SAMPLE_POOL_NAME, FASTQ_PATH, FEATURE_TYPE
# if GEX: 
    # libraries.append(f"{sample_pool_name_gex},{fastq_path},Gene Expression")
# if VDJ_T:
    # libraries.append(f"{sample_pool_name_vdjT},{fastq_path},VDJ_T")
# if VDJ_B:
    # libraries.append(f"{sample_pool_name_vdjB},{fastq_path},VDJ_B")
# if libraries.empty:
    # raise InvalidInputError("You must specify 
# libraries = "\n".join(libraries_to_invoke)


"""