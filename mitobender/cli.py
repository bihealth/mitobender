import click
from .runner import run_remove_background

@click.group()
def cli():
    """mitobender: remove ambient mtDNA background from mgatk results"""
    pass

@cli.command("remove-background")
@click.option("--mgatk-dir", "-m", required=True, type=click.Path(exists=True),
              help="mgatk final output directory.")
@click.option("--expected-cells", type=int, required=True,
              help="Number of expected cells for CellBender.")
@click.option("--epochs", type=int, default=150, show_default=True,
              help="Number of training epochs for CellBender.")
@click.option("--fpr", type=float, default=0.01, show_default=True,
              help="False positive rate for CellBender.")
@click.option("--cuda", default=False,
              help="Run CellBender on GPU (CUDA) if available.")
# Arguments for prepare_cellbender.R
@click.option("--n-cells-conf-detected", type=int, default=None,
              help="Number of confidently detected cells (for R prep).")
@click.option("--strand-correlation", type=float, default=None,
              help="Strand correlation (for R prep).")
@click.option("--vmr", type=float, default=None,
              help="Variance-to-mean ratio (for R prep).")
@click.option("--variable-sites", type=click.Path(exists=True), default=None,
              help="Path to text file listing variable sites (for R prep).")

def remove_background(mgatk_dir, expected_cells, epochs, fpr, cuda,
                      n_cells_conf_detected, strand_correlation, vmr, variable_sites):
    """Run ambient mtDNA background removal."""
    run_remove_background(
        mgatk_dir=mgatk_dir,
        expected_cells=expected_cells,
        epochs=epochs,
        fpr=fpr,
        use_cuda=cuda,
        n_cells_conf_detected=n_cells_conf_detected,
        strand_correlation=strand_correlation,
        vmr=vmr,
        variable_sites=variable_sites
    )
