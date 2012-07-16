# Copyright (C) 2012 Google, Inc.
# Copyright (C) 2010 Chris Jerdonek (cjerdonek@webkit.org)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1.  Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# 2.  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
import re
import StringIO

from webkitpy.common.system import outputcapture

_log = logging.getLogger(__name__)


class Printer(object):
    def __init__(self, stream, options=None):
        self.stream = stream
        self.options = options
        self.test_description = re.compile("(\w+) \(([\w.]+)\)")

    def test_name(self, test):
        m = self.test_description.match(str(test))
        return "%s.%s" % (m.group(2), m.group(1))

    def configure(self, options):
        self.options = options

        if options.timing:
            # --timing implies --verbose
            options.verbose = max(options.verbose, 1)

        log_level = logging.INFO
        if options.quiet:
            log_level = logging.WARNING
        elif options.verbose == 2:
            log_level = logging.DEBUG

        handler = logging.StreamHandler(self.stream)
        # We constrain the level on the handler rather than on the root
        # logger itself.  This is probably better because the handler is
        # configured and known only to this module, whereas the root logger
        # is an object shared (and potentially modified) by many modules.
        # Modifying the handler, then, is less intrusive and less likely to
        # interfere with modifications made by other modules (e.g. in unit
        # tests).
        handler.name = __name__
        handler.setLevel(log_level)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.addHandler(handler)
        logger.setLevel(logging.NOTSET)

        # Filter out most webkitpy messages.
        #
        # Messages can be selectively re-enabled for this script by updating
        # this method accordingly.
        def filter_records(record):
            """Filter out autoinstall and non-third-party webkitpy messages."""
            # FIXME: Figure out a way not to use strings here, for example by
            #        using syntax like webkitpy.test.__name__.  We want to be
            #        sure not to import any non-Python 2.4 code, though, until
            #        after the version-checking code has executed.
            if (record.name.startswith("webkitpy.common.system.autoinstall") or
                record.name.startswith("webkitpy.test")):
                return True
            if record.name.startswith("webkitpy"):
                return False
            return True

        testing_filter = logging.Filter()
        testing_filter.filter = filter_records

        # Display a message so developers are not mystified as to why
        # logging does not work in the unit tests.
        _log.info("Suppressing most webkitpy logging while running unit tests.")
        handler.addFilter(testing_filter)

        if self.options.pass_through:
            outputcapture.OutputCapture.stream_wrapper = _CaptureAndPassThroughStream

    def print_started_test(self, test_name):
        if self.options.verbose:
            self.stream.write(test_name)

    def print_finished_test(self, result, test_name, test_time, failure, err):
        timing = ''
        if self.options.timing:
            timing = ' %.4fs' % test_time
        if self.options.verbose:
            if failure:
                msg = ' failed'
            elif err:
                msg = ' erred'
            else:
                msg = ' passed'
            self.stream.write(msg + timing + '\n')
        else:
            if failure:
                msg = 'F'
            elif err:
                msg = 'E'
            else:
                msg = '.'
            self.stream.write(msg)

    def print_result(self, result, run_time):
        self.stream.write('\n')

        for (test, err) in result.errors:
            self.stream.write("=" * 80 + '\n')
            self.stream.write("ERROR: " + self.test_name(test) + '\n')
            self.stream.write("-" * 80 + '\n')
            for line in err.splitlines():
                self.stream.write(line + '\n')
            self.stream.write('\n')

        for (test, failure) in result.failures:
            self.stream.write("=" * 80 + '\n')
            self.stream.write("FAILURE: " + self.test_name(test) + '\n')
            self.stream.write("-" * 80 + '\n')
            for line in failure.splitlines():
                self.stream.write(line + '\n')
            self.stream.write('\n')

        self.stream.write('-' * 80 + '\n')
        self.stream.write('Ran %d test%s in %.3fs\n' %
            (result.testsRun, result.testsRun != 1 and "s" or "", run_time))

        if result.wasSuccessful():
            self.stream.write('\nOK\n')
        else:
            self.stream.write('FAILED (failures=%d, errors=%d)\n' %
                (len(result.failures), len(result.errors)))


class _CaptureAndPassThroughStream(object):
    def __init__(self, stream):
        self._buffer = StringIO.StringIO()
        self._stream = stream

    def write(self, msg):
        self._stream.write(msg)

        # Note that we don't want to capture any output generated by the debugger
        # because that could cause the results of capture_output() to be invalid.
        if not self._message_is_from_pdb():
            self._buffer.write(msg)

    def _message_is_from_pdb(self):
        # We will assume that if the pdb module is in the stack then the output
        # is being generated by the python debugger (or the user calling something
        # from inside the debugger).
        import inspect
        import pdb
        stack = inspect.stack()
        return any(frame[1] == pdb.__file__.replace('.pyc', '.py') for frame in stack)

    def flush(self):
        self._stream.flush()

    def getvalue(self):
        return self._buffer.getvalue()
