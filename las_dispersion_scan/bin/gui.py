"""The main laser dispersion scan GUI."""

import argparse
import logging
import signal
import sys
from typing import List, Optional

import matplotlib
import matplotlib.pyplot as plt
import typhos
from pydm.exception import install as install_exception_handler
from qtpy import QtWidgets

from .. import utils
from ..loader import Loader
from ..widgets import DscanMain

DESCRIPTION = __doc__
logger = logging.getLogger(__name__)


def _sigint_handler(signal, frame):
    logger.info("Caught Ctrl-C (SIGINT); exiting.")
    sys.exit(1)


def _configure_stylesheet(paths: Optional[List[str]] = None) -> str:
    """
    Configure stylesheets for the d-scan GUI.

    Parameters
    ----------
    paths : List[str], optional
        A list of paths to stylesheets to load.
        Defaults to those packaged in las-dispersion-scan.

    Returns
    -------
    str
        The full stylesheet.
    """
    app = QtWidgets.QApplication.instance()
    typhos.use_stylesheet()

    if paths is None:
        paths = [
            str(utils.SOURCE_PATH / "ui" / "stylesheet.qss"),
            str(utils.SOURCE_PATH / "ui" / "pydm.qss"),
        ]

    stylesheets = [app.styleSheet()]

    for path in paths:
        with open(path, "rt") as fp:
            stylesheets.append(fp.read())

    full_stylesheet = "\n\n".join(stylesheets)

    app.setStyleSheet(full_stylesheet)
    return full_stylesheet


def configure_ophyd():
    """Configure ophyd defaults."""
    from ophyd.signal import EpicsSignalBase

    EpicsSignalBase.set_defaults(
        timeout=10.0,
        connection_timeout=10.0,
        auto_monitor=True,
    )


def build_arg_parser(argparser=None):
    if argparser is None:
        argparser = argparse.ArgumentParser()

    argparser.description = DESCRIPTION
    argparser.formatter_class = argparse.RawTextHelpFormatter

    argparser.add_argument(
        "--prefix",
        type=str,
        help="The scan status prefix to use (see las_dispersion_scan.loader.DscanStatus)",
    )

    argparser.add_argument(
        "--script",
        type=str,
        help=(
            "Script that defines the stage and spectrometer instances, if available. "
            "This is a module name and not a path.  The usual Python import "
            "mechanism will be used. "
        ),
    )

    argparser.add_argument(
        "--stage",
        type=str,
        help=(
            "The stage name to load from happi.  "
            "This overrides the stage loaded from the script, if specified."
        ),
    )

    argparser.add_argument(
        "--spectrometer",
        type=str,
        help=(
            "The spectrometer name to load from happi.  "
            "This overrides the spectrometer loaded from the script, if specified."
        ),
    )

    argparser.add_argument(
        "--debug",
        action="store_true",
        help=(
            "Enable debug mode: numpy random seed set at each retrieval and "
            "IPython console if the retrieval process raises"
        ),
    )

    argparser.add_argument(
        "--load", dest="data_path", type=str, help="Load a data file at the start"
    )

    return argparser


def main(
    screen: str = "main",
    stylesheet: Optional[str] = None,
    prefix: Optional[str] = None,
    script: Optional[str] = None,
    stage: Optional[str] = None,
    spectrometer: Optional[str] = None,
    data_path: Optional[str] = None,
    debug: bool = False,
) -> None:
    """
    Launch the d-scan GUI.

    Parameters
    ----------
    screen : str, optional
        The screen to load.  Defaults to the primary GUI screen ("main")
    stylesheet : str, optional
        A stylesheet to use in place of the built-in ones.
    prefix : str, optional
        Prefix for the scan status PVs.
    script : str, optional
        Script that defines the stage and spectrometer instances, if available.
        This is a module name and not a path.  The usual Python import
        mechanism will be used.
    stage : str, optional
        Motor name from the happi database.  Overrides the script-provided
        settings if specified.
    spectrometer : str, optional
        Spectrometer name from the happi database. Overrides the
        script-provided settings if specified.
    data_path : str, optional
        File to load when the GUI opens.
    """

    if script is not None and ("/" in script or "\\" in script):
        raise ValueError(
            f"Script is expected to be a Python module name, not a path: " f"{script!r}"
        )

    signal.signal(signal.SIGINT, _sigint_handler)
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    install_exception_handler()
    configure_ophyd()

    try:
        _configure_stylesheet(paths=[stylesheet] if stylesheet else None)
    except Exception:
        logger.exception("Failed to load stylesheet; things may look odd...")

    try:
        matplotlib.use("Qt5Agg")
    except Exception:
        logger.warning("Unable to select the qt5 backend for matplotlib", exc_info=True)
    plt.ion()

    app.setOrganizationName("SLAC National Accelerator Laboratory")
    app.setApplicationName("las-dispersion-scan")

    loader = Loader(
        script=script,
        stage=stage,
        spectrometer=spectrometer,
        prefix=prefix,
    )
    try:
        if screen == "main":
            widget = DscanMain(loader=loader, debug=debug)
            if data_path is not None:
                widget.load_path(data_path)
        else:
            raise ValueError(f"Unexpected screen type: {screen}")
        widget.show()
    except Exception:
        logger.exception("Failed to load user interface")
        raise
    app.exec_()


if __name__ == "__main__":
    main()
