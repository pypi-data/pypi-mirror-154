# 薪行家代付nameko dependency


## install

```shell
pip install xxj-nameko-dependency
```

## config

通过yaml文件方式配置nameko环境变量

```
XXJ:
  MCHNT_NUM: ${XXJ_MCHNT_NUM}
  API_BASE_URL: ${XXJ_API_BASE_URL}
  DES_KEY: ${XXJ_DES_KEY}
  PUBLIC_KEY: ${XXJ_PUBLIC_KEY}
  PRIVATE_KEY: ${XXJ_PRIVATE_KEY}
```

## How to use?

```python
from xxj import XXJ

class TestService(Base):
    xxj = XXJ()

    @rpc
    def create_package(self, data):
        return self.xxj.call("remit/createpackage", data)
```


