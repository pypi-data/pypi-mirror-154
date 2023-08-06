import asyncio
import logging
import typer

from atlas_engine_client.external_task import ExternalTaskClient

from ..configuration import ConfigAccessor
from . import check_running_process_instance

logger = logging.getLogger('processcube_sdk')

app = typer.Typer()


def setup_logging(log_level=logging.INFO):
    
    format_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=format_template)

    return logging.getLogger()

def start_external_task(loop=None):
    ConfigAccessor.ensure_from_env()
    config = ConfigAccessor.current()

    engine_url = config.get('engine', 'url')

    client = ExternalTaskClient(engine_url, loop=loop)

    handler_factories = [
        check_running_process_instance,
    ]

    for factory in handler_factories:
        handler = factory.create_external_task(config)
        logger.info(f"Starting external task worker for topic '{handler.get_topic()}'")
        if loop is None:
            client.subscribe_to_external_task_for_topic(handler.get_topic(), handler)
        else:
            client.subscribe_to_external_task_for_topic(handler.get_topic(), handler, loop=loop)

    if loop is None:
        client.start()
    else:
        client.start(run_forever=False)


@app.command()
def external_task():
    setup_logging()
    start_external_task()

@app.callback(invoke_without_command=True)
def default():

    setup_logging()
    start_external_task()

if __name__ == '__main__':
    app()