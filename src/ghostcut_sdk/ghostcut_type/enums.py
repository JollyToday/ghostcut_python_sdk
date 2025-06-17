from enum import Enum


class Resolution(str, Enum):
    Res480p = "480p"
    Res720p = "720p"
    Res1080p = "1080p"


class NeedChineseOcclude(int, Enum):
    NoNeed = 0
    AutoStaticInpaint = 1
    ManulInaint = 2
    AutoDynamicInpaint = 3
    AutoStaticOcrTranslate = 11
    ManulOcrTranslate = 12
    AutoDynamicOcrTranslate = 13
    SubtitleExtract = 14

class RemoveBgAudio(int, Enum):
    NoNeed = 0
    RemoveAllBgAudio = 1
    KeepEffectSound = 2

 
