import pytest
import inspect

from . import replacer


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        '--spec2md',
        action='store_true',
        dest='spec2md',
        help='Saves test results as specification document in markdown format.'
    )

    # register config options
    parser.addini(
        'spec_target_file',
        default='documentation/spec.md',
        help='The target file to save the generated specification.'
    )

    parser.addini(
        'spec_indent',
        default='  ',
        help='Indention of spec in console.'
    )


def pytest_configure(config):
    if getattr(config.option, 'spec2md', 0):
        use_terminal = not getattr(config.option, 'quiet', 0) and not getattr(config.option, 'verbose', 0)

        import six
        import _pytest
        import _pytest.terminal

        config.addinivalue_line(
            "markers", "spec_reference(name): mark specification reference for the test"
        )

        _pytest.terminal.TerminalReporter.pytest_runtest_logstart = replacer.logstart
        _pytest.terminal.TerminalReporter.pytest_runtest_logreport = \
            replacer.report_on_terminal if use_terminal else replacer.report_no_terminal
        _pytest.terminal.TerminalReporter.pytest_collection_modifyitems = replacer.modify_items
        six.moves.reload_module(_pytest)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Adds docstring to the item usage in report"""
    outcome = yield
    report = outcome.get_result()
    node = getattr(item, 'obj', None)
    if node:
        report.node = node
        report.docstring_summary = str(node.__doc__) if node.__doc__ else ''
        report.docstring_parent = _get_parent_doc(node)
        for marker in item.iter_markers_with_node(name='spec_reference'):
            report.reference_doc = marker[1].args


def _get_parent_doc(function):
    func = getattr(function, "__self__", None)
    if not func:
        return ""
    parent = getattr(func, "__class__", None)
    if not parent:
        return ""

    doc = inspect.getdoc(parent)
    return doc if doc is not None else ""
