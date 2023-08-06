import asyncio
import traceback

from nonebot.log import logger
from nonebot.adapters.onebot.v11.message import MessageSegment

from ... import config
from ...database import DB as db
from bilireq.grpc.dynamic import grpc_get_user_dynamics
from bilireq.grpc.protos.bilibili.app.dynamic.v2.dynamic_pb2 import DynamicType
from ...utils import get_dynamic_screenshot, safe_send, scheduler

offset = {}


@scheduler.scheduled_job(
    "interval", seconds=config.haruka_dynamic_interval, id="dynamic_sched"
)
async def dy_sched():
    """动态推送"""

    uid = await db.next_uid("dynamic")
    if not uid:
        return
    user = await db.get_user(uid=uid)
    assert user is not None
    name = user.name

    # 获取 UP 最新动态列表
    dynamics = (
        await grpc_get_user_dynamics(uid, timeout=5, proxy=config.haruka_proxy)
    ).list

    if dynamics:
        # 如果 UP 发布过动态则更新昵称
        name = dynamics[0].modules[0].module_author.author.name

    logger.debug(f"爬取动态 {name}（{uid}）")

    if uid not in offset:  # 没有爬取过这位主播就把最新一条动态时间为 last_time
        dynamic = dynamics[0]
        offset[uid] = int(dynamic.extend.dyn_id_str)
        return

    dynamic = None
    for dynamic in dynamics[::-1]:  # 从旧到新取最近5条动态
        dynamic_id = int(dynamic.extend.dyn_id_str)
        if dynamic_id > offset[uid]:
            logger.info(f"检测到新动态（{dynamic_id}）：{name}（{uid}）")
            url = f"https://m.bilibili.com/dynamic/{dynamic_id}"
            image = None
            for _ in range(3):
                try:
                    # PC版网页：
                    # image = await get_dynamic_screenshot(dynamic.url)

                    # 移动端网页：
                    image = await get_dynamic_screenshot(url)
                    break
                except Exception:
                    logger.error("截图失败，以下为错误日志:")
                    logger.error(traceback.format_exc())
                await asyncio.sleep(0.1)
            if not image:
                logger.error("已达到重试上限，将在下个轮询中重新尝试")

            type_msg = {
                0: "发布了新动态",
                DynamicType.forward: "转发了一条动态",
                DynamicType.word: "发布了新文字动态",
                DynamicType.draw: "发布了新图文动态",
                DynamicType.av: "发布了新投稿",
                DynamicType.article: "发布了新专栏",
                DynamicType.music: "发布了新音频",
            }
            message = (
                f"{name} "
                + f"{type_msg.get(dynamic.card_type, type_msg[0])}：\n"
                + f"{url}\n"
                + MessageSegment.image(f"base64://{image}")
            )

            push_list = await db.get_push_list(uid, "dynamic")
            for sets in push_list:
                await safe_send(
                    bot_id=sets.bot_id,
                    send_type=sets.type,
                    type_id=sets.type_id,
                    message=message,
                    at=bool(sets.at) and config.haruka_dynamic_at,
                )

            offset[uid] = dynamic_id

    if dynamic:
        await db.update_user(uid, name)
