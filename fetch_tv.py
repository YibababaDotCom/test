import requests

M3U_URL = "https://raw.githubusercontent.com/YibababaDotCom/test/refs/heads/main/channels.m3u"
OUTPUT_FILE = "tv.m3u"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 频道映射关系：{ M3U中的频道识别特征: (输出的ID/名称, 显示标题) }
TARGET_CHANNELS = {
    "CCTV-5体育 线路A": {
        "id": "CCTV-5体育 线路A",
        "title": "CCTV-5体育 线路A"
    },
    "CCTV-5体育 线路B": {
    "id": "CCTV-5体育 线路B",
    "title": "CCTV-5体育 线路B"
    },
    "CCTV-5体育 线路C": {
        "id": "CCTV-5体育 线路C",
        "title": "CCTV-5体育 线路C"
    },
    "CCTV-5体育 线路D": {
        "id": "CCTV-5体育 线路D",
        "title": "CCTV-5体育 线路D"
    },
    "CCTV-5+体育赛事": {
        "id": "CCTV-5+体育赛事",
        "title": "CCTV-5+体育赛事"
    },
    "CCTV-16奥林匹克": {
        "id": "CCTV-16奥林匹克",
        "title": "CCTV-16奥林匹克"
    },
    "广东体育": {
        "id": "广东体育",
        "title": "广东体育"
    },
    "五星体育": {
        "id": "五星体育",
        "title": "五星体育"
    },
    "高尔夫网球": {
        "id": "高尔夫网球",
        "title": "高尔夫网球"
    },
    "央视台球": {
        "id": "央视台球",
        "title": "央视台球"
    },
    "风云音乐": {
        "id": "风云音乐",
        "title": "风云音乐"
    },
    "风云足球": {
        "id": "风云足球",
        "title": "风云足球"
    },
    "风云剧场": {
        "id": "风云剧场",
        "title": "风云剧场"
    },
    "怀旧剧场": {
        "id": "怀旧剧场",
        "title": "怀旧剧场"
    },
    "第一剧场": {
        "id": "第一剧场",
        "title": "第一剧场"
    },
    "世界地理": {
        "id": "世界地理",
        "title": "世界地理"
    },
    "女性时尚": {
        "id": "女性时尚",
        "title": "女性时尚"
    },
    "CHC动作电影": {
        "id": "CHC动作电影",
        "title": "CHC动作电影"
    },
    "CHC家庭影院": {
        "id": "CHC家庭影院",
        "title": "CHC家庭影院"
    },
    "CHC影迷电影": {
        "id": "CHC影迷电影",
        "title": "CHC影迷电影"
    },
    "老故事": {
        "id": "老故事",
        "title": "老故事"
    },
    "发现之旅": {
        "id": "发现之旅",
        "title": "发现之旅"
    }
}

def extract_channel_urls(m3u_text):
    """提取各频道的原始 URL"""
    lines = m3u_text.splitlines()
    found_urls = {}

    for i, line in enumerate(lines):
        if line.startswith("#EXTINF"):
            # 遍历我们关心的目标频道
            for target_name in TARGET_CHANNELS.keys():
                if target_name in found_urls:
                    continue  # 已找到的频道跳过
                
                # 准确检查 #EXTINF 行是否包含完整的频道名称
                if target_name in line:
                    # 往下寻找第一条非空的 URL 链接
                    for j in range(i + 1, len(lines)):
                        next_line = lines[j].strip()
                        if next_line and not next_line.startswith("#"):
                            found_urls[target_name] = next_line
                            break

    return found_urls

def resolve_real_url(initial_url):
    """跟进 302 重定向，获取最终真实 URL"""
    try:
        response = requests.head(initial_url, headers=headers, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print(f"解析真实 URL 失败: {e}")
        return initial_url

def main():
    print("正在下载原始 M3U 文件...")
    resp = requests.get(M3U_URL, headers=headers, timeout=15)
    resp.raise_for_status()

    raw_urls = extract_channel_urls(resp.text)
    
    m3u_lines = ["#EXTM3U"]

    # 按照 TARGET_CHANNELS 的顺序处理
    for target_name, config in TARGET_CHANNELS.items():
        raw_url = raw_urls.get(target_name)
        if not raw_url:
            print(f"⚠️ 未找到频道: {target_name}")
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
        
    print(f"已成功写入 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
