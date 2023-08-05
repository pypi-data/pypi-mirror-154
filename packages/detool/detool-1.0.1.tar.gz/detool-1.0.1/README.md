[![Supported Versions](https://img.shields.io/pypi/pyversions/leek.svg)](https://pypi.org/project/leek)
### 常用装饰器工具集
                  
#### pip安装
```shell
pip install detool
```

#### 统计函数执行时长装饰器
```python
import time
from detool import timer_cost

@timer_cost
def t_time():
    time.sleep(0.01)
    print(123)
```