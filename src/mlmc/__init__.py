"""
l2hmc/__init__.py
"""
from __future__ import absolute_import, annotations, division, print_function
import logging
import os
from typing import Optional
import warnings

from mpi4py import MPI
# from rich.logging import RichHandler
# from l2hmc.utils.enrich import EnRichHandler
from enrich.logging import RichHandler
import tqdm

warnings.filterwarnings('ignore')

os.environ['PYTHONIOENCODING'] = 'utf-8'

RANK = int(MPI.COMM_WORLD.Get_rank())
WORLD_SIZE = int(MPI.COMM_WORLD.Get_size())


def get_logger(
        name: Optional[str] = None,
        level: str = 'INFO',
        rank: int = 0,
        world_size: int = 1,
        rank_zero_only: bool = True,
        **kwargs,
) -> logging.Logger:
    # logging.basicConfig(stream=DummyTqdmFile(sys.stderr))
    log = logging.getLogger(name)
    from enrich.console import Console, get_theme
    from enrich.logging import RichHandler
    # log.handlers = []
    # from rich.logging import RichHandler
    # from l2hmc.utils.rich import get_console, is_interactive
    theme = get_theme()
    console = Console(theme=theme, log_path=False, markup=True)
    import os

    from rich.console import Console as rConsole
    os.environ['COLORTERM'] = 'truecolor'
    from rich.console import Console as rConsole
    rconsole = rConsole(theme=theme, log_path=False, markup=True)
    # format = "[%(asctime)s][%(name)s][%(levelname)s] - %(message)s"
    if rank_zero_only:
        if rank != 0:
            log.setLevel('CRITICAL')
        else:
            log.setLevel(level)
    if rank == 0:
        # console = get_console(
        #     markup=True,  # (WORLD_SIZE == 1),
        #     redirect=(world_size > 1),
        #     # file=outfile,
        #     **kwargs
        # )
        if console.is_jupyter:
            console.is_jupyter = False
        # log.propagate = True
        # log.handlers = []
        # use_markup = (
        #     WORLD_SIZE == 1
        #     and not is_interactive()
        # )
        log.addHandler(
            RichHandler(
                omit_repeated_times=False,
                level=level,
                console=console,
                show_time=True,
                show_level=True,
                show_path=False,
                # tracebacks_width=120,
                markup=True,
                enable_link_path=True,
                # keywords=['loss=', 'dt=', 'Saving']
            )
        )
        log.setLevel(level)
    if (
            len(log.handlers) > 1 
            and all([i == log.handlers[0] for i in log.handlers])
    ):
        log.handlers = [log.handlers[0]]
    return log
