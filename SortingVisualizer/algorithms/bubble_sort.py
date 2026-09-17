import pygame
import time
from algorithms.sorting_algorithm import SortingAlgorithm


class BubbleSort(SortingAlgorithm):

    def sort(self):
        self.is_running = True
        self.statistics.start_timer()
        data = self.array_data
        n = len(data)

        for i in range(n):
            if not self.is_running:
                break

            swapped = False
            for j in range(0, n - i - 1):
                if not self.is_running:
                    break

                self._wait_if_paused()

                # Highlight các phần tử đang so sánh
                self.visualizer.set_state(j, 'comparing')
                self.visualizer.set_state(j + 1, 'comparing')
                self.statistics.add_comparison()

                # Delay dựa trên tốc độ
                delay = max(1, 100 - self.speed)
                self._tick(delay)

                if data[j] > data[j + 1]:
                    # Hoán đổi
                    data[j], data[j + 1] = data[j + 1], data[j]
                    self.visualizer.set_state(j, 'swapping')
                    self.visualizer.set_state(j + 1, 'swapping')
                    self.statistics.add_swap()
                    swapped = True
                    self._tick(delay)

                # Reset trạng thái
                self.visualizer.set_state(j, 'default')
                self.visualizer.set_state(j + 1, 'default')

            # Mark sorted elements
            self.visualizer.set_state(n - i - 1, 'sorted')

            if not swapped:
                break

        # Mark all as sorted
        for i in range(n):
            self.visualizer.set_state(i, 'sorted')

        self.statistics.stop_timer()
        self.is_running = False