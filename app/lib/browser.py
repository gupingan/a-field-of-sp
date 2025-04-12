import asyncio
import random
import threading
from loguru import logger
from pyppeteer import launch
from pyppeteer.page import Page
from pyppeteer.errors import NetworkError, ElementHandleError, TimeoutError
from app.lib.core import TomlBase
from app.utils.math import bezier_curve


async def create_browser(dict_cookies, is_train, strategy):
    config = dict(
        executablePath=TomlBase.browser_path,
        headless=False,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        args=[
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--ignore-certificate-errors',
            '--disable-blink-features=AutomationControlled',
            '--excludeSwitches=["enable-automation"]',
            '--window-size=513,820',
        ],
        defaultViewport={"width": 513, "height": 666},
    )
    browser = await launch(**config)
    try:
        pages = await browser.pages()
        page = pages[0]
        cookies = [
            {'name': key, 'value': value, 'domain': '.xiaohongshu.com'} for key, value in dict_cookies.items()
        ]
        for cookie in cookies:
            await page.setCookie(cookie)
        await page.goto('https://www.xiaohongshu.com/')

        pick_note = PickNoteStrategy()
        close_note = CloseNoteStrategy()
        scroll_page = ScrollPageStrategy()
    except (asyncio.CancelledError, NetworkError, TimeoutError):
        return None

    while is_train:
        try:
            await asyncio.sleep(10)

            await pick_note.execute(page)
            logger.debug(f'进入笔记：{page.url}')
            await asyncio.sleep(random.randint(1, 3))
            await scroll_page.execute(page)
            logger.debug(f'浏览笔记：{page.url}')

            if strategy:
                random_strategy = set(random.choices(strategy, k=random.randint(1, len(strategy))))
                logger.debug(f'养号策略随机为：{random_strategy}')
                for sty in random_strategy:
                    logger.debug(f'执行养号策略准备中')
                    await asyncio.sleep(random.randint(5, 10))
                    logger.debug(f'执行养号策略：{sty}')
                    await sty.execute(page)

            await asyncio.sleep(random.randint(3, 6))
            await close_note.execute(page)
        except ElementHandleError:
            continue
        except (asyncio.CancelledError, NetworkError, TimeoutError):
            logger.debug('检测到浏览器已关闭，循环终止')
            break
        except Exception as e:
            logger.exception(e)


def run_browser_in_thread(dict_cookies: dict, is_train: bool = False, strategy: list = None):
    strategy = strategy or []

    def start_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(create_browser(dict_cookies, is_train, strategy))

    new_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_loop, args=(new_loop,))
    t.start()
    return t


def make_strategy(name: str):
    strategy_class = {
        'like_note': LikeNoteStrategy,
        'collect_note': CollectNoteStrategy,
        'share_note': ShareNoteStrategy,
        'like_comment': LikeCommentStrategy,
        'follow_author': FollowAuthorStrategy,
    }.get(name)

    if not strategy_class:
        return None

    return strategy_class()


class BaseStrategy:
    async def execute(self, page: Page):
        raise NotImplementedError

    def __repr__(self):
        return f'<{self.__class__.__name__} Strategy>'


class PickNoteStrategy(BaseStrategy):
    async def execute(self, page: Page):
        url = page.url
        if 'www.xiaohongshu.com/explore' not in url:
            return None

        elements = await page.xpath("//a[@class='title']")
        if not elements:
            return None

        logger.debug(f'获取到笔记的元素数量：{len(elements)}')

        # element = elements[4]
        element = random.choice(elements)

        current_scroll_y = await page.evaluate('window.scrollY')
        elem_top = await page.evaluate('(element) => element.getBoundingClientRect().top', element)

        window_inner_height = await page.evaluate('window.innerHeight')
        target_top = elem_top - window_inner_height // 2 + current_scroll_y
        # print('元素位置:', elem_top, '视窗高度:', window_inner_height, '目标位置:', target_top)

        # 如果当前目标 top 超过 10000，那么有概率会刷新页面
        refresh_flag = random.choice([False, False, True])
        if target_top >= 10000 and refresh_flag:
            await GotoHomeStrategy().execute(page)
            await page.waitForNavigation()
            await asyncio.sleep(5)
            await self.execute(page)
        else:
            scroll_distance = target_top - current_scroll_y
            steps = 50

            # 使用贝塞尔曲线生成滚动路径
            control_points = [
                (0, 0),
                (0.25, random.uniform(0.1, 0.3)),
                (0.75, random.uniform(0.7, 0.9)),
                (1, 1)
            ]
            bezier_path = bezier_curve(control_points, steps)

            for t in bezier_path:
                scroll_position = current_scroll_y + t * scroll_distance
                # print('scroll:',scroll_position)
                await page.evaluate(f'window.scrollTo(0, {scroll_position})')
                await asyncio.sleep(random.uniform(0.01, 0.05))

            await asyncio.sleep(random.uniform(0.5, 1.5))
            await page.evaluate('(element) => element.click()', element)


class GotoHomeStrategy(BaseStrategy):
    async def execute(self, page: Page):
        await page.goto('https://www.xiaohongshu.com/')


class LikeNoteStrategy(BaseStrategy):
    async def execute(self, page: Page):
        elements = await page.xpath("//div[@class='left']//span[@class='like-lottie']")
        if not elements:
            return None

        element = elements[0]
        await page.evaluate('(element) => element.click()', element)


class CollectNoteStrategy(BaseStrategy):
    async def execute(self, page: Page):
        elements = await page.xpath("//span[@id='note-page-collect-board-guide']")
        if not elements:
            return None

        element = elements[0]
        await page.evaluate('(element) => element.click()', element)


class ShareNoteStrategy(BaseStrategy):
    async def execute(self, page: Page):
        elements = await page.xpath("//div[@class='share-wrapper']")
        if not elements:
            return None

        await page.evaluate('document.getElementsByClassName("share-icon-container hovered")[0].click()')


async def scroll_to_position(page: Page, start: int, target: int):
    scroll_distance = target - start
    steps = 50  # 滚动的步数

    # 使用贝塞尔曲线生成滚动路径
    control_points = [
        (0, 0),
        (0.25, random.uniform(0.1, 0.3)),
        (0.75, random.uniform(0.7, 0.9)),
        (1, 1)
    ]
    bezier_path = bezier_curve(control_points, steps)

    for t in bezier_path:
        scroll_position = start + t * scroll_distance
        await page.evaluate(f'document.getElementById("noteContainer").scrollTo(0, {scroll_position})')
        await asyncio.sleep(random.uniform(0.01, 0.05))


class ScrollPageStrategy(BaseStrategy):
    async def execute(self, page: Page):
        viewpoint_height = await page.evaluate('window.innerHeight')
        await scroll_to_position(page, 0, viewpoint_height)
        await asyncio.sleep(TomlBase.preview_min_time)
        await scroll_to_position(page, viewpoint_height, 0)


class CloseNoteStrategy(BaseStrategy):
    async def execute(self, page: Page):
        elements = await page.xpath("//div[@class='close-box']")
        if not elements:
            return None

        element = elements[0]
        await page.evaluate('(element) => element.click()', element)


class LikeCommentStrategy(BaseStrategy):
    async def execute(self, page: Page):
        elements_length = await page.evaluate('document.getElementsByClassName("like").length')
        if not elements_length:
            return None
        index = random.randint(0, elements_length - 1)
        await page.evaluate(f'document.getElementsByClassName("like")[{index}].childNodes[0].click()')


class FollowAuthorStrategy(BaseStrategy):
    async def execute(self, page: Page):
        elements = await page.xpath("//div[@class='author']//div[@class='note-detail-follow-btn']")
        if not elements:
            return None

        await page.evaluate('document.getElementsByClassName("follow-button")[0].click()')
