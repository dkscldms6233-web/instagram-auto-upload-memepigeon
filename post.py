"""인스타그램 자동 업로드 스크립트
schedule.json 에 적힌 시간이 지난 게시물 중 아직 안 올린 것을 올리고 posted.json 에 기록해요.
"""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone

TOKEN = os.environ["IG_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]          # 예: 사용자/저장소
BRANCH = os.environ.get("BRANCH", "main")
API = "https://graph.instagram.com/v23.0"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"


def call(method, path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print("API 오류:", e.read().decode(), file=sys.stderr)
        raise


def wait_ready(container_id):
    for _ in range(30):
        s = call("GET", container_id, fields="status_code")
        if s.get("status_code") == "FINISHED":
            return
        if s.get("status_code") == "ERROR":
            raise RuntimeError(f"미디어 처리 실패: {container_id}")
        time.sleep(5)
    raise RuntimeError("미디어 처리 시간 초과")


def publish(post):
    me = call("GET", "me", fields="user_id")["user_id"]
    urls = [RAW + urllib.parse.quote(p) for p in post["images"]]
    if len(urls) == 1:
        c = call("POST", f"{me}/media", image_url=urls[0], caption=post["caption"])["id"]
    else:
        children = []
        for u in urls:
            cid = call("POST", f"{me}/media", image_url=u, is_carousel_item="true")["id"]
            wait_ready(cid)
            children.append(cid)
        c = call("POST", f"{me}/media", media_type="CAROUSEL",
                 children=",".join(children), caption=post["caption"])["id"]
    wait_ready(c)
    return call("POST", f"{me}/media_publish", creation_id=c)["id"]


def main():
    schedule = json.load(open("schedule.json", encoding="utf-8"))["posts"]
    state = json.load(open("posted.json", encoding="utf-8"))
    done = set(state["posted"])
    now = datetime.now(timezone.utc)
    for post in schedule:
        if post["id"] in done:
            continue
        if datetime.fromisoformat(post["time"]) > now:
            continue
        print("업로드:", post["id"])
        media_id = publish(post)
        print("완료:", post["id"], media_id)
        state["posted"].append(post["id"])
        json.dump(state, open("posted.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        break  # 한 번 실행에 한 게시물만 (밀린 게 있으면 다음 실행 때 올라가요)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        print(call("GET", "me", fields="user_id,username"))
    elif len(sys.argv) > 1 and sys.argv[1] == "refresh":
        print(call("GET", "refresh_access_token", grant_type="ig_refresh_token").get("expires_in"))
    else:
        main()
