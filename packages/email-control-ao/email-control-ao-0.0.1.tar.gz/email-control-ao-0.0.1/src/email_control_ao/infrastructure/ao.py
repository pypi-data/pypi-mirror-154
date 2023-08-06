from typing import List, Optional
import requests, json
from ddd_objects.infrastructure.ao import exception_class_dec
from ddd_objects.domain.exception import return_codes
from log_control_ao import Logger
from .do import EmailInfoDO

logger = Logger(domain='email-control-ao', location=__file__, local=True)
class EmailController:
    def __init__(self, token:str, ip: str=None, port: int=None) -> None:
        if port is None:
            port = 8080
        if ip is None:
            ip = 'email-control-svc.system-service.svc.cluster.local'
        self.url = f"http://{ip}:{port}"
        self.header = {"api-token":token}

    def _check_error(self, status_code, info):
        if status_code>299:
            if isinstance(info['detail'], str):
                return_code = return_codes['OTHER_CODE']
                error_info = info['detail']
            else:
                return_code = info['detail']['return_code']
                error_info = info['detail']['error_info']
            logger.error(f'Error detected by email-control-ao:\nreturn code: {return_code}\n'
                f'error info: {error_info}')

    @exception_class_dec(max_try=1)
    def send_single_email(self, email: EmailInfoDO, timeout=3):
        try:
            data = json.dumps(email.to_json())
            response=requests.post(f'{self.url}/send-single-email', 
                data=data, timeout=timeout, headers=self.header)
            info = json.loads(response.text)
            self._check_error(response.status_code, info)
            return True
        except:
            logger.error(f'Error detected by email-control-ao when connecting to email server')
            return False

class Email:
    def __init__(
        self,
        token,
        sender=None,
        receiver=None,
        subject=None,
        ip = None,
        port = None
    ) -> None:
        if sender is None:
            sender = 'no-reply-single@dm.dhel.top'
        if receiver is None:
            receiver = 'wangziling100@163.com'
        if subject is None:
            subject = 'Test'
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.email_ao = EmailController(token, ip, port)

    def send(
        self,
        content:Optional[str], 
        subject:Optional[str]=None,
        receiver:Optional[str]=None, 
        html_content:Optional[str]=None, 
        timeout = 3
    ):
        if subject is None:
            subject = self.subject
        if receiver is None:
            receiver = self.receiver
        if content is None and html_content is None:
            content = 'This is just a test'
        email_info = EmailInfoDO(
            sender = self.sender,
            receiver = receiver,
            subject = subject,
            content = content,
            html_content = html_content
        )
        result = self.email_ao.send_single_email(email_info, timeout)
        if result.succeed:
            return True
        else:
            return False