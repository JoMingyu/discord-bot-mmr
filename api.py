from abc import abstractmethod, ABC
from typing import Optional

import arrow
from pydantic import validator
from pydantic.main import BaseModel
from requests import get


def italic(text):
    return f"*{text}*"


def bold(text):
    return f"**{text}**"


def underlined(text):
    return f"__{text}__"


class Data(BaseModel):
    avg: int  # avg mmr
    err: int  # ± 오차범위
    closestRank: str
    percentile: int  # 하위 n%. 100 - percentile은 상위 %를 의미함
    # warn: bool  # 정확도 낮은 경우 True
    timestamp: int  # last calculate timestamp

    @property
    def timestamp_humanized(self) -> str:
        humanized = (
            arrow.get(self.timestamp)
            .humanize()
            .replace(" days", "일")
            .replace("a day", "1일")
            .replace(" hours", "시간")
            .replace("a hour", "1시간")
            .replace(" minutes", "분")
            .replace("a minute", "1분")
            .replace(" weeks", "주")
            .replace("a week", "1주")
            .replace(" ago", " 전")
        )

        return f"{humanized} 기준"

    def as_message(self) -> str:
        return f"""
{bold(self.avg)} ± {self.err} ({self.closestRank} 상위 {100 - self.percentile}%)
- {italic(self.timestamp_humanized)}
        """.strip()


class MMR(BaseModel):
    ranked: Optional[Data]  # 솔로랭크
    normal: Optional[Data]  # 일반게임
    ARAM: Optional[Data]  # 칼바람 나락

    def as_message(self):
        solo_rank = italic("N/A") if self.ranked is None else self.ranked.as_message()
        normal = italic("N/A") if self.normal is None else self.normal.as_message()
        aram = italic("N/A") if self.ARAM is None else self.ARAM.as_message()

        return f"""
솔로랭크
{solo_rank}

노말
{normal}

무작위 총력전
{aram}
        """.strip()

    @validator("*", pre=True)
    def validate_rank_data_not_available(cls, value: dict):
        if value["avg"] is None:
            return None

        return value


class MMRAPI(ABC):
    @abstractmethod
    def get_mmr_data(self, nickname) -> MMR:
        pass


class WhatIsMyMMRAPI(MMRAPI):
    def get_mmr_data(self, nickname) -> MMR:
        # TODO error handling - 닉네임 미발견

        resp = get(f"https://kr.whatismymmr.com/api/v1/summoner?name={nickname}")

        return MMR(**resp.json())
