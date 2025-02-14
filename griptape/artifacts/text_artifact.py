from __future__ import annotations
import json
from typing import TYPE_CHECKING, Optional
from attr import define, field
from griptape.artifacts import BaseArtifact

if TYPE_CHECKING:
    from griptape.drivers import BaseEmbeddingDriver
    from griptape.tokenizers import BaseTokenizer


@define(frozen=True)
class TextArtifact(BaseArtifact):
    value: str = field()
    __embedding: list[float] = field(factory=list, kw_only=True)

    @property
    def embedding(self) -> Optional[list[float]]:
        return None if len(self.__embedding) == 0 else self.__embedding

    @property
    def value_and_meta(self) -> str:
        return json.dumps({
            "value": self.value,
            "meta": self.meta
        })

    def __add__(self, other: TextArtifact) -> TextArtifact:
        return TextArtifact(self.value + other.value)

    def generate_embedding(self, driver: BaseEmbeddingDriver) -> list[float]:
        self.__embedding.clear()
        self.__embedding.extend(driver.embed_string(str(self.value)))

        return self.embedding

    def token_count(self, tokenizer: BaseTokenizer) -> int:
        return tokenizer.token_count(str(self.value))

    def to_text(self) -> str:
        return str(self.value)

    def to_dict(self) -> dict:
        from griptape.schemas import TextArtifactSchema

        return dict(TextArtifactSchema().dump(self))
