import os
import subprocess
import sys

def run_remove_background(mgatk_dir, expected_cells, epochs, fpr, use_cuda=False,
                          n_cells_conf_detected=None, strand_correlation=None,
                          vmr=None, variable_sites=None):
    """
    Run mgatk-style CellBender background removal:
      1. prepare_cellbender.R -> MTX input
      2. cellbender remove-background -> H5 output
      3. convert_cellbender_output.R -> mgatk-style output
    """

    script_dir = os.path.join(os.path.dirname(__file__), "R")
    prep_script = os.path.join(script_dir, "prepare_cellbender.R")
    conv_script = os.path.join(script_dir, "convert_cellbender_output.R")

    # Step 1: prepare input (.mtx + barcodes + genes)
    sys.stderr.write(f"[mitobender] preparing CellBender input\n")
    cellbender_input_dir = os.path.join(mgatk_dir, 'cellbender_input')
    os.makedirs(cellbender_input_dir, exist_ok=True)
    prep_cmd = ["Rscript", prep_script, "-i", mgatk_dir, "-o", cellbender_input_dir]

    if n_cells_conf_detected is not None:
        prep_cmd.extend(["--n_cells_conf_detected", str(n_cells_conf_detected)])
    if strand_correlation is not None:
        prep_cmd.extend(["--strand_correlation", str(strand_correlation)])
    if vmr is not None:
        prep_cmd.extend(["--vmr", str(vmr)])
    if variable_sites is not None:
        prep_cmd.extend(["--variable_sites", variable_sites])

    subprocess.run(prep_cmd, check=True)

    # Step 2: run CellBender
    sys.stderr.write(f"[mitobender] running CellBender\n")
    cellbender_output_dir = os.path.join(mgatk_dir, 'cellbender_output')
    os.makedirs(cellbender_output_dir, exist_ok=True)
    h5_out = os.path.join(cellbender_output_dir, "cellbender_output.h5")
    cb_cmd = [
        "cellbender", "remove-background",
        "--input", cellbender_input_dir,
        "--output", h5_out,
        "--expected-cells", str(expected_cells),
        "--epochs", str(epochs),
        "--fpr", str(fpr),
    ]
    if use_cuda:
        cb_cmd.append("--cuda")

    subprocess.run(cb_cmd, check=True)

    # Step 3: convert CellBender output back to mgatk-style
    sys.stderr.write(f"[mitobender] converting CellBender output\n")
    output_file = os.path.join(mgatk_dir, "mitobender_results.rds")
    conv_cmd = ["Rscript", conv_script, "-i", mgatk_dir, "-c", h5_out, "-o", output_file]
    subprocess.run(conv_cmd, check=True)

    sys.stderr.write(f"[mitobender] Finished background removal. Results in {output_file}\n")
