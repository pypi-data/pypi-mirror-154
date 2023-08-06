# pymtts

A python package for using Azure smart AI speech

## sample use case

```python
from pymtts import async_Mtts
mtts = async_Mtts()
mp3_bytes_buffer = await mtts.mtts("欢迎使用pymtts","zh-CN-YunxiNeural", 'general', 0, 0, )
```