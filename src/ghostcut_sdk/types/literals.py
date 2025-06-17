from typing import Literal

Resolution = Literal["480p", "720p", "1080p"]
NeedChineseOcclude = Literal[0, 1, 2]


def test_need_chinese_occlude(x: NeedChineseOcclude, resulution: Resolution):
    print(f"{x=}")

