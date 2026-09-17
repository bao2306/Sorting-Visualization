import pygame
import time
from algorithms.sorting_algorithm import SortingAlgorithm


class QuickSort(SortingAlgorithm):

    def sort(self):
        """Thực hiện Quick Sort."""
        self.is_running = True
        self.statistics.start_timer()
        data = self.array_data

        self._quick_sort_helper(data, 0, len(data) - 1)

        # Mark all as sorted
        for i in range(len(data)):
            self.visualizer.set_state(i, 'sorted')

        self.statistics.stop_timer()
        self.is_running = False

    def _quick_sort_helper(self, data, low, high):

        if not self.is_running:
            return

        if low < high:
            pivot_index = self._partition(data, low, high)
            self._quick_sort_helper(data, low, pivot_index - 1)
            self._quick_sort_helper(data, pivot_index + 1, high)

    def _partition(self, data, low, high):

        pivot = data[high]
        self.visualizer.set_state(high, 'pivot')
        i = low - 1

        for j in range(low, high):
            if not self.is_running:
                break

            self._wait_if_paused()

            self.visualizer.set_state(j, 'comparing')
            self.statistics.add_comparison()

            delay = max(1, 100 - self.speed)
            self._tick(delay)

            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                self.visualizer.set_state(i, 'swapping')
                self.visualizer.set_state(j, 'swapping')
                self.statistics.add_swap()
                self._tick(delay)

            self.visualizer.set_state(j, 'default')

        data[i + 1], data[high] = data[high], data[i + 1]
        self.visualizer.set_state(i + 1, 'default')
        self.visualizer.set_state(high, 'default')
        self.statistics.add_swap()

        return i + 1 #Returns:int: Vị trí pivot