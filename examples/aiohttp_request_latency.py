import asyncio

import aiohttp


class TraceTracing:
    def __init__(self):
        self.start_time = None
        self.time_lat = None

        self.trace_config = aiohttp.TraceConfig()
        # трекер начала запросы
        self.trace_config.on_connection_create_start.append(self.on_request_start)

        # трекер конца запросы
        self.trace_config.on_connection_create_end.append(self.on_request_end)
        self.trace_config.on_request_exception.append(self.on_request_end)

    async def on_request_start(self, _session, _trace_config_ctx, _params):
        self.start_time = asyncio.get_event_loop().time()

    async def on_request_end(self, _session, _trace_config_ctx, _params):
        self.time_lat = asyncio.get_event_loop().time() - self.start_time

    async def get(self):
        async with aiohttp.ClientSession(
                trace_configs=[self.trace_config],
                timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.request('https://127.0.0.1:8000/ping') as response:
                body = await response.text()
        return body, self.time_lat


async def main():
    body, lat = await TraceTracing().get()
    print('Req body={} lat={}'.format(body, lat))


if __name__ == '__main__':
    asyncio.run(main())
