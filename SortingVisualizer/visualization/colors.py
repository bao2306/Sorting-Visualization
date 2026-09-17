"""
Quản lý các màu sắc dùng trong visualization.
Mỗi trạng thái có một màu riêng.
"""


class Colors:
    """Lớp chứa các hằng số màu sắc (RGB)."""

    # Màu cơ bản
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)

    # Trạng thái sắp xếp
    DEFAULT = (52, 152, 219)  # Xanh dương - Bình thường
    COMPARING = (231, 76, 60)  # Đỏ - Đang so sánh
    SWAPPING = (241, 196, 15)  # Vàng - Đang đổi chỗ
    SORTED = (46, 204, 113)  # Xanh lá - Đã sắp xếp
    PIVOT = (230, 126, 34)  # Cam - Pivot (dùng cho QuickSort)
    MERGED = (155, 89, 182)  # Tím - Đã merge (dùng cho MergeSort)

    # Màu chữ
    TEXT_COLOR = (255, 255, 255)
    TEXT_DARK = (0, 0, 0)

    # Màu nền
    BACKGROUND = (44, 62, 80)  # Xám đen
    BUTTON_COLOR = (52, 152, 219)  # Xanh dương
    BUTTON_HOVER = (41, 128, 185)  # Xanh dương đậm
    BUTTON_ACTIVE = (231, 76, 60)  # Đỏ

    @staticmethod
    def get_color_by_state(state):
        """
        Lấy màu theo trạng thái.

        Args:
            state (str): Trạng thái ('default', 'comparing', 'swapping', 'sorted', 'pivot', 'merged')

        Returns:
            tuple: Màu RGB
        """
        states = {
            'default': Colors.DEFAULT,
            'comparing': Colors.COMPARING,
            'swapping': Colors.SWAPPING,
            'sorted': Colors.SORTED,
            'pivot': Colors.PIVOT,
            'merged': Colors.MERGED,
        }
        return states.get(state, Colors.DEFAULT)