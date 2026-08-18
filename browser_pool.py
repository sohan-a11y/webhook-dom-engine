import time
import asyncio
from playwright.async_api import async_playwright, Playwright, Browser
from models import ExecutionRequest, ExecutionResponse, ActionType
from config import settings

class BrowserPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserPool, cls).__new__(cls)
            cls._instance.pw = None
            cls._instance.browser = None
            cls._instance.semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_CONTEXTS)
        return cls._instance

    async def start(self):
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(headless=settings.HEADLESS)
        print("[BrowserPool] Chromium browser process started.")

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.pw:
            await self.pw.stop()
        print("[BrowserPool] Chromium browser process stopped.")

    async def execute_macro(self, req: ExecutionRequest) -> ExecutionResponse:
        start_time = time.perf_counter()
        async with self.semaphore:
            if not self.browser:
                return ExecutionResponse(
                    status="error",
                    execution_time_ms=0,
                    error_message="BrowserPool is not initialized."
                )

            context = await self.browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(req.url, wait_until="domcontentloaded", timeout=settings.DEFAULT_TIMEOUT_MS)

                for act in req.actions:
                    t_ms = act.timeout_ms or settings.DEFAULT_TIMEOUT_MS
                    if act.action == ActionType.GOTO:
                        if act.value:
                            await page.goto(act.value, wait_until="domcontentloaded", timeout=t_ms)
                    elif act.action == ActionType.CLICK:
                        if act.selector:
                            await page.click(act.selector, timeout=t_ms)
                    elif act.action == ActionType.TYPE:
                        if act.selector and act.value is not None:
                            await page.fill(act.selector, act.value, timeout=t_ms)
                    elif act.action == ActionType.WAIT_FOR:
                        if act.selector:
                            await page.wait_for_selector(act.selector, timeout=t_ms)

                # Final extraction
                await page.wait_for_selector(req.return_selector, timeout=settings.DEFAULT_TIMEOUT_MS)
                text = await page.inner_text(req.return_selector)

                exec_time = (time.perf_counter() - start_time) * 1000
                return ExecutionResponse(
                    status="success",
                    scraped_data=text,
                    execution_time_ms=round(exec_time, 2)
                )

            except Exception as e:
                exec_time = (time.perf_counter() - start_time) * 1000
                return ExecutionResponse(
                    status="error",
                    execution_time_ms=round(exec_time, 2),
                    error_message=str(e)
                )
            finally:
                await context.close()
