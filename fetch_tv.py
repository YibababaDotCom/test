import requests

M3U_URL = "https://raw.githubusercontent.com/YibababaDotCom/test/refs/heads/main/channels.m3u"
OUTPUT_FILE = "tv.m3u"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

# 频道映射关系：支持多个可能的匹配关键字（列表形式），提高命中率
TARGET_CHANNELS = {
    "CCTV-5体育": {
        "id": "CCTV-5体育",
        "title": "CCTV-5体育",
        "keywords": ["CCTV-5体育"]
    },
    "CCTV-5+体育赛事": {
        "id": "CCTV-5+体育赛事",
        "title": "CCTV-5+体育赛事",
        "keywords": ["CCTV-5+体育赛事"]
    },
    "CCTV-16奥林匹克": {
        "id": "CCTV-16奥林匹克",
        "title": "CCTV-16奥林匹克",
        "keywords": ["CCTV-16奥林匹克"]
    },
    "广东体育": {
        "id": "广东体育",
        "title": "广东体育",
        "keywords": ["广东体育"]
    },
    "五星体育": {
        "id": "五星体育",
        "title": "五星体育",
        "keywords": ["五星体育"]
    },
    "高尔夫网球": {
        "id": "高尔夫网球",
        "title": "高尔夫网球",
        "keywords": ["高尔夫网球"]
    },
    "央视台球": {
        "id": "央视台球",
        "title": "央视台球",
        "keywords": ["央视台球"]
    },
    "风云音乐": {
        "id": "风云音乐",
        "title": "风云音乐",
        "keywords": ["风云音乐"]
    },
    "风云足球": {
        "id": "风云足球",
        "title": "风云足球",
        "keywords": ["风云足球"]
    },
    "风云足球": {
        "id": "风云足球",
        "title": "风云足球",
        "keywords": ["风云足球"]
    },
    "风云剧场": {
        "id": "风云剧场",
        "title": "风云剧场",
        "keywords": ["风云剧场"]
    },
    "怀旧剧场": {
        "id": "怀旧剧场",
        "title": "怀旧剧场",
        "keywords": ["怀旧剧场"]
    },
    "第一剧场": {
        "id": "第一剧场",
        "title": "第一剧场",
        "keywords": ["第一剧场"]
    },
    "世界地理": {
        "id": "世界地理",
        "title": "世界地理",
        "keywords": ["世界地理"]
    },
    "女性时尚": {
        "id": "女性时尚",
        "title": "女性时尚",
        "keywords": ["女性时尚"]
    },
    "CHC动作电影": {
        "id": "CHC动作电影",
        "title": "CHC动作电影",
        "keywords": ["CHC动作电影"]
    },
    "CHC家庭影院": {
        "id": "CHC家庭影院",
        "title": "CHC家庭影院",
        "keywords": ["CHC家庭影院"]
    },
    "CHC影迷电影": {
        "id": "CHC影迷电影",
        "title": "CHC影迷电影",
        "keywords": ["CHC影迷电影"]
    },
    "老故事": {
        "id": "老故事",
        "title": "老故事",
        "keywords": ["老故事"]
    },
    "发现之旅": {
        "id": "发现之旅",
        "title": "发现之旅",
        "keywords": ["发现之旅"]
    },
    "CCTV-4K": {
        "id": "CCTV-4K",
        "title": "CCTV-4K",
        "keywords": ["CCTV-4K"]
    },
    "CCTV-8K": {
        "id": "CCTV-8K",
        "title": "CCTV-8K",
        "keywords": ["CCTV-8K"]
    },
    "周星驰电影": {
        "id": "周星驰电影",
        "title": "周星驰电影",
        "keywords": ["周星驰电影"]
    },
    "周润发电影": {
        "id": "周润发电影",
        "title": "周润发电影",
        "keywords": ["周润发电影"]
    },
    "成龙电影": {
        "id": "成龙电影",
        "title": "成龙电影",
        "keywords": ["成龙电影"]
    }
}

def extract_channel_urls(m3u_text):
    """优化后的提取逻辑，支持多关键字模糊匹配"""
    lines = m3u_text.splitlines()
    found_urls = {}

    for i, line in enumerate(lines):
        if line.startswith("#EXTINF"):
            # 检查当前行是否命中了任何配置的关键字
            for config_key, config_data in TARGET_CHANNELS.items():
                if config_key in found_urls:
                    continue
                
                # 只要满足 keywords 列表中的任意一个词即视为匹配
                if any(kw in line for kw in config_data["keywords"]):
                    # 向下寻找第一个非注释的 URL 链接
                    for j in range(i + 1, len(lines)):
                        next_line = lines[j].strip()
                        if next_line and not next_line.startswith("#"):
                            found_urls[config_key] = next_line
                            break

    return found_urls

def resolve_real_url(initial_url):
    """增强版重定向解析：优先 HEAD，失败或受阻则降级为带有 stream 截断的 GET"""
    try:
        # 第一次尝试：使用 HEAD 请求
        response = requests.head(initial_url, headers=headers, allow_redirects=True, timeout=8)
        if response.status_code < 400:
            return response.url
    except Exception:
        pass

    try:
        # 第二次尝试：降级为 GET 请求（只读取头部流，避免下载完整视频）
        response = requests.get(initial_url, headers=headers, allow_redirects=True, stream=True, timeout=8)
        final_url = response.url
        response.close()
        return final_url
    except Exception as e:
        print(f"⚠️ 解析真实 URL 失败 ({initial_url}): {e}")
        return initial_url

def main():
    print("正在下载原始 M3U 文件...")
    try:
        resp = requests.get(M3U_URL, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ 下载 M3U 文件失败: {e}")
        return

    raw_urls = extract_channel_urls(resp.text)
    m3u_lines = ["#EXTM3U"]

    # 按照 TARGET_CHANNELS 的顺序处理
    for config_key, config in TARGET_CHANNELS.items():
        raw_url = raw_urls.get(config_key)
        if not raw_url:
            print(f"⚠️ 未找到频道: {config['title']}")
            continue

        print(f"[{config['id']}] 找到原始链接: {raw_url}")
        real_url = resolve_real_url(raw_url)
        print(f"[{config['id']}] 转换真实链接: {real_url}\n")

        # 写入 M3U 格式
        m3u_lines.append(f'#EXTINF:-1 tvg-id="{config["id"]}" tvg-name="{config["id"]}",{config["title"]}')
        m3u_lines.append(real_url)

    # 保存最终文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines) + "\n")
        
    print(f"✅ 已成功写入 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
