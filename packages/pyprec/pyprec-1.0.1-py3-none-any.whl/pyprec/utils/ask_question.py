import six
import signal
from typing import Callable
from logging import Logger
from .utils import colorize


class TimeOutError(Exception):
    """Class for run-time error"""


def question_instance(logger: Logger, question: str, default: str) -> str:
    """Asks for user input.

    Parameters
    ----------
    logger: Logger
        The logger instance.
    question: str
        The question to ask.
    default: str
        The default answer.

    Returns
    -------
    str
        The user answer to the question.
    """
    colored_question = colorize(question, "magenta")
    while True:
        result = input(colored_question).lower()
        if not result:
            result = default
        # keep asking only if result is not valid, but answer is required
        if result:
            break
        logger.info("Required field, please try again ...")
    return result


def timed_input(
    logger: Logger,
    question: str,
    default: str,
    timeout: float = None,
    noerror: bool = True,
    fct: Callable = None,
) -> str:
    """Poses a question with a maximal time to answer.

    Default answer is taken if maximal time is reached.

    Parameters
    ----------
    logger: Logger
        The logger instance.
    question: str
        The question to ask.
    default: str
        The default answer.
    timeout: float
        Time limit to answer in seconds.
    noerror: bool
        Wether to raise error on TimeOutError exception.
    fct: Callable
        The callable effectively asking the question.

    Returns
    -------
    str
        The user answer to the question.
    """

    def handle_alarm(signum, frame):
        raise TimeOutError

    signal.signal(signal.SIGALRM, handle_alarm)

    if fct is None:
        fct = six.moves.input

    if timeout:
        signal.alarm(timeout)
    try:
        result = fct(logger, question, default)
    except TimeOutError:
        if noerror:
            logger.info("use %s" % default)
            return default
        else:
            signal.alarm(0)
            raise
    finally:
        signal.alarm(0)
    return result


def ask_question(
    logger: Logger, question: str, default: str, timeout: float = 10
) -> str:
    """Asks question to user.

    User has only `timeout` seconds to answer, then the `default` is returned.

    Parameters
    ----------
    logger: Logger
        The logger instance.
    question: str
        The question to ask.
    default: str
        The default answer.
    timeout: float
        Time limit to answer in seconds.

    Returns
    -------
    str
        The user answer to the question.
    """
    value = timed_input(
        logger, question, default, timeout=timeout, fct=question_instance
    )
    return value
