# email-control-ao

定义DDD概念中的基类，避免每个项目都自己定义。

# 打包上传
```bash
python3 -m pip install --upgrade setuptools wheel twine build

python3 -m build

python3 -m twine upload dist/*
```
# 下载使用
```bash
pip install email_control_ao
```
```python
import email_control_ao
```