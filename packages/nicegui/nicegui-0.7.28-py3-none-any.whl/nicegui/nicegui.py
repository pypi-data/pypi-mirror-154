#!/usr/bin/env python3
# isort:skip_file
from typing import Awaitable, Callable

from .ui import Ui  # NOTE: before justpy
import justpy as jp

from . import binding, globals
from .task_logger import create_task
from .timer import Timer


@jp.app.on_event('startup')
def startup():
    globals.tasks.extend(create_task(t.coro, name=t.name) for t in Timer.prepared_coroutines)
    Timer.prepared_coroutines.clear()
    globals.tasks.extend(create_task(t, name='startup task') for t in Ui.startup_tasks if isinstance(t, Awaitable))
    [safe_invoke(t) for t in Ui.startup_tasks if isinstance(t, Callable)]
    jp.run_task(binding.loop())


@jp.app.on_event('shutdown')
def shutdown():
    [create_task(t, name='shutdown task') for t in Ui.shutdown_tasks if isinstance(t, Awaitable)]
    [safe_invoke(t) for t in Ui.shutdown_tasks if isinstance(t, Callable)]
    [t.cancel() for t in globals.tasks]


def safe_invoke(func: Callable):
    try:
        func()
    except:
        globals.log.exception(f'could not invoke {func}')


app = globals.app = jp.app
ui = Ui()

page = ui.page('/', classes=globals.config.main_page_classes)
page.__enter__()
jp.justpy(lambda: page, start_server=False)
