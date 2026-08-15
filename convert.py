import json
import urllib.request
import sys

# 1. 官方 Venera 漫画源索引地址
SOURCE_INDEX_URL = "https://raw.githubusercontent.com/venera-app/venera-configs/main/index.json"
# 2. 使用 jsDelivr CDN 加速 JS 脚本的下载（优化国内网络环境）
CDN_URL_TEMPLATE = "https://cdn.jsdelivr.net/gh/venera-app/venera-configs@main/{}"

def fetch_index():
    """从官方仓库拉取最新的 index.json"""
    req = urllib.request.Request(SOURCE_INDEX_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"❌ 拉取官方 index.json 失败: {e}", file=sys.stderr)
        sys.exit(1)

def transform(sources):
    """将官方格式转换为 Venera-Next 所需格式"""
    venera_next_sources = []
    for src in sources:
        filename = src.get("fileName")
        if not filename:
            continue
            
        # 构建 Venera-Next 订阅列表要求的 JSON 结构
        new_src = {
            "name": src.get("name", ""),
            "url": CDN_URL_TEMPLATE.format(filename),
            "version": src.get("version", "1.0.0")
        }
        
        # 保留可选的 description 字段
        description = src.get("description")
        if description:
            new_src["description"] = description
            
        venera_next_sources.append(new_src)
        
    return venera_next_sources

if __name__ == "__main__":
    print("🔄 开始拉取并转换漫画源配置...")
    original_sources = fetch_index()
    converted_sources = transform(original_sources)
    
    output_file = "venera-next-sources.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(converted_sources, f, indent=2, ensure_ascii=False)
        
    print(f"✅ 转换成功！共生成 {len(converted_sources)} 个漫画源，已保存至 {output_file}")
