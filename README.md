telegram: [t.me/modox_dev](https://t.me/modox_dev)

<h2 align="center">About Me </h2>

```python
from typing import List, Dict, Tuple

class Human:
    def __init__(self):
        self.name = "Modox"
        self.role = "Developer"
        self.location = "France 🌍"

    def introduce(self) -> str:
        return f"Hi, I'm {self.name} 👋"


class Developer(Human):

    @property
    def about_me(self) -> Dict[str, str]:
        return {
            "name": "Modox",
            "username": "modox-dev",
            "role": "Reverse Engineering",
            "focus": "I code for fun"
        }

    @property
    def languages(self) -> List[str]:
        return [
            "English",
            "French",
            "Spanish"
        ]

    @property
    def code(self) -> Dict[str, List[str]]:
        return {
            "good": ["python", "verse"],
            "learning": ["javascript"]
        }

    @property
    def technologies(self) -> List[str]:
        return [
            "Discord BOT",
            "Reverse Engineering",
            "Automation"
        ]

    @property
    def setup(self) -> Dict[str, Dict[str, str]]:
        return {
            "desktop": {
                "cpu": "Intel",
                "gpu": "Nvidia",
                "ram": "64GB"
            }
        }

    def current_mission(self) -> str:
        return "Building, learning, breaking things and fixing them again 🚀"


if __name__ == "__main__":
    me = Developer()
    print(me.introduce())
```

<h2 align="center">Skills </h2>

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,javascript,unreal" />
  </a>
</p>
