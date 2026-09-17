import pygame
import time
from algorithms.sorting_algorithm import SortingAlgorithm


class MergeSort(SortingAlgorithm):

    def sort(self):
        """Thực hiện Merge Sort."""
        self.is_running = True
        self.statistics.start_timer()
        data = self.array_data

        self._merge_sort_helper(data, 0, len(data) - 1)

        # Mark all as sorted
        for i in range(len(data)):
            self.visualizer.set_state(i, 'sorted')

        self.statistics.stop_timer()
        self.is_running = False

    def _merge_sort_helper(self, data, left, right):
        if not self.is_running:
            return

        if left < right:
            mid = (left + right) // 2
            self._merge_sort_helper(data, left, mid)
            self._merge_sort_helper(data, mid + 1, right)
            self._merge(data, left, mid, right)

    def _merge(self, data, left, mid, right):
        left_part = data[left:mid + 1]
        right_part = data[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            if not self.is_running:
                return

            self._wait_if_paused()

            self.visualizer.set_state(k, 'comparing')
            self.statistics.add_comparison()

            delay = max(1, 100 - self.speed)
            self._tick(delay)

            if left_part[i] <= right_part[j]:
                data[k] = left_part[i]
                i += 1
            else:
                data[k] = right_part[j]
                j += 1

            self.visualizer.set_state(k, 'merged')
            self.statistics.add_swap()
            k += 1

        while i < len(left_part):
            data[k] = left_part[i]
            self.visualizer.set_state(k, 'merged')
            i += 1
            k += 1

        while j < len(right_part):
            data[k] = right_part[j]
            self.visualizer.set_state(k, 'merged')
            j += 1
            k += 1