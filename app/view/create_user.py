import xhs
import typing as t
from loguru import logger
from app.lib import QtCore, QtWidgets, QtGui
from app.lib.factory import PrivateUser, LoginQrCode, PrivateUserCenter, PrivateUserFactory
from app.lib.threads import NetworkPool
from app.utils.string import validate_web_session, validate_user_id
from app.ui import qrcode_create_user_ui, mobile_create_user_ui, manual_create_user_ui


class QrcodeCreateUser(QtWidgets.QDialog):
    # fixed: 修复创建单元添加时重复添加的情况
    created = QtCore.Signal(PrivateUser, bool)  # 用户、是否为新用户

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.ui = qrcode_create_user_ui.Ui_QrcodeCreateUser()
        self.ui.setupUi(self)
        self.build_init_datas()
        self.connect_ui_events()
        self.service_deployment()

    def build_init_datas(self):
        """
        构建初始的数据 控件参数
        :return:
        """
        self.factory = PrivateUserFactory()
        self.ui.remark_te.setFocus()
        self.reset_relative_parameters()

    def connect_ui_events(self):
        """
        连接各个控件的槽函数与信号
        :return:
        """
        self.ui.refresh_qrcode_btn.clicked.connect(self.handle_refresh_qrcode_click)
        self.ui.confirm_button.clicked.connect(self.handle_confirm_btn_click)
        self.ui.check_button.clicked.connect(self.handle_check_btn_click)

    def service_deployment(self):
        self.network_pool = NetworkPool(parent=self)

    def reset_relative_parameters(self):
        self.factory.retrieve_qrcode_params()
        self.login_qrcode: t.Optional[LoginQrCode] = None
        self.login_user: t.Optional[PrivateUser] = None
        self.ui.check_button.setEnabled(True)
        self.ui.label_nickname.setText('')
        self.ui.label_user_id.setText('')
        self.ui.remark_te.setText('')

    def handle_refresh_qrcode_click(self):
        self.reset_relative_parameters()
        self.ui.refresh_qrcode_btn.setEnabled(False)
        create_qrcode_signals = self.network_pool.start_task(
            xhs.API().set_cookies(self.factory.make_cookies()).create_qrcode)
        create_qrcode_signals.success.connect(self.on_create_qrcode_success)
        create_qrcode_signals.finished.connect(lambda: self.ui.refresh_qrcode_btn.setEnabled(True))

    def on_create_qrcode_success(self, response: dict):
        try:
            url = response['data'].get('url') if response.get('data') else ''
            qr_id = response['data'].get('qr_id') if response.get('data') else ''
            code = response['data'].get('code') if response.get('data') else ''
            self.factory.import_qrcode_params(url, qr_id, code)
            self.login_qrcode = self.factory.make_qrcode()
            qr_img = QtGui.QImage()
            qr_img.loadFromData(self.login_qrcode.bytes, 'PNG')
            self.ui.label_qrcode.setPixmap(QtGui.QPixmap.fromImage(qr_img))
        except Exception as e:
            logger.error(f'Create qrcode: {response}')
            logger.exception(e)
            QtWidgets.QMessageBox.critical(self, '刷新失败', '获取二维码失败，请查看日志')

    def handle_check_btn_click(self):
        """
        处理`先检测`按钮的单击事件
        功能：根据 qr_id 与 code 去实现
        :return:
        """
        if self.login_qrcode:
            self.ui.check_button.setEnabled(False)
            check_qrcode_signals = self.network_pool.start_task(
                xhs.API().set_cookies(self.factory.make_cookies()).qrcode_status,
                self.login_qrcode.qr_id, self.login_qrcode.code
            )
            check_qrcode_signals.success.connect(self.on_check_qrcode_success)
            check_qrcode_signals.finished.connect(lambda: self.ui.check_button.setEnabled(True))
        else:
            QtWidgets.QMessageBox.critical(self, '检测失败', '当前二维码的相关数据未获取到，请稍后重试')

    def on_check_qrcode_success(self, response: dict):
        try:
            code_status = response['data'].get('code_status', -1) if response['data'] else -1
            if code_status == -1:
                QtWidgets.QMessageBox.critical(self, '登录失败', '当前二维码的登录状态暂未获取到')
            elif code_status == 0:
                QtWidgets.QMessageBox.warning(self, '登录失败', '请使用小红书或者微信扫码')
            elif code_status == 1:
                QtWidgets.QMessageBox.warning(self, '登录失败', '请务必在手机上确认登录')
            elif code_status == 2:
                session = response['data']['login_info']['session']
                cookies = self.factory.make_cookies(session)
                user_id = response['data']['login_info']['user_id']
                self.ui.label_user_id.setText(user_id)
                get_user_info = xhs.API().set_cookies(cookies).user_me()
                logger.debug(f'获取账号个人信息：{get_user_info}')
                if get_user_info.get('data'):
                    nickname = get_user_info['data'].get('nickname', '获取昵称失败')
                else:
                    nickname = '获取昵称失败'
                self.ui.label_nickname.setText(nickname)
                self.login_user = self.factory.make_user(user_id, nickname, session, '')
            elif code_status == 3:
                QtWidgets.QMessageBox.critical(self, '登录失败', '当前二维码已过期，请刷新二维码')
        except Exception as e:
            logger.exception(e)
            QtWidgets.QMessageBox.critical(self, '检测失败', '未知原因导致检测失败，请查看日志')

    def handle_confirm_btn_click(self):
        """
        处理`后添加`按钮的单击事件
        功能：添加用户到列表中
        :return:
        """
        if self.login_user and self.login_user.session:
            self.login_user.remark = self.ui.remark_te.toPlainText()

            if self.login_user in PrivateUserCenter.data:
                self.created.emit(self.login_user, False)
            else:
                self.created.emit(self.login_user, True)
                PrivateUserCenter.append(self.login_user)

            PrivateUserCenter.save()

            result = QtWidgets.QMessageBox.information(
                self, '添加成功', f'账号{self.login_user.name}已添加成功。\n继续添加还是退出？',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel
            )
            if result == QtWidgets.QMessageBox.StandardButton.Yes:
                self.handle_refresh_qrcode_click()
            else:
                self.close()
        else:
            QtWidgets.QMessageBox.critical(self, '添加失败', '暂未检测到用户已登录')


class MobileCreateUser(QtWidgets.QDialog):
    created = QtCore.Signal(PrivateUser, bool)  # 用户、是否为新用户

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.ui = mobile_create_user_ui.Ui_MobileCreateUser()
        self.ui.setupUi(self)
        self.build_init_datas()
        self.connect_ui_events()
        self.service_deployment()

    def build_init_datas(self):
        """
        构建初始的数据 控件参数
        :return:
        """
        self.factory = PrivateUserFactory()
        self.reset_relative_parameters()

    def connect_ui_events(self):
        """
        连接各个控件的槽函数与信号
        :return:
        """
        self.ui.cancel_btn.clicked.connect(self.close)
        self.ui.get_code_btn.clicked.connect(self.handle_get_code_click)
        self.ui.create_btn.clicked.connect(self.handle_create_btn_clik(need_close=False))
        self.ui.create_close_btn.clicked.connect(self.handle_create_btn_clik(need_close=True))

    def service_deployment(self):
        self.network_pool = NetworkPool(parent=self)

    def reset_relative_parameters(self):
        self.ui.phone_number_le.setFocus()
        self.ui.create_btn.setEnabled(True)
        self.ui.create_close_btn.setEnabled(True)

    def handle_get_code_click(self):
        phone_number = self.ui.phone_number_le.text().strip()
        zone_number = self.ui.zone_code_le.text().strip()

        if not phone_number:
            QtWidgets.QMessageBox.critical(self, '发送失败', '请填写手机号码')
            return None

        if not zone_number:
            QtWidgets.QMessageBox.critical(self, '发送失败', '请填写手机区域码')
            return None

        self.ui.get_code_btn.setEnabled(False)

        signals = self.network_pool.start_task(
            xhs.API().set_cookies(self.factory.make_cookies()).mobile_send_code,
            phone_number, zone_number
        )
        signals.success.connect(self.on_get_code_success)
        signals.failure.connect(self.on_get_code_failure)
        signals.finished.connect(self.on_get_code_finished)

    def on_get_code_success(self, response: dict):
        if not isinstance(response, dict):
            QtWidgets.QMessageBox.critical(self, '发送失败', '发送验证码失败，请求后的响应内容不被支持')
            return None

        if response.get('code', -1) != 0:
            QtWidgets.QMessageBox.critical(self, '发送失败', response['msg'])
            return None

        QtWidgets.QMessageBox.information(self, '发送成功', '验证码已发送，请稍后核对短信最新消息')

    def on_get_code_failure(self, error: Exception):
        logger.exception(error)
        QtWidgets.QMessageBox.critical(self, '响应解析失败', '发送验证码的响应失败，请查看软件日志')

    def on_get_code_finished(self):
        self.ui.get_code_btn.setEnabled(True)

    def handle_create_btn_clik(self, need_close: bool):
        def wrapper():
            phone_number = self.ui.phone_number_le.text().strip()
            zone_number = self.ui.zone_code_le.text().strip()
            verify_code = self.ui.sms_code_le.text().strip()

            if not phone_number:
                QtWidgets.QMessageBox.critical(self, '添加失败', '请填写手机号码')
                return None

            if not zone_number:
                QtWidgets.QMessageBox.critical(self, '添加失败', '请填写手机区域码')
                return None

            if not verify_code:
                QtWidgets.QMessageBox.critical(self, '添加失败', '请填写手机验证码')
                return None

            self.ui.create_btn.setEnabled(False)
            self.ui.create_close_btn.setEnabled(False)

            signals = self.network_pool.start_task(
                xhs.API().set_cookies(self.factory.make_cookies()).mobile_check_code,
                phone_number, verify_code, zone_number
            )
            signals.success.connect(self.on_create_user_success(phone_number, zone_number, need_close=need_close))
            signals.failure.connect(self.on_create_user_failure)
            signals.finished.connect(self.on_create_user_finished)

        return wrapper

    def on_create_user_success(self, phone_number, zone_number, need_close):
        def wrapper(response: dict):
            if not isinstance(response, dict):
                QtWidgets.QMessageBox.critical(self, '添加失败', '检查验证码失败，请求后的响应内容不被支持')
                return None

            if response.get('code', -1) != 0:
                QtWidgets.QMessageBox.critical(self, '添加失败', response['msg'])
                return None

            if 'data' not in response or 'mobile_token' not in response['data']:
                QtWidgets.QMessageBox.critical(self, '添加失败', response['msg'])
                return None

            mobile_token = response['data']['mobile_token']
            use_response = xhs.API().set_cookies(self.factory.make_cookies()).mobile_use_code(
                phone_number, mobile_token, zone_number)
            logger.debug(f'使用验证码后的响应：{use_response}')
            if 'data' not in use_response or use_response['code'] != 0:
                QtWidgets.QMessageBox.critical(self, '添加失败', response['msg'])
                return None

            session = use_response['data'].get('session', '')
            if not validate_web_session(session):
                QtWidgets.QMessageBox.critical(self, '添加失败', '获取的 Web Session 不合法')
                return None

            user_id = use_response['data'].get('user_id', '')
            if not validate_user_id(user_id):
                QtWidgets.QMessageBox.critical(self, '添加失败', '获取的 User ID 不合法')
                return None

            cookies = self.factory.make_cookies(session)
            me_info = xhs.API().set_cookies(cookies).user_me()
            logger.debug(f'获取账号个人信息：{me_info}')
            nickname = me_info['data'].get('nickname', '获取昵称失败')
            self._append_or_update_user(user_id, nickname, session, need_close)

        return wrapper

    def on_create_user_failure(self, error: Exception):
        logger.exception(error)
        QtWidgets.QMessageBox.critical(self, '添加失败', f'发起创建请求失败（详情查看日志）：\n{str(error)}')

    def on_create_user_finished(self):
        self.reset_relative_parameters()

    def _append_or_update_user(self, user_id, nickname, session, need_close=False):
        login_user = self.factory.make_user(user_id, nickname, session, '')
        if login_user and login_user.session:
            login_user.remark = self.ui.remark_te.toPlainText()

            if login_user in PrivateUserCenter.data:
                self.created.emit(login_user, False)
            else:
                self.created.emit(login_user, True)
                PrivateUserCenter.append(login_user)

            PrivateUserCenter.save()
            if need_close:
                self.close()
            else:
                QtWidgets.QMessageBox.information(self, '添加成功', f'用户{nickname}已添加')
        else:
            QtWidgets.QMessageBox.critical(self, '添加失败', '用户工厂创建用户失败')


class ManualCreateUser(QtWidgets.QDialog):
    created = QtCore.Signal(PrivateUser, bool)  # 用户、是否为新用户

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.ui = manual_create_user_ui.Ui_ManualCreateUser()
        self.ui.setupUi(self)
        self.build_init_datas()
        self.connect_ui_events()
        self.service_deployment()

    def build_init_datas(self):
        """
        构建初始的数据 控件参数
        :return:
        """
        self.factory = PrivateUserFactory()
        self.reset_relative_parameters()

    def connect_ui_events(self):
        """
        连接各个控件的槽函数与信号
        :return:
        """
        self.ui.cancel_btn.clicked.connect(self.close)
        self.ui.create_btn.clicked.connect(self.handle_create_btn_clik(need_close=False))
        self.ui.create_close_btn.clicked.connect(self.handle_create_btn_clik(need_close=True))

    def service_deployment(self):
        self.network_pool = NetworkPool(parent=self)

    def reset_relative_parameters(self):
        self.ui.session_le.setFocus()
        self.ui.create_btn.setEnabled(True)
        self.ui.create_close_btn.setEnabled(True)

    def handle_create_btn_clik(self, need_close: bool):
        def wrapper():
            session = self.ui.session_le.text().strip()

            if not validate_web_session(session):
                QtWidgets.QMessageBox.critical(self, '添加失败', '必须填写有效的 session 值')
                return None

            self.ui.create_btn.setEnabled(False)
            self.ui.create_close_btn.setEnabled(False)

            signals = self.network_pool.start_task(
                xhs.API().set_cookies(self.factory.make_cookies(session)).user_me,
            )
            signals.success.connect(self.on_create_user_success(session, need_close=need_close))
            signals.failure.connect(self.on_create_user_failure)
            signals.finished.connect(self.on_create_user_finished)

        return wrapper

    def on_create_user_success(self, session, need_close):
        def wrapper(response: dict):
            if not isinstance(response, dict):
                QtWidgets.QMessageBox.critical(self, '添加失败', '获取用户请求失败，请求后的响应内容不被支持')
                return None

            if response.get('code', -1) != 0:
                QtWidgets.QMessageBox.critical(self, '添加失败', response['msg'])
                return None

            if 'data' not in response or not response['data']:
                QtWidgets.QMessageBox.critical(self, '添加失败', response['msg'])
                return None

            logger.debug(f'获取账号个人信息：{response}')
            nickname = response['data'].get('nickname', '获取昵称失败')
            user_id = response['data'].get('user_id', '')
            if not validate_user_id(user_id):
                QtWidgets.QMessageBox.critical(self, '添加失败', '获取用户的 User ID 失败')
                return None
            self._append_or_update_user(user_id, nickname, session, need_close)

        return wrapper

    def on_create_user_failure(self, error: Exception):
        logger.exception(error)
        QtWidgets.QMessageBox.critical(self, '添加失败', f'发起创建请求失败（详情查看日志）：\n{str(error)}')

    def on_create_user_finished(self):
        self.reset_relative_parameters()

    def _append_or_update_user(self, user_id, nickname, session, need_close=False):
        login_user = self.factory.make_user(user_id, nickname, session, '')
        if login_user and login_user.session:
            login_user.remark = self.ui.remark_te.toPlainText()

            if login_user in PrivateUserCenter.data:
                self.created.emit(login_user, False)
            else:
                self.created.emit(login_user, True)
                PrivateUserCenter.append(login_user)

            PrivateUserCenter.save()
            if need_close:
                self.close()
            else:
                QtWidgets.QMessageBox.information(self, '添加成功', f'用户{nickname}已添加')
        else:
            QtWidgets.QMessageBox.critical(self, '添加失败', '用户工厂创建用户失败')
