"""Define the default boring things

You modify the class' __get__ descriptor to effect changes!
"""
import re

from dataclasses import dataclass, field

from yacd import singleton, instancify, callify


@callify
@instancify
@singleton
@dataclass(frozen=True)
class DEFAULT_THINGS_CONSIDERED_BORING:
    """A capsule for the regex"""

    __regex : re.Pattern = field(default=re.compile(r'''
        (?:b(ed)?h(anger)?\svdr:)
        |
        (?:(dovecot)|(log)(\[\d+\])?:\simap)
        |
        (?:b(ed)?h(anger)?\sfirefox(\.desktop)?(\[\d+\])?:)
        |
        (?:b(ed)?h(anger)?\smp3fs(\[\d+\])?:)
        |
        (?:b(ed)?h(anger)?\scron.*:)
        |
        (?:failed\sto\scoldplug\sunifying.*:)
        |
        (?:b(ed)?h(anger)?\ssmartd.*:.*SMART\sUsage\sAttribute:\s194\sTemperature_Celsius\schanged\sfrom)
        |
        (?:EMITTING\sCHANGED\sfor)
        |
        (?:helper\(pid\s+\d+\):\scompleted\swith\sexit\scode\s0)
        |
        (?:helper\(pid\s+\d+\):\slaunched\sjob\sudisks-helper-ata-smart-collect\son)
        |
        (?:Refreshing\sATA\sSMART\sdata\sfor)
        |
        (?:dvb_frontend_get_frequency_limits)
        |
        (?:systemd\[1\]:\sCondition\scheck\sresulted\sin\s.+\sbeing\sskipped\.)
        |
        (?:gdm-x-session\[\d+\]:\s>\sWarning:\s+Could\snot\sresolve\skeysym\s\S+)
    ''', re.VERBOSE))

    def __call__(self) -> re.Pattern:
        return self.__regex

    def __str__(self):
        return self.__regex.pattern
