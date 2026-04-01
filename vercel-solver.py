import hashlib
import base64
import secrets
from dataclasses import dataclass
import curl_cffi.requests

@dataclass
class ChallengeData:
    request_id: int
    difficulty: int
    seed_main: str
    seed_pattern: str
    iterations: int

class VercelBypass:
    FACTORS = (498787, 533737, 619763, 708403, 828071)

    def __init__(self, proxy: str | None = None):
        self.client = curl_cffi.requests.Session(impersonate="chrome136")

        if proxy:
            self.client.proxies = {"all": proxy}

        self.client.headers = self._default_headers()

    def _default_headers(self) -> dict:
        return {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/142.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
        }

    def fetch_challenge(self, url: str) -> tuple[str, str]:
        res = self.client.get(url)
        return res.text, res.headers.get("x-vercel-challenge-token")

    def decode_token(self, token: str) -> ChallengeData:
        parts = token.split(".")
        payload = base64.b64decode(parts[3]).split(b";")

        return ChallengeData(
            request_id=int(parts[1]),
            difficulty=int(parts[2]),
            seed_main=payload[1].decode(),
            seed_pattern=payload[2].decode(),
            iterations=int(payload[3]),
        )

    def generate_nonce(self, base: str, prefix: str) -> tuple[str, str]:
        while True:
            n = secrets.token_hex(8)
            h = hashlib.sha256((base + n).encode()).hexdigest()
            if h.startswith(prefix):
                return n, h

    def compute_solution(self, data: ChallengeData) -> str:
        results = []
        last_hash = ""

        start_index = (data.request_id * self.FACTORS[data.request_id % 5]) % 36

        for i in range(data.iterations):
            if i == 0:
                target = data.seed_pattern[start_index:start_index + 4]
            else:
                shift = (data.request_id * self.FACTORS[(i - 1) % 5]) % data.difficulty
                target = last_hash[shift:shift + 4]

            nonce, last_hash = self.generate_nonce(data.seed_main, target)
            results.append(nonce)

        return ";".join(results)

    def send_solution(self, base_url: str, token: str, solution: str) -> int:
        root = base_url.rstrip("/")

        self.client.headers.update({
            "x-vercel-challenge-token": token,
            "x-vercel-challenge-solution": solution,
            "x-vercel-challenge-version": "2",
            "origin": root,
            "referer": f"{root}/.well-known/vercel/security/static/challenge.v2.min.js",
        })

        res = self.client.post(f"{root}/.well-known/vercel/security/request-challenge")
        return res.status_code

    def run(self, url: str) -> None:
        _, token = self.fetch_challenge(url)

        if not token:
            print("No challenge detected.")
            return

        data = self.decode_token(token)
        solution = self.compute_solution(data)

        status = self.send_solution(url, token, solution)
        print("Challenge response:", status)

        final = self.client.get(url)
        print("Final status:", final.status_code)

        cookie = self.client.cookies.get("_vcrcs")
        print("Cookie _vcrcs:", cookie)


if __name__ == "__main__":
    bypass = VercelBypass()
    bypass.run("https://") # Enter the website you want bypass vercel