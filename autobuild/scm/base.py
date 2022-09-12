from __future__ import annotations

from datetime import datetime
from typing import NamedTuple, Union


def date() -> str:
    return datetime.now().strftime("%Y%m%d")


class Semver(NamedTuple):
    major: int
    minor: int
    patch: int
    prerelease: str

    @property
    def next(self) -> "Semver":
        return Semver(
            major=self.major,
            minor=self.minor,
            patch=self.patch if self.prerelease else self.patch + 1,
            prerelease=None,
        )

    def __str__(self) -> str:
        if self.prerelease:
            return f"{self.major}.{self.minor}.{self.patch}-{self.prerelease}"
        return f"{self.major}.{self.minor}.{self.patch}"

    @staticmethod
    def parse(v: str) -> Union[None, "Semver"]:
        if v.startswith("v"):
            v = v[1:]

        split = v.split(".")

        # Extract pre-release
        last = split[-1]
        prerelease = None
        try:
            prerelease_idx = last.index("-")
            prerelease = last[prerelease_idx+1:]
            split[-1] = last[:prerelease_idx]
        except ValueError:
            pass

        # Populate all version numbers, even if only one or two is provided, ex. v1 or v1.0
        try:
            major, minor, patch = (int(split[i]) if i < len(split) else 0 for i in range(3))
        except ValueError:
            return None

        return Semver(
            major=major,
            minor=minor,
            patch=patch,
            prerelease=prerelease,
        )

