import requests
import threading
import time
import random
import hashlib
from queue import Queue
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LoadTester:
    def __init__(self, url, request_num=1000, concurrent_threads=50, timeout_seconds=15, callback=None):
        self.url = url
        self.request_num = request_num
        self.concurrent_threads = concurrent_threads
        self.timeout_seconds = timeout_seconds
        self.callback = callback
        
        # Statistics
        self.successful_requests = 0
        self.failed_requests = 0
        self.timeout_errors = 0
        self.connection_errors = 0
        self.waf_blocks = 0
        self.rate_limits = 0
        self.server_errors = 0
        self.total_bytes_received = 0
        self.response_times = []
        self.status_codes = {}
        
        self.lock = threading.Lock()
        self.request_queue = Queue()
        self.is_running = False
        self.start_time = None
        
        # User agents pool
        self.user_agents = self.generate_user_agents()
        
        # Session pool
        self.session_pool = []
        self.create_session_pool()
    
    def generate_user_agents(self):
        """Generate diverse user agents"""
        agents = []
        
        # Chrome variants
        for v in range(90, 122):
            agents.append(f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36')
            agents.append(f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36')
        
        # Firefox variants
        for v in range(90, 122):
            agents.append(f'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{v}.0) Gecko/20100101 Firefox/{v}.0')
        
        # Mobile variants
        for v in range(90, 110):
            agents.append(f'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Mobile Safari/537.36')
        
        return agents
    
    def create_session_pool(self):
        """Create session pool for connection reuse"""
        for i in range(min(self.concurrent_threads, 50)):
            session = requests.Session()
            
            # Add cookies
            timestamp = int(time.time())
            session.cookies.set('_ga', f'GA1.2.{random.randint(1000000000, 9999999999)}.{timestamp}')
            session.cookies.set('sessionid', hashlib.md5(str(random.random()).encode()).hexdigest())
            
            session.headers.update({
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            })
            
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=20,
                pool_maxsize=20,
                max_retries=0
            )
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            self.session_pool.append(session)
    
    def get_session(self):
        """Get random session from pool"""
        return random.choice(self.session_pool) if self.session_pool else requests
    
    def generate_headers(self):
        """Generate request headers"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.9']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }
    
    def send_request(self, request_id):
        """Send single request"""
        session = self.get_session()
        
        try:
            # Build URL with cache busting
            request_url = self.url
            sep = '&' if '?' in self.url else '?'
            ts = int(time.time() * 1000000) + random.randint(1, 99999)
            request_url = f"{self.url}{sep}_={ts}&req={request_id}"
            
            # Generate headers
            headers = self.generate_headers()
            
            # Send request
            start_time = time.time()
            response = session.get(request_url, timeout=self.timeout_seconds, headers=headers, verify=False, allow_redirects=True)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            with self.lock:
                self.response_times.append(response_time)
                self.status_codes[response.status_code] = self.status_codes.get(response.status_code, 0) + 1
                self.total_bytes_received += len(response.content)
            
            if 200 <= response.status_code < 300:
                with self.lock:
                    self.successful_requests += 1
                return True
            
            elif response.status_code == 403:
                with self.lock:
                    self.failed_requests += 1
                    self.waf_blocks += 1
            
            elif response.status_code == 429:
                with self.lock:
                    self.failed_requests += 1
                    self.rate_limits += 1
                time.sleep(random.uniform(1, 2))
            
            elif response.status_code >= 500:
                with self.lock:
                    self.failed_requests += 1
                    self.server_errors += 1
            
            else:
                with self.lock:
                    self.failed_requests += 1
        
        except requests.exceptions.Timeout:
            with self.lock:
                self.failed_requests += 1
                self.timeout_errors += 1
        
        except requests.exceptions.ConnectionError:
            with self.lock:
                self.failed_requests += 1
                self.connection_errors += 1
            time.sleep(random.uniform(0.5, 1))
        
        except Exception as e:
            with self.lock:
                self.failed_requests += 1
        
        return False
    
    def worker(self):
        """Worker thread"""
        while self.is_running:
            try:
                request_id = self.request_queue.get(timeout=1)
                if request_id is None:
                    break
                
                self.send_request(request_id)
                self.request_queue.task_done()
                
                # Update callback
                if self.callback:
                    self.callback(self.get_stats())
                
            except:
                continue
    
    def get_stats(self):
        """Get current statistics"""
        with self.lock:
            total = self.successful_requests + self.failed_requests
            progress = (total / self.request_num * 100) if self.request_num > 0 else 0
            success_rate = (self.successful_requests / total * 100) if total > 0 else 0
            
            elapsed = time.time() - self.start_time if self.start_time else 1
            rps = total / elapsed if elapsed > 0 else 0
            
            avg_response = sum(self.response_times) / len(self.response_times) if self.response_times else 0
            min_response = min(self.response_times) if self.response_times else 0
            max_response = max(self.response_times) if self.response_times else 0
            
            status = "Running" if self.is_running else "Stopped"
            if total >= self.request_num:
                status = "Completed"
            
            return {
                'successful': self.successful_requests,
                'failed': self.failed_requests,
                'waf_blocks': self.waf_blocks,
                'rate_limits': self.rate_limits,
                'server_errors': self.server_errors,
                'timeout_errors': self.timeout_errors,
                'connection_errors': self.connection_errors,
                'progress': progress,
                'success_rate': success_rate,
                'rps': rps,
                'avg_response': avg_response,
                'min_response': min_response,
                'max_response': max_response,
                'bytes_received': self.total_bytes_received,
                'status': status,
                'total': total
            }
    
    def run_test(self):
        """Run the load test"""
        self.is_running = True
        self.start_time = time.time()
        
        # Reset stats
        self.successful_requests = 0
        self.failed_requests = 0
        self.timeout_errors = 0
        self.connection_errors = 0
        self.waf_blocks = 0
        self.rate_limits = 0
        self.server_errors = 0
        self.total_bytes_received = 0
        self.response_times = []
        self.status_codes = {}
        
        # Queue requests
        for i in range(self.request_num):
            self.request_queue.put(i + 1)
        
        # Start worker threads
        threads = []
        for _ in range(self.concurrent_threads):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()
            threads.append(t)
        
        # Wait for completion
        self.request_queue.join()
        
        self.is_running = False
        
        # Final callback
        if self.callback:
            self.callback(self.get_stats())
    
    def stop(self):
        """Stop the test"""
        self.is_running = False
        
        # Clear queue
        while not self.request_queue.empty():
            try:
                self.request_queue.get_nowait()
                self.request_queue.task_done()
            except:
                break
