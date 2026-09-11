import urllib.request

# iptv-org sources
BD_URL = "https://iptv-org.github.io/iptv/countries/bd.m3u"
IN_URL = "https://iptv-org.github.io/iptv/countries/in.m3u"
OUTPUT_FILE = "BD-IN-FREE.m3u"

# EPG Link (Bangladesh + India)
EPG_URL = "https://iptv-org.github.io/epg/guides/bd/bengali.xml,https://iptv-org.github.io/epg/guides/in/hindi.xml"

# পছন্দের চ্যানেলগুলোর ফিল্টার লিস্ট
KEYWORDS = ["star jalsha", "zee bangla", "enterr10", "dd bangla"]

def fetch_m3u(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

print("Fetching playlists...")
lines = fetch_m3u(BD_URL) + fetch_m3u(IN_URL)

channels = []
current_extinf = ""

# Parse m3u lines and clean spaces
for line in lines:
    line = line.strip() # Remove extra spaces/newlines
    if not line:
        continue
    if line.startswith("#EXTINF"):
        current_extinf = line
    elif line.startswith("http") and current_extinf:
        channels.append((current_extinf, line))
        current_extinf = ""

# Remove duplicates
unique_channels = list(set(channels))

priority_channels = []
other_channels = []

# Filter and sort
for extinf, url in unique_channels:
    extinf_lower = extinf.lower()
    if any(kw in extinf_lower for kw in KEYWORDS):
        priority_channels.append((extinf, url))
    else:
        other_channels.append((extinf, url))

# Save to BD-IN-FREE.m3u with EPG header
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    # ফাইলের শুরুতে EPG লিংক যুক্ত করা হচ্ছে
    f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
    
    # পছন্দের চ্যানেলগুলো
    for extinf, url in priority_channels:
        f.write(f"{extinf}\n{url}\n")
        
    # বাকি চ্যানেলগুলো
    for extinf, url in other_channels:
        f.write(f"{extinf}\n{url}\n")

print(f"Playlist updated! Total channels: {len(priority_channels) + len(other_channels)}")
