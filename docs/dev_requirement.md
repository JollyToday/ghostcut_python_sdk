

# 需求

以`https://api.zhaoli.com/v-w-c/gateway/ve/work/free为例

```python
# 调用
ghostcut = Ghostcut()
free_input = FreeInput(
    urls = ["a", "b"],
    ...
)
# 后面resp也可以定义下数据结构，如果要定义，需要和琦玉那边确认下
resp = ghostcut.free(free_input)
```

```python
# free方法定义
from pydantic import BaseModel, Field, field_validator, field_serializer

class Ghostcut:
    ...
    def free(self, free_input: Dict[str, Any] | FreeInput) -> Dict[str, Any]:
        if not isinstance(free_input, FreeInput):
            free_input = FreeInput.model_validate(free_input)
        # requests中需要dict或json的地方，通过model_dump或model_dump_json转换为dict和str
        free_input_dict = free_input.model_dump(exclude_none=True)  
        free_input_json = free_input.model_dump_json(exclude_none=True)
        

# 一些类型, 譬如ExtraOptions的定义可以参考ghostcut_util/db/table_class和ghostcut_util/enums
class FreeInput(BaseModel):
    urls: List[str] = Field(description="需要处理的视频URL")
    names: List[str] | None = Field(default=None, description="作品名")
    extraOptions: ExtraOptions | None = Field(default=None, description="...") # 该字段文档中要求的类型是string，即json dumps后的字符串，但是为了便于用户定义还是复用ghost_util/db/table_class中的定义，然后通过field_validator和field_serializer定义反序列化和序列化方式。
    ... # 其他字段

    @field_validator("extraOptions", mode="before")
    @classmethod
    def validate_extra_options(cls, extra_options: str | None) -> ExtraOptions | None:
        if not extra_options:
            return None
        return ExtraOptions.model_validate_json(extra_options)

    @field_serializer("extraOptions")
    def serialize_extra_options(self, extra_options: ExtraOptions | None) -> str:
        if not extra_options:
            return ""
        return extra_options.model_dump_json(exclude_none=True)
```