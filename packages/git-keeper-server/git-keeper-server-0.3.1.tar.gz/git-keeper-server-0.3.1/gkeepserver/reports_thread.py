# Copyright 2022 Nathan Sommer and Ben Coleman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Provides a thread that writes the results of assignment tests into a reports
repository.
"""

from queue import Queue, Empty
from threading import Thread
from time import time


class ReportsThread(Thread):
    def __init__(self):
        Thread.__init__(self)

        self._reports_queue = Queue()
        self._shutdown_flag = False

    def enqueue_report(self, report):
        pass
