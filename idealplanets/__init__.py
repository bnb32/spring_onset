"""Idealplanets module"""
import argparse


def cesm_argparse():
    """Parse args for running cesm"""
    parser = argparse.ArgumentParser(description="Run CESM")
    parser.add_argument('-case', default='./cases/aqua', type=str)
    parser.add_argument('-aqua', default=False, action='store_true')
    parser.add_argument('-drycore', default=False, action='store_true')
    parser.add_argument('-drycore_topo', default=False, action='store_true')
    parser.add_argument('-queue', default='regular')
    parser.add_argument('-cam', default=False, action='store_true')
    parser.add_argument('-stop_opt', default="none")
    parser.add_argument('-stop_n', default="-999")
    parser.add_argument('-run', default=False, action='store_true')
    parser.add_argument('-ntasks', default=128)
    parser.add_argument('-out_tstep', default=24)
    parser.add_argument('-walltime', default="5:00:00")
    parser.add_argument('-start_date', default="1980-03-15")
    parser.add_argument('-stop_date', default="19800414")
    parser.add_argument('-project', default=None)
    parser.add_argument('-data_dir', default=None)
    parser.add_argument('-sst_file', default=None)
    parser.add_argument('-topo_file', default=None)
    parser.add_argument('-tref_file', default=None)
    parser.add_argument('-cime_out_dir', default=None)
    parser.add_argument('-docn_stream_file',
                        default="user_docn.streams.txt.aquapfile")
    parser.add_argument('-docn_mode', default="sst_aquapfile")
    parser.add_argument('-rebuild', default=False, action='store_true')
    parser.add_argument('-config', required=True)
    return parser


def run_cesm_pipeline_argparse():
    """Parse args for running cesm pipeline, including anomaly injection"""
    parser = argparse.ArgumentParser(description="Run CESM pipeline")
    parser.add_argument('-anomaly_lat', type=float, default=30.0)
    parser.add_argument('-anomaly_lon', type=float, default=0.0)
    parser.add_argument('-anomaly_radius', type=float, default=10.0)
    parser.add_argument('-max_anomaly', type=float, default=5.0)
    parser.add_argument('-anomaly_type', default='zonal_band', type=str,
                        choices=['disk', 'zonal_band', 'meridional_band',
                                 'none'])
    parser.add_argument('-walltime', default="5:00:00")
    parser.add_argument('-out_tstep', default=24)
    parser.add_argument('-ndays', default=200, type=int)
    parser.add_argument('-start_date', default="1980-03-15")
    parser.add_argument('-control', default=False, action='store_true')
    parser.add_argument('-norun', default=False, action='store_true')
    parser.add_argument('-aqua', default=False, action='store_true')
    parser.add_argument('-drycore', default=False, action='store_true')
    parser.add_argument('-lapse_rate', default=False, action='store_true')
    parser.add_argument('-surface', default=False, action='store_true')
    parser.add_argument('-drycore_topo', default=False, action='store_true')
    parser.add_argument('-ntasks', type=int, default=128)
    parser.add_argument('-rebuild', default=False, action='store_true')
    parser.add_argument('-config', required=True)
    return parser


def run_batch_argparse():
    """Parse args for running multiple instances of cesm pipeline"""
    parser = argparse.ArgumentParser(
        description="Run Multiple Instances of CESM Pipeline")
    parser.add_argument('-case', default='aqua_anomaly')
    parser.add_argument('-anomaly_lat_min', type=float, default=10.0)
    parser.add_argument('-anomaly_lat_max', type=float, default=50.0)
    parser.add_argument('-anomaly_lon', type=float, default=180.0)
    parser.add_argument('-anomaly_lat_increment', type=float, default=5.0)
    parser.add_argument('-max_anomaly', type=float, default=5.0)
    parser.add_argument('-anomaly_radius_squared', type=float, default=20.0)
    parser.add_argument('-anomaly_type', default='zonal_band', type=str)
    parser.add_argument('-sims', default=False, action='store_true')
    parser.add_argument('-config', required=True)
    return parser


def plot_steadystate_argparse():
    """Parse args for steadystate plot"""
    parser = argparse.ArgumentParser(description="Plot CESM Steadystate")
    parser.add_argument('-infile', required=True, type=str)
    parser.add_argument('-outdir', default=None)
    parser.add_argument('-field', default="KE", type=str)
    parser.add_argument('-level', default=250, type=int)
    parser.add_argument('-drycore', default=False, action='store_true')
    parser.add_argument('-aqua', default=False, action='store_true')
    parser.add_argument('-config', required=True)
    return parser


def plot_spectrum_argparse():
    """Parse args for spectrum plot"""
    parser = argparse.ArgumentParser(description="Plot CESM Spectrum")
    parser.add_argument('-infile', required=True, type=str)
    parser.add_argument('-outdir', default=None)
    parser.add_argument('-field', default="Z3", type=str)
    parser.add_argument('-level', default=250, type=int)
    parser.add_argument('-drycore', default=False, action='store_true')
    parser.add_argument('-aqua', default=False, action='store_true')
    parser.add_argument('-anomaly', default=False, action='store_true')
    parser.add_argument('-control', default=False, action='store_true')
    parser.add_argument('-config', required=True)
    return parser


def inject_argparse():
    """Parse args for anomaly injection"""
    parser = argparse.ArgumentParser(description="Inject Anomaly")
    parser.add_argument('-aqua', default=False, action='store_true')
    parser.add_argument('-drycore', default=False, action='store_true')
    parser.add_argument('-drycore_topo', default=False, action='store_true')
    parser.add_argument('-lapse_rate', default=False, action='store_true')
    parser.add_argument('-surface', default=False, action='store_true')
    parser.add_argument('-data_dir', default=None)
    parser.add_argument('-sst_file', default=None)
    parser.add_argument('-topo_file', default=None)
    parser.add_argument('-tref_file', default=None)
    parser.add_argument('-sst_outfile', default=None)
    parser.add_argument('-topo_outfile', default=None)
    parser.add_argument('-tref_outfile', default=None)
    parser.add_argument('-anomaly_type', default='zonal_band', type=str,
                        choices=['disk', 'zonal_band', 'meridional_band',
                                 'none'])
    parser.add_argument('-max_anomaly', type=float, default=5.0)
    parser.add_argument('-anomaly_radius', type=float, default=5.0)
    parser.add_argument('-anomaly_lat', type=float, default=30.0)
    parser.add_argument('-anomaly_lon', type=float, default=0.0)
    parser.add_argument('-config', required=True)
    return parser
