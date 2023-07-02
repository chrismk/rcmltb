from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from time import time
from os import path as ospath
from bot.helper.telegram_helper.message_utils import sendMessage
from bot import bot, botUptime
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import cmd_exec, get_readable_time
from bot.helper.ext_utils.human_format import get_readable_file_size
from bot.helper.telegram_helper.filters import CustomFilters



async def stats(client, message):
    if ospath.exists('.git'):
        last_commit = await cmd_exec("git log -1 --date=short --pretty=format:'%cd <b>|</b> %cr'", True)
        last_commit = last_commit[0]
    else:
        last_commit = 'No UPSTREAM_REPO'
    total, used, free, disk = disk_usage('/')
    swap = swap_memory()
    memory = virtual_memory()
    stats = f'<b>程序编译时间:</b> {last_commit}\n\n'\
            f'<b>Bot启动时间:</b> {get_readable_time(time() - botUptime)}\n'\
            f'<b>系统启动时间:</b> {get_readable_time(time() - boot_time())}\n\n'\
            f'<b>硬盘:</b> {get_readable_file_size(total)}\n'\
            f'<b>已用:</b> {get_readable_file_size(used)} | <b>剩余:</b> {get_readable_file_size(free)}\n\n'\
            f'<b>已上传:</b> {get_readable_file_size(net_io_counters().bytes_sent)}\n'\
            f'<b>已下载:</b> {get_readable_file_size(net_io_counters().bytes_recv)}\n\n'\
            f'<b>CPU:</b> {cpu_percent(interval=0.5)}%\n'\
            f'<b>内存:</b> {memory.percent}%\n'\
            f'<b>硬盘:</b> {disk}%\n\n'\
            f'<b>CPU核心:</b> {cpu_count(logical=False)}\n'\
            f'<b>交换空间:</b> {get_readable_file_size(swap.total)} | <b>已用:</b> {swap.percent}%\n'\
            f'<b>内存:</b> {get_readable_file_size(memory.total)}\n'\
            f'<b>已用:</b> {get_readable_file_size(memory.used)}\n'\
            f'<b>剩余:</b> {get_readable_file_size(memory.available)}\n'    

    await sendMessage(stats, message)
        

        
stats_handler = MessageHandler(stats, filters= command(BotCommands.StatsCommand) & (CustomFilters.user_filter | CustomFilters.chat_filter))

bot.add_handler(stats_handler)

