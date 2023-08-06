""" Helper functions for python-sigma-uq
"""
import os
from pathlib import Path
from importlib import import_module, util
import json
from appdirs import user_data_dir
import numpy as np
import adranis_sigma.uq.display_util as display_util
# Helper functions


def sigma_save_config(host, token):
    """ Saves the Sigma API url and token of the user
    to a file in a proper AppDir.
    If this specific file is found during import
    of the Sigma package, those values will be
    automatically loaded.

    Args:
        host (string): The URL of the SIGMA API endpoint
            that the user is authorized to connect to
        token (string): The token associated to the user

    Returns:
        string: (print friendly) Message related to the success of the
            operation
    """
    theDir = user_data_dir("Adranis-Sigma", "Sigma")
    # Create the folder if it doesn't exist
    Path(theDir).mkdir(parents=True, exist_ok=True)
    theFile = os.path.join(theDir, 'sigma_config.json')
    theConfig = {"host": host, "token": token}
    with open(theFile, 'w', encoding='UTF-8') as outfile:
        json.dump(theConfig, outfile)
    return f"Stored Sigma API configuration in {theFile}"


def sigma_load_config(verbose=False):
    # Loads the Sigma API url and token from the configuration file
    theDir = user_data_dir("Adranis-Sigma", "Sigma")
    theFile = os.path.join(theDir, 'sigma_config.json')
    if os.path.isfile(theFile):
        with open(theFile, 'r', encoding='UTF-8') as infile:
            theConfig = json.load(infile)
    else:
        theConfig = {"host": None, "token": None}
    if verbose:
        print(f"Loaded Sigma API configuration from file {theFile}.")
    return theConfig


def load_module(path, name):
    # Loads a module from a given path with a given name
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def jsonify_np_array(A):
    return A.tolist()


def getlines(fd):
    line = bytearray()
    c = None
    while True:
        c = fd.read(1)
        if c is None:
            return
        line += c
        if c == b'\n':
            yield str(line)
            del line[:]


def extract_json(input_string):
    # extracts the json raw sub-string from a string
    idx_start_candidates = [input_string.find('{'), input_string.find('[')]
    json_start = min(x for x in idx_start_candidates if x != -1)
    idx_end_candidates = [input_string.rfind('}'), input_string.rfind(']')]
    json_end = max(idx_end_candidates) + 1
    return input_string[json_start:json_end]


def function_eval(fun, X, Parameters=None):
    if callable(fun):
        return fun(X)
    else:
        # expecting the fun to be a string
        # we are expecting a syntax a.b.c (or longer) where a.b is the module and
        # c is the method
        X = np.array(X)
        method_sep = fun.rfind('.')
        the_module = import_module(fun[0:method_sep])
        the_method = getattr(the_module, fun[method_sep + 1:])
        if Parameters is None:
            return the_method(X)
        else:
            return the_method(X, Parameters)


def display(obj, theInterface, **kwargs):
    """Produces visualizations of UQ objects. Based on
    UQLab's uq_display.

    Args:
        obj (dict): a dictionary
            that is returned by Sigma API when a UQ object
            is created
        theInterface (CloudSession.interface): the interface
             of the cloud session

    Raises:
        ValueError: Unknown or Unsupported type of UQ object

    Returns:
        plotly figure: A handle to a plotly figure (e.g. fig)
        that can be visualized by `fig.show()`
    """
    if obj['Class'] == 'uq_input':
        # display input
        return display_util.Input(obj, theInterface, **kwargs)
    if obj['Class'] == 'uq_model':
        # display model
        if 'PCE' in obj:
            return display_util.PCE(obj)
        if 'Kriging' in obj:
            return display_util.Kriging(obj, theInterface)
        else:
            raise ValueError("Not yet implemented!")

    if obj['Class'] == 'uq_analysis':
        # display analysis
        print("Not yet implemented!")
