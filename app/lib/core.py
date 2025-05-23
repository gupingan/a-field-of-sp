import io
import random
import uuid
import difflib
import datetime
import json
import copy
import time
from os import PathLike
from pathlib import PurePath
from collections import defaultdict
from typing import List, Dict, Union, Generic, TypeVar, Set, Optional
from types import DynamicClassAttribute
from enum import Enum, auto

import toml
import requests
import xhs
from win32api import RegOpenKey, RegQueryValueEx
from win32con import HKEY_LOCAL_MACHINE, KEY_READ
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
from loguru import logger
from app.lib import QtCore, QtGui
from app.lib.globals import CONFIG_FILE, toml_template, WORK_TYPES, NOTE_TYPES, ROOT_DIR, settings, train_strategy
from app.lib.time import get_current_datetime
from app.utils import pcid, string

T = TypeVar('T')


class Object:
    def __init__(self):
        self.id = uuid.uuid4().hex

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'<{self.__class__.__name__}(id={self.id})>'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def to_dict(self) -> Dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: Dict):
        raise NotImplementedError

    @staticmethod
    def all_not_none(*args):
        return all((a is not None for a in args))


class User(Object):
    def __init__(self, uid: Union[str], name: Union[str]):
        super().__init__()
        self.id = uid
        self.name = name
        self.home_page = f'https://www.xiaohongshu.com/user/profile/{uid}'

    @classmethod
    def from_dict(cls, data: Dict):
        uid = data.get('id')
        name = data.get('name')
        if cls.all_not_none(uid, name):
            return cls(uid, name)
        return None


class Author(User):
    _instances = {}

    def __new__(cls, user_id: Union[str], *args, **kwargs):
        obj_id = user_id
        if obj_id in cls._instances:
            return cls._instances[obj_id]
        else:
            obj = super().__new__(cls)
            cls._instances[obj_id] = obj
            return obj

    def __init__(self, user_id: Union[str], nickname: Union[str]):
        if not hasattr(self, 'notes'):
            super().__init__(user_id, nickname)
            self.notes: Dict[Union[str], Union[Note]] = dict()

    def add_note(self, note):
        if isinstance(note, Note):
            self.notes[note.id] = note
            return True

        return False

    def add_notes(self, notes):
        for note in notes:
            self.add_note(note)

    def to_dict(self) -> Dict:
        data = super().to_dict()
        notes = data.pop('notes', None)
        if isinstance(notes, dict):
            notes_dict = dict()
            for nid, note in notes.items():
                notes_dict[nid] = note.to_dict()
            data['notes'] = notes_dict

        return data

    @classmethod
    def from_dict(cls, data: Dict):
        uid = data.get('id')
        name = data.get('name')
        notes = data.get('notes')
        if cls.all_not_none(uid, name, notes):
            note_objs = dict()
            for nid, note in notes.items():
                note_objs[nid] = NormalNote.from_dict(note)

            normal_user = cls(uid, name)
            normal_user.notes = note_objs
            return normal_user

        return None


class LinkedUser(User):
    def __init__(self, user_id: Union[str] = '', nickname: Union[str] = '', session: Union[str] = ''):
        super().__init__(user_id, nickname)
        self.session = session  # 登录 session

    @property
    def dict_cookies(self):
        raw_cookies = TomlBase.cookies.copy() or {}
        raw_cookies['web_session'] = self.session
        return raw_cookies

    @property
    def string_cookies(self):
        iters = [f'{key}={value}' for key, value in self.dict_cookies.items()]
        return '; '.join(iters)

    @classmethod
    def from_session(cls):
        linked_user_session = TomlBase.linked_user_session
        if linked_user_session and string.validate_web_session(linked_user_session):
            return cls(session=linked_user_session)
        return None


class PrivateUser(User):

    def __init__(self, user_id: Union[str] = '', nickname: Union[str] = '', session: Union[str] = '',
                 remark: Union[str] = ''):
        super().__init__(user_id, nickname)
        self.session = session  # 登录 session
        self.remark = remark  # 使用备注
        self.working = False  # 是否工作中
        self.available = -1  # 登录状态
        self.comment_state = -1  # 评论状态

        self.create_time = ''  # 创建时间
        self.modify_time = ''  # 修改时间

    @classmethod
    def from_dict(cls, data: Dict):
        uid = data.get('id')
        name = data.get('name')
        session = data.get('session')
        remark = data.get('remark')
        working = data.get('working')
        available = data.get('available')
        comment_state = data.get('comment_state')
        create_time = data.get('create_time')
        modify_time = data.get('modify_time')
        if cls.all_not_none(uid, name, session, remark, working, available, comment_state, create_time, modify_time):
            obj = cls(uid, name, session, remark)
            obj.working = working
            obj.available = available
            obj.comment_state = comment_state
            obj.create_time = create_time
            obj.modify_time = modify_time
            return obj
        return None

    def init_time(self):
        self.create_time = get_current_datetime().strftime("%Y-%m-%d %H:%M:%S")
        self.modify_time = self.create_time
        return self.create_time

    def update_time(self):
        self.modify_time = get_current_datetime().strftime("%Y-%m-%d %H:%M:%S")
        return self.modify_time

    @property
    def dict_cookies(self):
        raw_cookies = TomlBase.cookies.copy() or {}
        raw_cookies['web_session'] = self.session
        return raw_cookies

    @property
    def string_cookies(self):
        iters = [f'{key}={value}' for key, value in self.dict_cookies.items()]
        return '; '.join(iters)


class AtUser(User):
    def __init__(self, user_id: Union[str], nickname: Union[str] = '未获取信息', remark: Union[str] = '',
                 sign: Union[str] = ''):
        super().__init__(user_id, nickname)
        self.remark = remark
        self.sign = sign

    @classmethod
    def from_dict(cls, data: Dict):
        uid = data.get('id')
        name = data.get('name')
        remark = data.get('remark', '')
        sign = data.get('sign', '')
        if cls.all_not_none(uid, name, remark, sign):
            return cls(uid, name, remark, sign)
        return None

    @property
    def results(self):
        return {
            'nickname': f'{self.name}',
            'user_id': f'{self.id}_{self.sign}' if self.sign else self.id
        }


class Comment(Object):
    def __init__(self, content: Union[str], at_users: List[str]):
        super().__init__()
        self.content = content
        self.at_users = at_users

    def to_dict(self) -> Dict:
        at_users = []
        for at_user_id in self.at_users:
            at_user = AtUserCenter.find(at_user_id)
            if at_user:
                at_users.append(at_user.to_dict())
        return {
            'content': self.content,
            'at_users': at_users
        }

    @classmethod
    def from_dict(cls, data: Dict):
        content = data.get('content')
        raw_at_users = data.get('at_users')
        if cls.all_not_none(content, raw_at_users):
            at_users = []
            for at_user_dict in raw_at_users:
                at_user_id = at_user_dict.get('id')
                at_user_obj = AtUserCenter.find(at_user_id)
                if at_user_obj:
                    at_users.append(at_user_id)
            return cls(content, at_users)
        return None

    def result(self, content: str):
        at_user_string = ''
        for at_user_id in self.at_users:
            at_user = AtUserCenter.find(at_user_id)
            if not at_user:
                continue
            at_user_string += f' @{at_user.name} '
        return f'{content}{at_user_string}'

    @property
    def real_at_users(self):
        at_users = []
        for at_user_id in self.at_users:
            at_user = AtUserCenter.find(at_user_id)
            if not at_user:
                continue
            at_users.append(at_user.results)
        return at_users


class Note(Object):
    def __init__(self, nid: Union[str]):
        super().__init__()
        self.id = nid
        self.note_url = f'https://www.xiaohongshu.com/explore/{nid}'

    @classmethod
    def from_dict(cls, data: Dict):
        nid = data.get('id')
        if cls.all_not_none(nid):
            return cls(nid)
        return None


class NormalNote(Note):
    def __init__(self, note_id: Union[str],
                 note_title: Union[str] = None,
                 note_type: Union[str] = None,
                 xsec_token: Union[str] = None,
                 xsec_source: Union[str] = None,
                 ):
        super().__init__(note_id)
        self.note_title = note_title or "未获取到笔记标题"
        self.note_type = note_type or "未获取到笔记类型"
        self.xsec_token = xsec_token or ''
        self.xsec_source = xsec_source or 'pc_feed'
        self.author = None

    def set_author(self, author: Union[Author]):
        self.author = author

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.pop('author', None)
        return data

    @classmethod
    def from_dict(cls, data: Dict):
        nid = data.get('id')
        note_title = data.get('note_title')
        note_type = data.get('note_type')
        xsec_token = data.get('xsec_token')
        xsec_source = data.get('xsec_source')
        if cls.all_not_none(nid, note_title, note_type, xsec_token, xsec_source):
            return cls(nid, note_title, note_type, xsec_token, xsec_source)

        return None


class Config(Object):
    def __init__(self, name: Union[str] = ''):
        super().__init__()
        self.name: Union[str] = name  # 配置名称
        self.collect_type: Union[int] = 1  # 在线搜索[默认]、推荐页采集、本地导入
        self.keywords: List[str] = []  # 搜索词列表
        self.note_type: Union[str] = ''  # 笔记类型
        self.sort_method: Union[str] = ''  # 排序类型
        self.is_similarity_filter: Union[bool] = False  # 是否相似度过筛
        self.similarity_lower_limit: Union[float] = 0.10  # 相似度底限
        self.similarity_keywords: List[str] = []  # 相似度关键词列表
        self.is_comment: Union[bool] = False  # 是否评论笔记
        self.is_fav_no_comment: Union[bool] = False  # 是否跳过已收藏
        self.is_comment_fav: Union[bool] = False  # 是否评论后收藏
        self.is_check_block: Union[bool] = False  # 是否检查评论屏蔽
        self.comments: List[Comment] = []  # 评论对象列表
        self.uncommon_char_mode: Union[str] = 'append'  # 生僻字模式
        self.uncommon_char_count: Union[int] = 0  # 生僻字数量
        self.is_linked_check: Union[bool] = False  # 联动检查
        self.is_skip_over_comment: Union[bool] = False  # 过多评论不检查
        self.comment_threshold: Union[int] = 0  # 过多评论不检查屏蔽的阈值
        self.is_consecutive_block_stop: Union[bool] = False  # 连续屏蔽停止
        self.consecutive_block_threshold: Union[int] = 0  # 连续屏蔽停止的条件阈值
        self.is_overall_block_stop: Union[bool] = False  # 总体屏蔽停止
        self.overall_block_threshold: Union[int] = 0  # 总体屏蔽停止的条件阈值
        self.is_retry_after_block: Union[bool] = False  # 是否屏蔽后重试
        self.retry_count: Union[int] = 0  # 重试多少次
        self.is_retry_comment_random: Union[bool] = False  # 重试评论是否随机
        self.retry_interval: Union[float] = 1.0  # 重试间隔秒

    def to_dict(self) -> Dict:
        data = super().to_dict()
        comments = data.pop('comments', None)
        if isinstance(comments, list):
            data['comments'] = [comment.to_dict() for comment in comments]

        return data

    @classmethod
    def from_dict(cls, data: Dict):
        cid = data.get('id')
        name = data.get('name')
        collect_type = data.get('collect_type')
        keywords = data.get('keywords')
        note_type = data.get('note_type')
        sort_method = data.get('sort_method')
        is_comment = data.get('is_comment')
        is_fav_no_comment = data.get('is_fav_no_comment')
        is_comment_fav = data.get('is_comment_fav')
        is_check_block = data.get('is_check_block')
        comments = data.get('comments')
        uncommon_char_mode = data.get('uncommon_char_mode')
        uncommon_char_count = data.get('uncommon_char_count')
        is_skip_over_comment = data.get('is_skip_over_comment')
        comment_threshold = data.get('comment_threshold')
        is_consecutive_block_stop = data.get('is_consecutive_block_stop')
        consecutive_block_threshold = data.get('consecutive_block_threshold')
        is_overall_block_stop = data.get('is_overall_block_stop')
        overall_block_threshold = data.get('overall_block_threshold')
        is_retry_after_block = data.get('is_retry_after_block')
        retry_count = data.get('retry_count')
        is_retry_comment_random = data.get('is_retry_comment_random')
        retry_interval = data.get('retry_interval')
        if cls.all_not_none(cid, name, collect_type, keywords, note_type, sort_method, is_comment,
                            is_fav_no_comment, is_comment_fav, is_check_block, comments, uncommon_char_mode,
                            uncommon_char_count, is_skip_over_comment, comment_threshold, is_consecutive_block_stop,
                            consecutive_block_threshold, is_overall_block_stop, overall_block_threshold,
                            is_retry_after_block, retry_count, is_retry_comment_random,
                            retry_interval):
            obj = cls(name)
            obj.__dict__.update(data)
            obj.comments = [Comment.from_dict(comment) for comment in comments]
            return obj

        return None

    def copy(self):
        config = self.__class__(self.name)
        self_dict = self.__dict__.copy()
        self_dict.pop('id')
        config.__dict__.update(self_dict)
        return config


class LoginQrCode:
    def __init__(self, url, qr_id, code):
        self.url = url
        self.qr_id = qr_id
        self.code = code
        self.qrcode = QRCode(
            version=1,
            box_size=5,
            border=4,
            error_correction=ERROR_CORRECT_L
        )
        self.qrcode.add_data(url)
        self.qrcode.make(fit=True)
        self.image = self.qrcode.make_image(fill_color="black", back_color="transparent")

    @property
    def bytes(self):
        fp = io.BytesIO()
        self.image.save(fp, 'PNG')
        return fp.getvalue()

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.qr_id}|{self.code})>'

    def __str__(self):
        return f'<{self.__class__.__name__}({self.qr_id}|{self.code})>'


class UnitState(Enum):
    READY = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOP = auto()
    ERROR = auto()

    @DynamicClassAttribute
    def description(self):
        descriptions = {
            self.READY: '就绪中',
            self.RUNNING: '运行中',
            self.PAUSED: '已暂停',
            self.STOP: '已终止',
            self.ERROR: '异常'
        }
        return descriptions.get(self, '未知态')

    @classmethod
    def is_valid(cls, state):
        """检查状态是否有效"""
        return state in cls._member_map_

    @classmethod
    def next_state(cls, current_state):
        """获取下一个有效状态"""
        states = list(cls)
        current_index = states.index(current_state)
        next_index = (current_index + 1) % len(states)
        return states[next_index]

    @staticmethod
    def get_state_color(state):
        colors = {
            UnitState.READY: QtGui.QColor(QtCore.Qt.GlobalColor.darkBlue),
            UnitState.RUNNING: QtGui.QColor(QtCore.Qt.GlobalColor.green),
            UnitState.PAUSED: QtGui.QColor(QtCore.Qt.GlobalColor.darkYellow),
            UnitState.STOP: QtGui.QColor(QtCore.Qt.GlobalColor.darkGray),
            UnitState.ERROR: QtGui.QColor(QtCore.Qt.GlobalColor.red),
        }
        return colors.get(state, QtGui.QColor(QtCore.Qt.GlobalColor.black))


class Tasker(QtCore.QObject):
    def __init__(
            self,
            user: Union[PrivateUser] = None,
            config: Union[Config] = None,
            task_count: Union[int] = 0,
            parent=None
    ):
        super().__init__(parent=parent)
        self.user = user
        self.api = xhs.API().set_cookies(user.string_cookies)
        self.config = config.copy()
        self.task_count = task_count
        self.work_notes = []
        self.consecutive_block_count = 0
        self.overall_block_count = 0
        self.is_allow = True
        self.allow_running = True

    def send_log(self, text: str = '', level: str = 'EMPTY'):
        self.parent().sendLog.emit(text, level)

    def set_task_count(self, value: Union[int]):
        self.task_count = value

    def parent(self) -> Union['Unit', None]:
        return super().parent()

    def run(self):
        # 根据单元状态判断
        self.parent().check_paused()
        self.parent().check_stop()

        user_link = string.create_link(self.user.home_page, self.user.name, 12)
        self.send_log(f'正在检测红薯账号{user_link}的登录状态...', 'IMPORTANT')
        self.user.available = self.check_user_login()
        if self.user.available == 1:
            self.send_log(f'红薯账号：{user_link} 登录状态有效', 'SUCCESS')
        else:
            self.send_log(f'红薯账号：{user_link} 登录状态非有效状态，当前阶段已放弃', 'FAILURE')
            return None

        # 根据单元状态判断
        self.parent().check_paused()
        self.parent().check_stop()

        # 根据设置采集笔记
        collect_notes = self.collect_notes()
        self.parent().notes.extend(collect_notes)
        self.parent().hash_notes.update(collect_notes)
        # 遍历笔记执行任务
        for note in self.work_notes:
            # 根据单元状态判断
            self.parent().check_paused()
            self.parent().check_stop()

            # 如果账号不是有效的或者已被禁言 则跳过
            if self.user.available != 1 or self.user.comment_state == -2:
                continue
            # 如果不评论
            if not self.config.is_comment:
                self.parent().uncomment_notes.append(note)
                self.parent().hash_uncomment_notes.add(note)
                continue

            # 根据单元状态判断
            self.parent().check_paused()
            self.parent().check_stop()

            # 连续屏蔽停止判断
            if self.config.is_check_block and self.config.is_consecutive_block_stop:
                if self.consecutive_block_count > self.config.consecutive_block_threshold:
                    self.send_log(
                        f'账号{user_link}评论连续屏蔽超过阈值{self.config.consecutive_block_threshold}，当前阶段已放弃',
                        'FAILURE')
                    return None
            # 总体屏蔽停止判断
            if self.config.is_check_block and self.config.is_overall_block_stop:
                if self.overall_block_count > self.config.overall_block_threshold:
                    self.send_log(
                        f'账号{user_link}评论总体屏蔽超过阈值{self.config.overall_block_threshold}，当前阶段已放弃',
                        'FAILURE')
                    return None

            # 1 成功评论  0 失败评论  -1 不评论
            comment_result = self.comment_note(note)
            if comment_result == 1:
                self.parent().success_notes.append(note)
                self.parent().hash_success_notes.add(note)
            elif comment_result == 0:
                self.parent().failure_notes.append(note)
                self.parent().hash_failure_notes.add(note)
            elif comment_result == -1:
                self.parent().uncomment_notes.append(note)
                self.parent().hash_uncomment_notes.add(note)
            # 评论后是否收藏
            if self.config.is_comment_fav:
                self.favorite_note(note)

            self.parent().sleep(1)

    def check_user_login(self):
        result = -1
        response = self.api.user_me()
        code = response.get('code')

        if code == -100:
            result = 0
        elif code == 0:
            result = 1

        return result

    def collect_notes(self):
        self.send_log(f'当前阶段设定处理的笔记数量为：{self.task_count} 条，用户：{self.user.name}', 'NORMAL')

        not_finish_note = self.parent().failure_notes
        if len(not_finish_note) >= self.task_count:
            self.work_notes = not_finish_note[:self.task_count]
            return self.work_notes
        else:
            self.work_notes.extend(not_finish_note)

        self.send_log(f'上阶段残留的笔记：{len(not_finish_note)} 条，可获取 {len(self.work_notes)} 条', 'NORMAL')
        new_task_count = self.task_count - len(self.work_notes)
        self.send_log(f'当前阶段待采集笔记：{new_task_count} 条', 'NORMAL')

        if self.config.collect_type == 1:
            self.work_notes.extend(self._online_collect(new_task_count))
        elif self.config.collect_type == 2:
            self.work_notes.extend(self._recommend_collect(new_task_count))
        elif self.config.collect_type == 3:
            self.work_notes.extend(self._local_collect(new_task_count))

        return self.work_notes

    def _online_collect_notes(self, keywords: List[str], note_type: str, sort_method: str, new_task_count: int):
        temp_notes = []
        page = 1
        page_size = 20
        has_more = True
        empty_item_count = 0
        empty_item_maximum = 3
        while len(temp_notes) < new_task_count and has_more and empty_item_count < empty_item_maximum:
            response = self.api.search_note(
                ' '.join(keywords), page, page_size, xhs.SORT_TYPE[sort_method], xhs.NOTE_TYPE[note_type]
            )
            if response['code'] == -100:
                self.user.available = 0
                self.send_log(f'账号 {self.user.name} 登录已失效，在线采集无法继续', 'FAILURE')
                return temp_notes
            has_more = response['data'].get('has_more', False)
            if not has_more:
                self.send_log('服务器没有给出更多的笔记，停止采集', 'WARNING')
                continue
            if 'items' not in response['data']:
                empty_item_count += 1
                if empty_item_count < empty_item_maximum:
                    self.send_log(f'采集中出现空数据，但是影响不大，继续尝试第 {empty_item_count} 次', 'WARNING')
                else:
                    self.send_log(f'采集中出现空数据，由于尝试获取次数过多，即将停止', 'WARNING')
                continue
            items = response['data']['items']
            add_index = 0
            for item in items:
                try:
                    note_id = item['id']
                    if '-' in note_id:
                        continue
                    xsec_token = item['xsec_token']
                    xsec_source = 'pc_search'
                    note_title = item['note_card'].get('display_title', '无标题')
                    # 相似度过筛判断
                    if self.config.is_similarity_filter:
                        if note_title == '无标题':
                            continue

                        similarity_result = False
                        for sm_keyword in self.config.similarity_keywords:
                            similarity = difflib.SequenceMatcher(None, note_title, sm_keyword).ratio()
                            if similarity >= self.config.similarity_lower_limit:
                                similarity_result = True

                        if not similarity_result:
                            continue

                    note_type = NOTE_TYPES.get(item['note_card']['type'], '未知')
                    user_id = item['note_card']['user']['user_id']
                    nickname = item['note_card']['user']['nickname']
                    author = Author(user_id, nickname)
                    note = NormalNote(note_id, note_title, note_type, xsec_token, xsec_source)
                    author.add_note(note)
                    note.set_author(author)
                    if note not in self.parent().hash_notes:
                        add_index += 1
                        temp_notes.append(note)
                except Exception as e:
                    logger.exception(e)
                    self.send_log('解析笔记过程中出现了小问题，但是问题不大', 'WARNING')
            logger.debug(f'第 {page} 次搜索：有效添加 {add_index} 条')
            page += 1
            self.parent().msleep(random.randint(100, 300))
        self.send_log(f'关键词`{"|".join(keywords)}`的{note_type}类型笔记已完成搜索', 'NORMAL')
        return temp_notes

    def _online_collect(self, new_task_count: Union[int]):
        """
        在线采集
        :param new_task_count: 待采集的数目
        :return:
        """
        results = []

        keywords = self.config.keywords
        note_types = WORK_TYPES.get(self.config.note_type, ['图文'])
        sort_method = self.config.sort_method
        logger.debug('准备采集...')
        self.send_log('开始采集，请稍等片刻...', 'NORMAL')
        # 先根据关键词分，再根据笔记类型分
        self.parent().check_paused()
        self.parent().check_stop()

        if len(note_types) == 1:
            temp_notes = self._online_collect_notes(keywords, note_types[0], sort_method, new_task_count)
            results = temp_notes[:new_task_count]
        elif len(note_types) == 2:
            temp_notes = []
            task_count1 = new_task_count // 2
            task_count2 = new_task_count - task_count1
            temp_notes1 = self._online_collect_notes(keywords, note_types[0], sort_method, task_count1)
            temp_notes.extend(temp_notes1)
            temp_notes2 = self._online_collect_notes(keywords, note_types[1], sort_method, task_count2)
            temp_notes.extend(temp_notes2)
            results = temp_notes[:new_task_count]

        logger.debug(f'在线采集完成：{keywords} 共计：{len(results)}')
        self.send_log(f'在线采集并处理完毕，共计: {len(results)}条', 'SUCCESS')
        return results

    def _recommend_collect(self, new_task_count: Union[int]):
        """
        推荐页采集
        :param new_task_count: 待采集的数目
        :return:
        """
        self.send_log(f'推荐页采集单阶段仅支持最多10轮搜索（不支持修改，否则影响账号获取接口后果自负）', 'IMPORTANT')
        results = []

        for index in range(10):
            self.parent().check_paused()
            self.parent().check_stop()

            response = self.api.homefeed(num=60)
            try:
                if response['code'] != 0:
                    if response['code'] == -100:
                        self.user.available = 0
                        self.send_log(f'账号 {self.user.name} 登录已失效，推荐页采集无法继续', 'FAILURE')
                    else:
                        self.send_log(f'`{response["msg"]}`导致推荐页采集无法继续', 'FAILURE')
                    return results
                else:
                    items = response['data']['items']
                    for item in items:
                        self.parent().check_paused()
                        self.parent().check_stop()

                        if 'note_card' in item:
                            note_title = item['note_card'].get('display_title', '无标题')

                            if note_title == '无标题':
                                continue

                            for sm_keyword in self.config.similarity_keywords:
                                similarity = difflib.SequenceMatcher(None, note_title, sm_keyword).ratio()
                                if similarity >= self.config.similarity_lower_limit:
                                    note_id = item['id']
                                    xsec_token = item['xsec_token']
                                    xsec_source = 'pc_feed'
                                    note_type = NOTE_TYPES.get(item['note_card']['type'], '未知')
                                    user_id = item['note_card']['user']['user_id']
                                    nickname = item['note_card']['user']['nickname']
                                    author = Author(user_id, nickname)
                                    note = NormalNote(note_id, note_title, note_type, xsec_token, xsec_source)
                                    author.add_note(note)
                                    note.set_author(author)
                                    if note not in results:
                                        results.append(note)
            except (KeyError, ValueError, IndexError, AttributeError):
                continue

            if len(results) >= new_task_count:
                self.send_log(f'采集数量已达到目标值 {new_task_count}，终止采集', 'SUCCESS')
                results = results[:new_task_count]
                break

            self.send_log(f'第 {index + 1} 轮采集已完毕，当前数量：{len(results)} 条', 'NORMAL')
            self.parent().msleep(250)

        return results

    def _local_collect(self, new_task_count: Union[int]):
        """
        本地导入
        :param new_task_count: 待采集的数目 或者 可导入的最大数目
        :return:
        """
        results = []
        if self.parent().import_notes:
            for note in self.parent().import_notes[:new_task_count]:
                if note not in self.parent().hash_notes:
                    results.append(note)
            for note in results:
                self.parent().import_notes.remove(note)
            self.send_log(f'已从上一阶段导入的笔记中获取到多余的 {len(results)} 条', 'SUCCESS')
        else:
            self.parent().is_wait_import = True
            self.send_log(f'请为当前阶段的账号`{self.user.name}`提供一些笔记(右下角导入笔记)', 'WARNING')

            self.parent().pause()
            self.parent().check_paused()
            self.parent().is_wait_import = False
            self.parent().check_stop()

            for note in self.parent().import_notes[:new_task_count]:
                if note not in self.parent().hash_notes:
                    results.append(note)
            for note in results:
                self.parent().import_notes.remove(note)

            self.send_log(f'当前阶段已导入笔记共计 {len(results)} 条', 'SUCCESS')

        return results

    def comment_note(self, note: Union[NormalNote]):
        user_link = string.create_link(self.user.home_page, self.user.name, 12)
        note_link = string.create_link(note.note_url, note.note_title, 12)

        is_check_block = self.config.is_check_block

        try:
            if self.config.is_fav_no_comment or (self.config.is_check_block and self.config.is_skip_over_comment):
                note_feed = self.api.note_feed(note.id)
                logger.debug(f'获取笔记详情：{note.id} - {note_feed}')
                if not note_feed['success']:
                    if note_feed['code'] == -100:
                        self.user.available = 0
                        self.send_log(f'{user_link}登录已过期，笔记{note_link}无法继续评论', 'FAILURE')
                    return 0

                note_card = note_feed['data']['items'][0]['note_card']
                collected = note_card['interact_info']['collected']
                raw_comment_count = note_card['interact_info']['comment_count']
                comment_count = int(raw_comment_count) if (
                        isinstance(raw_comment_count, str) and raw_comment_count.isdigit()) else 0
                if self.config.is_check_block and self.config.is_skip_over_comment:
                    if comment_count > self.config.comment_threshold:
                        self.send_log(
                            f'笔记{note_link}的评论数量超过阈值{self.config.comment_threshold}，不检查屏蔽',
                            'NORMAL'
                        )
                        is_check_block = False

                if self.config.is_fav_no_comment and collected:
                    self.send_log(f'{note.note_type}类型的笔记{note_link}已收藏，跳过评论', 'NORMAL')
                    return -1
        except (KeyError, IndexError, TypeError):
            self.send_log(f'获取笔记{note_link}的数据失败，当前阶段跳过该笔记评论', 'FAILURE')
            return 0

        return self._execute_comment(note, is_check_block)

    def _execute_comment(self, note: Union[NormalNote], is_check_block: Union[bool]):
        user_link = string.create_link(self.user.home_page, self.user.name, 12)
        note_link = string.create_link(note.note_url, note.note_title, 12)
        if not self.config.comments:
            self.send_log('当前配置未设置评论内容，无法继续', 'FAILURE')
            return 0

        comment, real_at_users = self._get_comment()

        for index in range(self.config.retry_count + 1):
            self.parent().check_paused()
            self.parent().check_stop()

            if self.config.is_retry_comment_random:
                comment, real_at_users = self._get_comment()

            logger.debug(f'执行评论的参数：{note.id}, {comment}, {real_at_users}')
            response = (self.api.comment_post(note.id, comment, real_at_users))
            logger.debug(f'评论后的响应：{note.id} - {response}')

            self.parent().check_paused()
            self.parent().check_stop()

            if 'data' not in response or 'msg' not in response:
                self.send_log(f'对{note.note_type}类型的笔记{note_link}评论失败，原因未知', 'FAILURE')
                return 0

            try:
                comment_id = response['data']['comment']['id']
            except (KeyError, TypeError):
                if response['code'] == -9109:
                    self.send_log(f'{note.note_type}类型的笔记{note_link}可能已被删除或者被限制，不再评论该笔记',
                                  'WARNING')
                    return -1
                if response['code'] == -9119:
                    self.send_log(f'笔记{note_link}的作者{user_link}只允许好友评论，不再评论该笔记', 'WARNING')
                    return -1
                if response['code'] == 10001:
                    self.user.comment_state = -2
                    self.send_log(f'用户{user_link}已被禁言，无法继续评论', 'FAILURE')
                    return 0
                if response['code'] == -100:
                    self.user.available = 0
                    self.send_log(f'对{note.note_type}类型的笔记{note_link}评论失败，{user_link}登录已失效', 'FAILURE')
                    return 0

                self.send_log(f'对{note.note_type}类型的笔记{note_link}评论失败，{response["msg"]}', 'FAILURE')
                return -1
            except Exception as e:
                logger.exception(e)
                self.send_log(f'对{note.note_type}类型的笔记{note_link}评论失败，可查看软件日志', 'FAILURE')
                return 0

            self.send_log(f'用户{user_link}对笔记{note_link}发送了评论：{comment}', 'SUCCESS')

            final_result = 1

            if is_check_block:
                self.parent().check_paused()
                self.parent().check_stop()

                if not comment_id:
                    self.send_log('无法获取评论ID，无法检查屏蔽，评论默认成功', 'WARNING')
                    return final_result

                # 连续屏蔽停止判断
                if self.config.is_consecutive_block_stop:
                    if self.consecutive_block_count > self.config.consecutive_block_threshold:
                        return 0
                # 总体屏蔽停止判断
                if self.config.is_overall_block_stop:
                    if self.overall_block_count > self.config.overall_block_threshold:
                        raise UnitStop()

                logger.debug(f'检查屏蔽开始，评论ID：{comment_id}')
                start_time = time.time()
                self.parent().msleep(int(TomlBase.after_check_seconds * 1000))
                check_result = self._check_comment_state(note, comment_id)
                end_time = time.time()
                consuming_time = end_time - start_time
                logger.debug(f'检查结果'
                             f'[{consuming_time}s|{consuming_time - TomlBase.after_check_seconds}s]：'
                             f'{check_result}')

                # 各情况打印
                if check_result == '可见':
                    self.consecutive_block_count = 0
                    self.user.comment_state = 1
                    final_result = 1
                    self.send_log(f'对{note.note_type}笔记{note_link}发出的评论是可见的', 'SUCCESS')
                elif check_result == '不可见':
                    self.send_log(f'对{note.note_type}笔记{note_link}发出的评论不可见', 'FAILURE')
                elif check_result == '未知':
                    self.send_log(f'对{note.note_type}笔记{note_link}发出的评论可视度未知', 'WARNING')
                elif check_result == '未找到':
                    self.send_log(f'对{note.note_type}笔记{note_link}发出的评论未找到', 'WARNING')
                else:
                    self.send_log(f'检查屏蔽时发生了意料之外的情况，评论默认失败', 'WARNING')

                # 非可见时的处理
                if check_result != '可见':
                    self.consecutive_block_count += 1
                    self.overall_block_count += 1
                    self.user.comment_state = 0
                    final_result = 0

                    if self.config.is_retry_after_block:
                        if index >= self.config.retry_count:
                            return final_result  # 处理重试最后一次的打印（理论3次，会打印第4次重新...）
                        self.send_log(f'第{index + 1}次重新提交评论`{comment}`中...', 'NORMAL')
                        self.parent().sleep(int(self.config.retry_interval))
                        continue  # 非可见并重试
                return final_result  # 可见时 / 非可见且不重试
            return final_result  # 不检查屏蔽下跳出，意味执行一次

    def _get_comment(self):
        self.parent().check_paused()
        self.parent().check_stop()
        comment_obj: Comment = random.choice(self.config.comments)
        return comment_obj.result(comment_obj.content), comment_obj.real_at_users

    def _check_comment_state(self, note: Union[NormalNote], comment_id: Union[str], cursor: Union[str] = ""):
        self.parent().check_paused()
        self.parent().check_stop()
        if self.config.is_linked_check:
            linked_user = LinkedUser.from_session()
            if not linked_user:
                self.send_log('未设置联动用户[设置 -> 联动用户]，当前使用递归检索模式[极慢]', 'WARNING')

                return self._old_check(note, comment_id, cursor)

            return self._linked_check(linked_user, note, comment_id)
        else:
            return self._old_check(note, comment_id, cursor)

    def _old_check(self, note: Union[NormalNote], comment_id: Union[str], cursor: Union[str] = ""):
        self.parent().check_paused()
        self.parent().check_stop()

        user_link = string.create_link(self.user.home_page, self.user.name, 12)
        response = self.api.show_comments(note.id, cursor, comment_id, xsec_token=note.xsec_token)
        logger.debug(f'查看评论内容：{response}')
        if not response['success']:
            if response['code'] == -100:
                self.user.available = 0
                self.send_log(f'检查屏蔽失败，用户{user_link}登录已失效', 'FAILURE')
            return '未知'

        if 'comments' in response['data']:
            for comment in response['data']['comments']:
                if comment is None:
                    continue
                if comment['id'] == comment_id:
                    if comment['status'] in {0, 2, 4}:
                        return "可见"
                    return "不可见"
            if not response['data'].get('has_more', False):
                return '未找到'
            cursor = response['data'].get('cursor', '')
            return self._old_check(note, comment_id, cursor)

    def _linked_check(self, linked_user: LinkedUser, note: Union[NormalNote], comment_id: Union[str]):
        self.parent().check_paused()
        self.parent().check_stop()

        contents = ['嗯...[害羞R]', '对的[害羞R]', '[害羞R][害羞R]666', '[害羞R]那也这样吧']
        response = xhs.API().set_cookies(linked_user.string_cookies).comment_post(
            note.id, random.choice(contents), target_comment_id=comment_id
        )
        logger.debug(f'联动检查屏蔽，返回响应：{response}')

        try:
            if response['code'] == 0:
                child_comment_id = response['data']['comment']['id']
                xhs.API().set_cookies(linked_user.string_cookies).comment_delete(note.id, child_comment_id)
                return '可见'
            elif response['code'] == 10001:
                # 禁言的，但是评论是存在的
                return '可见'
            elif response['code'] in (-9128, -9126):
                return '不可见'
            elif response['code'] == -100:
                self.send_log('检查屏蔽失败，联动用户的登录已失效，请暂停后重新设置', 'FAILURE')
                return '未知'
        except (KeyError, TypeError, AttributeError):
            return '未知'

        return '未知'

    def favorite_note(self, note: Union[NormalNote]):
        user_link = string.create_link(self.user.home_page, self.user.name, 12)
        note_link = string.create_link(note.note_url, note.note_title, 12)

        self.parent().msleep(100)

        self.parent().check_paused()
        self.parent().check_stop()

        for _ in range(3):
            try:
                self.parent().msleep(985)
                response = self.api.collect_note(note.id)
                logger.debug(f'收藏笔记({_ + 1})：{note.id} - {response}')

                if response['success'] and response['msg'] == '成功':
                    self.send_log(f'用户{self.user.name}对{note.note_type}类型笔记{note_link}进行了收藏', 'NORMAL')
                elif not response['success'] and response['code'] == -100:
                    self.user.available = 0
                    self.send_log(f'收藏失败，用户{user_link}登录已失效', 'FAILURE')
                else:
                    logger.exception(f'favorite_note_failure: {response}')
                    self.send_log(f'{note.note_type}类型的笔记{note_link}收藏失败，可查看软件日志', 'FAILURE')
                return None
            except requests.exceptions.ConnectionError:
                continue


class UnitStop(Exception):
    pass


class Unit(QtCore.QThread):
    sendLog = QtCore.Signal(str, str)
    currentChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.id = pcid.get_short_id()
        self.state = UnitState.READY
        self.tasks: List[Tasker] = []
        self.root_config: Optional[Config] = None
        self.current_tasker: Optional[Tasker] = None
        self.current_stage: Union[int] = 0
        self.notes: List[NormalNote] = []
        self.hash_notes: Set[NormalNote] = set()
        self.is_wait_import: Union[bool] = False
        self.import_notes: List[NormalNote] = []
        self.success_notes: List[NormalNote] = []
        self.hash_success_notes: Set[NormalNote] = set()
        self.failure_notes: List[NormalNote] = []
        self.hash_failure_notes: Set[NormalNote] = set()
        self.uncomment_notes: List[NormalNote] = []
        self.hash_uncomment_notes: Set[NormalNote] = set()

    def insert_tabview(self, tab_view, tab_icon=None, tab_name=None):
        self.state = UnitState.RUNNING
        tab_name = tab_name or self.root_config.name
        tab_name = string.truncate(tab_name, 10)
        if tab_icon is None:
            tab_view.addTab(self.parent(), tab_name)
        else:
            tab_view.addTab(self.parent(), tab_icon, tab_name)

    def send_log(self, text: str = '', level: str = 'EMPTY'):
        self.sendLog.emit(text, level)

    def run(self):
        self.state = UnitState.RUNNING

        for tasker in self.tasks:
            # 如果用户已经被其他线程竞争使用了
            # 那么就等待其他线程执行完毕，直到 working 恢复到 False
            while tasker.user.working:
                self.sleep(1)

            self.current_stage += 1
            self.current_tasker = tasker
            self.current_tasker.user.working = True
            self.currentChanged.emit(self.current_stage)

            self.check_paused()
            try:
                self.check_stop()
            except UnitStop:
                self.send_log('当前单元已被用户手动停止', 'WARNING')
                self.current_tasker.user.working = False
                break

            if self.state == UnitState.RUNNING:
                try:
                    tasker.is_allow = False
                    if tasker.allow_running:
                        tasker.run()
                        self.send_log(f'第{self.current_stage}阶段，用户{tasker.user.name}已处理完所有笔记', 'SUCCESS')
                    else:
                        self.send_log(f'第{self.current_stage}阶段被设置为取消执行，已跳过', 'SUCCESS')

                    self.send_log()
                    self.sleep(1)
                except UnitStop:
                    self.send_log('当前单元已被用户手动停止', 'WARNING')
                    self.current_tasker.user.working = False
                    break
                except Exception as e:
                    logger.exception(e)
                    self.send_log('当前阶段发生了意料之外的异常，详情可查看软件日志', 'FAILURE')

            self.current_tasker.user.working = False

        self.state = UnitState.STOP

    def check_paused(self):
        while self.state == UnitState.PAUSED:
            self.sleep(1)

    def check_stop(self):
        if self.state == UnitState.STOP:
            raise UnitStop

    def pause(self):
        if self.state != UnitState.STOP:
            self.state = UnitState.PAUSED

    def resume(self):
        if self.state != UnitState.STOP:
            self.state = UnitState.RUNNING

    def stop(self):
        self.state = UnitState.STOP


class BaseCenter(Generic[T]):
    path: Union[str, PathLike, PurePath] = CONFIG_FILE
    data: List[T] = []

    @staticmethod
    def get_chrome_path():
        try:
            key = RegOpenKey(
                HKEY_LOCAL_MACHINE,
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe',
                0,
                KEY_READ
            )
            chrome_path = RegQueryValueEx(key, "")[0]
            key.close()
            return chrome_path
        except Exception as e:
            logger.error(f'获取浏览器路径失败：{str(e)}')
            return ""

    @classmethod
    def _validate_data(cls, data: dict) -> dict:
        data = defaultdict(dict, data)
        data['core'] = defaultdict(list, data['core'])
        data['core']['configs'] = data['core'].get('configs', [])
        data['core']['users'] = data['core'].get('users', [])
        data['core']['at_users'] = data['core'].get('at_users', [])
        data['base'] = defaultdict(dict, data['base'])
        data['base']['cookies'] = data['base'].get('cookies', {})
        data['base']['template'] = data['base'].get('template', {})
        data['base']['target_note_id'] = data['base'].get('target_note_id', '')
        data['base']['target_note_xsec_token'] = data['base'].get('target_note_xsec_token', '')
        data['base']['linked_user_session'] = data['base'].get('linked_user_session', '')
        data['base']['browser_path'] = data['base'].get('browser_path', cls.get_chrome_path())
        data['base']['startup_check_update'] = data['base'].get('startup_check_update', True)
        data['base']['auto_rename'] = data['base'].get('auto_rename', False)
        data['base']['preview_min_time'] = data['base'].get('preview_min_time', 3)
        data['base']['train_strategy'] = data['base'].get('train_strategy', train_strategy)
        data['base']['after_check_seconds'] = data['base'].get('after_check_seconds', 6.0)
        return data

    @classmethod
    def check_valid(cls):
        try:
            raw_data = toml.load(str(cls.path))
            new_data = cls._validate_data(raw_data)
            with open(cls.path, 'w', encoding='utf-8') as fw:
                toml.dump(new_data, fw)
        except FileNotFoundError:
            with open(cls.path, 'w', encoding='utf-8') as fw:
                toml.dump(toml_template, fw)

    @classmethod
    def load(cls):
        raise NotImplementedError

    @classmethod
    def save(cls):
        raise NotImplementedError

    @classmethod
    def append(cls, item: T):
        cls.data.append(item)

    @classmethod
    def pop(cls, index: Union[int]):
        cls.data.pop(index)

    @classmethod
    def remove(cls, item: T):
        cls.data.remove(item)

    @classmethod
    def index(cls, value: Union[T, str]) -> Union[int]:
        if isinstance(value, str):
            return next((i for i, data in enumerate(cls.data) if data.id == value), -1)
        elif isinstance(value, Object):
            return next((i for i, data in enumerate(cls.data) if data == value), -1)
        else:
            return -1

    @classmethod
    def find(cls, value: Union[str, int]) -> Union[T, None]:
        if isinstance(value, str):
            return next((data for data in cls.data if data.id == value), None)
        elif isinstance(value, int):
            return cls.data[value]
        else:
            return None


class ConfigCenter(BaseCenter[Config]):
    data = []

    @classmethod
    def load(cls):
        cls.data.clear()
        data = toml.load(str(cls.path))
        if 'core' in data and 'configs' in data['core']:
            configs = data['core']['configs']
            for config in configs:
                config_obj = Config.from_dict(config)
                if config_obj:
                    # 依赖项 推荐采集 必须 开启相似度筛选
                    if config_obj.collect_type == 2:
                        config_obj.is_similarity_filter = True
                    cls.data.append(config_obj)

    @classmethod
    def save(cls):
        configs = [config_obj.to_dict() for config_obj in cls.data]

        data = toml.load(str(cls.path))
        if 'core' not in data:
            data['core'] = {}

        data['core']['configs'] = configs

        with open(str(cls.path), 'w', encoding='utf-8') as fw:
            toml.dump(data, fw)


class AtUserCenter(BaseCenter[AtUser]):
    data = []

    @classmethod
    def load(cls):
        cls.data.clear()
        data = toml.load(str(cls.path))
        if 'core' in data and 'at_users' in data['core']:
            at_users = data['core']['at_users']
            for at_user in at_users:
                at_user_obj = AtUser.from_dict(at_user)
                if at_user_obj:
                    cls.data.append(at_user_obj)

    @classmethod
    def save(cls):
        at_users = [at_user_obj.to_dict() for at_user_obj in cls.data]

        data = toml.load(str(cls.path))
        if 'core' not in data:
            data['core'] = {}

        data['core']['at_users'] = at_users

        with open(str(cls.path), 'w', encoding='utf-8') as fw:
            toml.dump(data, fw)


class PrivateUserCenter(BaseCenter[PrivateUser]):
    data = []

    @classmethod
    def load(cls):
        cls.data.clear()
        data = toml.load(str(cls.path))
        if 'core' in data and 'users' in data['core']:
            users = data['core']['users']
            for user in users:
                user_obj = PrivateUser.from_dict(user)
                if user_obj:
                    cls.data.append(user_obj)

    @classmethod
    def save(cls):
        users = [user_obj.to_dict() for user_obj in cls.data]

        data = toml.load(str(cls.path))
        if 'core' not in data:
            data['core'] = {}

        data['core']['users'] = users

        with open(str(cls.path), 'w', encoding='utf-8') as fw:
            toml.dump(data, fw)


class Cookies:
    _state = dict()

    def __init__(self, raw: Union[str, Dict[str, str]]):
        if isinstance(raw, str):
            self.data = self.from_string(raw)
        elif isinstance(raw, dict):
            self.data = raw
        else:
            self.data = dict()

    def check_keys(self, keys: set):
        self._state.clear()
        is_valid = True
        for key in keys:
            if key not in self.data.keys():
                self._state[key] = '并不存在'
                is_valid = False

        return is_valid

    def to_string(self):
        return '; '.join((f'{k}={v}' for k, v in self.data.items()))

    def from_string(self, raw: Union[str]):
        _items = (item.strip().split('=') for item in raw.split(';'))
        self.data = {item[0]: item[1] for item in _items if len(item) == 2}
        return self.data

    def logs(self, log_type=dict):
        if log_type == str:
            return '\n'.join((f'键 {k} {v}' for k, v in self._state.items()))
        return self._state


class TomlBase:
    path: Union[str, PathLike, PurePath] = CONFIG_FILE
    template: Union[Config] = None
    cookies: Union[dict] = {}
    target_note_id: Union[str] = None
    target_note_xsec_token: Union[str] = None
    linked_user_session: Union[str] = None
    auto_rename: Union[bool] = False
    browser_path: Union[str] = None
    after_check_seconds: Union[float] = 6.0
    preview_min_time: Union[int] = 3
    train_strategy: List[Union[str]] = train_strategy

    @classmethod
    def load(cls):
        data = toml.load(str(cls.path))
        if 'base' in data:
            # 导入配置模板
            if 'template' in data['base']:
                template_dict = data['base']['template']
                cls.template = Config.from_dict(template_dict)
                if cls.template is None:
                    cls.template = Config('配置模板')
            # 导入基础 CK
            if 'cookies' in data['base']:
                cookies_dict = data['base']['cookies']
                if 'web_session' in cookies_dict:
                    cookies_dict['web_session'] = ''
                cls.cookies = cookies_dict
            # 批量检测屏蔽时所用的笔记 ID
            if 'target_note_id' in data['base']:
                target_note_id = data['base']['target_note_id']
                cls.target_note_id = target_note_id if isinstance(target_note_id, str) else ''
            # 批量检测屏蔽时所用的笔记 Xsec_token
            if 'target_note_xsec_token' in data['base']:
                target_note_xsec_token = data['base']['target_note_xsec_token']
                cls.target_note_xsec_token = target_note_xsec_token if isinstance(target_note_xsec_token,
                                                                                  str) else ''

            # 新增笔记/导入笔记时所用的 session
            if 'linked_user_session' in data['base']:
                linked_user_session = data['base']['linked_user_session']
                cls.linked_user_session = linked_user_session if isinstance(linked_user_session, str) else ''
            # 导入是否自动命名
            if 'auto_rename' in data['base']:
                auto_rename = data['base']['auto_rename']
                cls.auto_rename = auto_rename if isinstance(auto_rename, bool) else False
            # 浏览器路径
            if 'browser_path' in data['base']:
                browser_path = data['base']['browser_path']
                cls.browser_path = browser_path if isinstance(browser_path, str) else ''
            # 多少秒后检查屏蔽
            if 'after_check_seconds' in data['base']:
                after_check_seconds = data['base']['after_check_seconds']
                cls.after_check_seconds = after_check_seconds if isinstance(after_check_seconds, float) else 6.0
            # 养号预览笔记最低时间
            if 'preview_min_time' in data['base']:
                preview_min_time = data['base']['preview_min_time']
                cls.preview_min_time = preview_min_time if isinstance(preview_min_time, int) else 3
            # 养号策略设置
            if 'train_strategy' in data['base']:
                temp_train_strategy = data['base']['train_strategy']
                cls.train_strategy = [s for s in temp_train_strategy if s in train_strategy]

    @classmethod
    def save(cls):
        data = toml.load(str(cls.path))
        if 'base' not in data:
            data['base'] = {}

        # 写入配置模板
        if cls.template:
            template_dict = cls.template.to_dict()
            data['base']['template'] = template_dict
        # 写入基础 CK
        if 'web_session' in cls.cookies:
            cls.cookies['web_session'] = ''
        cls.cookies.pop('x-user-id-creator.xiaohongshu.com', None)
        cls.cookies.pop('access-token-creator.xiaohongshu.com', None)
        cls.cookies.pop('customer-sso-sid', None)
        cls.cookies.pop('customerClientId', None)
        cls.cookies.pop('unread', None)
        data['base']['cookies'] = cls.cookies
        # 写入目标检查笔记的 Note ID
        data['base']['target_note_id'] = cls.target_note_id if cls.target_note_id else ''
        # 写入目标检查笔记的 Xsec_token
        data['base']['target_note_xsec_token'] = cls.target_note_xsec_token if cls.target_note_xsec_token else ''
        # 写入创建笔记/导入笔记所用的 session
        data['base']['linked_user_session'] = cls.linked_user_session if cls.linked_user_session else ''
        # 写入是否自动命名
        data['base']['auto_rename'] = cls.auto_rename
        # 写入浏览器路径
        data['base']['browser_path'] = cls.browser_path
        # 写入多少秒后检查屏蔽
        data['base']['after_check_seconds'] = cls.after_check_seconds
        # 写入养号预览笔记多少秒（最低值）
        data['base']['preview_min_time'] = cls.preview_min_time
        # 写入养号策略列表
        data['base']['train_strategy'] = [s for s in cls.train_strategy if s in train_strategy]

        with open(str(cls.path), 'w', encoding='utf-8') as fw:
            toml.dump(data, fw)


class MigrateConfig:
    """
    旧版本配置迁移到新版本
    """

    old_path = ROOT_DIR / 'config.json'
    old_backup_path = ROOT_DIR / 'config.backup.json'
    new_path = CONFIG_FILE

    # new_path = ROOT_DIR / 'config.bb.toml'

    def __init__(self):
        self.old_data = {}
        self.new_data = copy.deepcopy(toml_template)
        self.message = {
            '_migrate_base': False,
            '_migrate_config': False,
            '_migrate_user': False,
            '_migrate_at_user': False,
        }

    def old_config_exist(self):
        return self.old_path.exists()

    def _load_old_config(self):
        with self.old_path.open('r', encoding='utf-8') as fr:
            self.old_data = json.load(fr)

    def _migrate_base(self):
        try:
            self.new_data['base']['target_note_id'] = settings.value('gpa-khs-check-shield-note', '')
            self.new_data['base']['linked_user_session'] = settings.value('gpa-khs-add-note-user', '')
            self.new_data['base']['startup_check_update'] = bool(settings.value('gpa-khs-startup-check', 1))
            self.new_data['base']['auto_rename'] = bool(settings.value('gpa-khs-auto-rename', 0))
            self.new_data['base']['cookies'] = json.loads(settings.value('gpa-khs-cookies', '{}'))
            self.new_data['base']['template'] = {}
            self.new_data['base']['browser_path'] = ''
            old_template = self.old_data.get('config_template')
            if not old_template and not isinstance(old_template, dict):
                return None
            self.new_data['base']['template']['id'] = old_template.get('id')
            self.new_data['base']['template']['name'] = '配置模版'
            self.new_data['base']['template']['collect_type'] = 1
            self.new_data['base']['template']['keywords'] = old_template.get('keywords', [])
            self.new_data['base']['template']['note_type'] = old_template.get('classify_type', '采集全部')
            self.new_data['base']['template']['sort_method'] = old_template.get('sort_type', '最新')
            self.new_data['base']['template']['is_similarity_filter'] = False
            self.new_data['base']['template']['similarity_lower_limit'] = 0.10
            self.new_data['base']['template']['similarity_keywords'] = []
            self.new_data['base']['template']['is_comment'] = old_template.get('comment_note', False)
            self.new_data['base']['template']['is_fav_no_comment'] = old_template.get('skip_collect', False)
            self.new_data['base']['template']['is_comment_fav'] = old_template.get('collect_note', False)
            self.new_data['base']['template']['is_check_block'] = old_template.get('check_shield', False)
            self.new_data['base']['template']['uncommon_char_mode'] = old_template.get('rare_word_mode', 'append')
            self.new_data['base']['template']['uncommon_char_count'] = old_template.get('rare_word_count', 0)
            self.new_data['base']['template']['is_linked_check'] = False
            self.new_data['base']['template']['is_skip_over_comment'] = False
            self.new_data['base']['template']['comment_threshold'] = 0
            self.new_data['base']['template']['is_consecutive_block_stop'] = False
            self.new_data['base']['template']['consecutive_block_threshold'] = 0
            self.new_data['base']['template']['is_overall_block_stop'] = False
            self.new_data['base']['template']['overall_block_threshold'] = 0
            self.new_data['base']['template']['is_retry_after_block'] = old_template.get('try_shield', False)
            self.new_data['base']['template']['retry_count'] = old_template.get('retry_number', 0)
            self.new_data['base']['template']['is_retry_comment_random'] = old_template.get('retry_comment_random',
                                                                                            False)
            self.new_data['base']['template']['retry_interval'] = old_template.get('retry_inter_time', 1.0)
            self.new_data['base']['template']['comments'] = []
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def _migrate_config(self):
        try:
            self.new_data['core']['configs'] = []
            old_configs = self.old_data['configs']
            for old_config in old_configs:
                new_config = {'id': old_config.get('id'), 'name': old_config.get('name', '未检测到配置名称'),
                              'collect_type': 1, 'keywords': old_config.get('keywords', []),
                              'note_type': old_config.get('classify_type', '采集全部'),
                              'sort_method': old_config.get('sort_type', '最新'), 'is_similarity_filter': False,
                              'similarity_lower_limit': 0.10, 'similarity_keywords': [],
                              'is_comment': old_config.get('comment_note', False),
                              'is_fav_no_comment': old_config.get('skip_collect', False),
                              'is_comment_fav': old_config.get('collect_note', False),
                              'is_check_block': old_config.get('check_shield', False),
                              'uncommon_char_mode': old_config.get('rare_word_mode', 'append'),
                              'uncommon_char_count': old_config.get('rare_word_count', 0), 'is_linked_check': False,
                              'is_skip_over_comment': False, 'comment_threshold': 0, 'is_consecutive_block_stop': False,
                              'consecutive_block_threshold': 0, 'is_overall_block_stop': False,
                              'overall_block_threshold': 0, 'is_retry_after_block': old_config.get('try_shield', False),
                              'retry_count': old_config.get('retry_number', 0),
                              'is_retry_comment_random': old_config.get('retry_comment_random',
                                                                        False),
                              'retry_interval': old_config.get('retry_inter_time', 1.0), 'comments': []}
                old_comments = old_config['comments']
                for old_comment in old_comments:
                    new_comment = {'content': '', 'at_users': []}
                    if old_comment and old_comment[0]:
                        new_comment['content'] = old_comment[0]
                        old_at_users = old_comment[1]
                        for old_at_user in old_at_users:
                            new_at_user = {'id': '', 'name': '', 'home_page': '', 'remark': ''}
                            if old_at_user:
                                new_at_user['name'] = old_at_user['nickname']
                                new_at_user['id'] = old_at_user['user_id']
                                new_at_user[
                                    'home_page'] = f'https://www.xiaohongshu.com/user/profile/{old_at_user["user_id"]}'
                                new_comment['at_users'].append(new_at_user)
                        new_config['comments'].append(new_comment)
                self.new_data['core']['configs'].append(new_config)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def _migrate_user(self):
        try:
            self.new_data['core']['users'] = []
            old_users = self.old_data['users']
            for old_user in old_users:
                new_user = {
                    'id': '', 'name': '', 'home_page': '', 'session': '', 'remark': '',
                    'working': False, 'available': -1, 'comment_state': -1,
                    'create_time': '', 'modify_time': ''
                }
                if old_user and isinstance(old_user, dict):
                    new_user['name'] = old_user['nickname']
                    new_user['id'] = old_user['user_id']
                    new_user['home_page'] = f'https://www.xiaohongshu.com/user/profile/{old_user["user_id"]}'
                    new_user['session'] = old_user['session']
                    new_user['remark'] = old_user.get('remark', '')
                    new_user['working'] = old_user.get('working', False)
                    new_user['available'] = old_user.get('available', -1)
                    new_user['comment_state'] = old_user.get('comment_state', -1)
                    new_user['create_time'] = old_user.get('create_time',
                                                           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    new_user['modify_time'] = old_user.get('modify_time',
                                                           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                    self.new_data['core']['users'].append(new_user)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def _migrate_at_user(self):
        try:
            self.new_data['core']['at_users'] = []
            old_users = self.old_data['users']
            for old_user in old_users:
                new_user = {'id': '', 'name': '', 'home_page': '', 'remark': '', }
                if old_user and isinstance(old_user, dict):
                    new_user['name'] = old_user['nickname']
                    new_user['id'] = old_user['user_id']
                    new_user['home_page'] = f'https://www.xiaohongshu.com/user/profile/{old_user["user_id"]}'
                    new_user['remark'] = old_user.get('remark', '')
                    self.new_data['core']['at_users'].append(new_user)
                return True
        except Exception as e:
            logger.exception(e)
            return False

    def migrate(self):
        self._load_old_config()
        if not self.old_data:
            return None

        self.message['_migrate_base'] = self._migrate_base()
        self.message['_migrate_config'] = self._migrate_config()
        self.message['_migrate_user'] = self._migrate_user()
        self.message['_migrate_at_user'] = self._migrate_at_user()

        migrate_result = all(self.message.values())
        if migrate_result:
            try:
                with open(self.new_path, 'w', encoding='utf-8') as fw:
                    toml.dump(self.new_data, fw)
            except Exception as e:
                logger.exception(e)
                migrate_result = False

        if migrate_result:
            try:
                with open(self.old_backup_path, 'w', encoding='utf-8') as fw:
                    json.dump(self.old_data, fw, ensure_ascii=False, indent=4)
            except Exception as e:
                logger.exception(e)
            self.old_path.unlink()

        return migrate_result


class BackupConfig:
    backup_path = ROOT_DIR / 'config.backup.toml'
    restore_path = CONFIG_FILE

    @classmethod
    def backup(cls):
        result = True
        try:
            with cls.restore_path.open('r', encoding='utf-8') as fr:
                with cls.backup_path.open('w', encoding='utf-8') as fw:
                    fw.write(fr.read())
        except Exception as e:
            logger.exception(e)
            result = False

        return result

    @classmethod
    def restore(cls):
        result = True
        try:
            with cls.backup_path.open('r', encoding='utf-8') as fr:
                with cls.restore_path.open('w', encoding='utf-8') as fw:
                    fw.write(fr.read())
        except Exception as e:
            logger.exception(e)
            result = False

        return result
