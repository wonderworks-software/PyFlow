## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


import asyncio


_PYFLOW_EVENT_LOOP = None


def get_or_create_event_loop():
    global _PYFLOW_EVENT_LOOP

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is not None:
        _PYFLOW_EVENT_LOOP = loop
        return loop

    if _PYFLOW_EVENT_LOOP is None or _PYFLOW_EVENT_LOOP.is_closed():
        _PYFLOW_EVENT_LOOP = asyncio.new_event_loop()

    asyncio.set_event_loop(_PYFLOW_EVENT_LOOP)
    return _PYFLOW_EVENT_LOOP


def close_event_loop():
    global _PYFLOW_EVENT_LOOP

    loop = _PYFLOW_EVENT_LOOP
    _PYFLOW_EVENT_LOOP = None

    if loop is None:
        asyncio.set_event_loop(None)
        return

    if not loop.is_closed():
        pending = [task for task in asyncio.all_tasks(loop) if not task.done()]
        for task in pending:
            task.cancel()
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        loop.close()

    asyncio.set_event_loop(None)
