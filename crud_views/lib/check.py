import re
from typing import Any, Iterable, Type

from django.core.checks import Error, CheckMessage
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from pydantic import BaseModel

REGS = {
    "name": {
        "reg": re.compile(r"^[a-z_]+$"),
        "msg": "must be lowercase alpha with underscores"
    },
    "path": {
        "reg": re.compile(r"^$|^[a-z0-9_-]+(?:/[a-z0-9_-]+)*$"),
        "msg": "must be lowercase alpha with underscores and dashes and must not start or end with a slash"
    }
}


class Check(BaseModel):
    """
    Base class for checks
    """
    context: Type | object
    id: str
    msg: str | None = None

    def get_id(self) -> str:
        """
        error id
        """
        return f"viewset.{self.id}"

    def get_message_context(self) -> dict:
        return dict(
            context=self.context,
            id=self.id,
            eid=self.get_id(),
        )

    def get_message(self, msg: str = None) -> str:
        kwargs = self.get_message_context()
        if msg:
            msg.format(**kwargs)
        return self.msg.format(**kwargs)


class CheckAttribute(Check):
    """
    Check for attribute
    """
    id: str = "E100"
    attribute: str | None = None
    nullable: bool = False
    msg: str = "Attribute »{attribute}» does not exist or is not set at »{context}»"

    def get_message_context(self) -> dict:
        context = super().get_message_context()
        context.update(
            attribute=self.attribute,
            value=self.value,
        )
        return context

    @property
    def exists(self) -> bool:
        return hasattr(self.context, self.attribute)

    @property
    def value(self) -> Any:
        return getattr(self.context, self.attribute)

    def messages(self) -> Iterable[CheckMessage]:
        # yield from super().messages()
        if not self.exists or (self.value is None and not self.nullable):
            yield Error(id=self.get_id(), msg=self.get_message())


class CheckAttributeReg(CheckAttribute):
    """
    Check attribute against regex
    """
    reg: re.Pattern
    msg: str = "Attribute »{attribute}» value »{value}» does not match regex »{reg}» at »{context}»"

    def get_message_context(self) -> dict:
        context = super().get_message_context()
        context.update(
            reg=self.reg,
        )
        return context

    def messages(self) -> Iterable[CheckMessage]:
        yield from super().messages()
        if self.exists and not self.reg.match(self.value):
            yield Error(id=f"viewset.{self.id}", msg=self.get_message())


class CheckEitherAttribute(Check):
    """
    Check for either attribute
    """
    attribute1: str | None = None
    attribute2: str | None = None

    msg: str = "Neither »{attribute1}» not »{attribute2}» are set or are missing »{context}»"

    def get_message_context(self) -> dict:
        context = super().get_message_context()
        context.update(
            attribute1=self.attribute1,
            attribute2=self.attribute2,
            value1=self.value1,
            value2=self.value2,
        )
        return context

    @property
    def value1(self) -> Any:
        return getattr(self.context, self.attribute1, None)

    @property
    def value2(self) -> Any:
        return getattr(self.context, self.attribute2, None)

    def messages(self) -> Iterable[CheckMessage]:
        # yield from super().messages()

        if not self.value1 and not self.value2:
            yield Error(id=self.get_id(),
                        msg=self.get_message(
                            "Neither attribute »{attribute1}» nor attribute »{attribute2}» are set at »{context}»"))

        if self.value1 and self.value2:
            yield Error(id=self.get_id(),
                        msg=self.get_message(
                            "Both attributes »{attribute1}» and »{attribute2}» are set at »{context}»"))


class CheckAttributeTemplate(CheckAttribute):
    """
    Check for either attribute
    """
    id: str = "E203"
    msg: str = "Template »{attribute}» »{value}» not found at »{context}»"
    nullable: bool = True

    def messages(self) -> Iterable[CheckMessage]:
        yield from super().messages()
        if self.exists:
            try:
                get_template(self.value)
            except TemplateDoesNotExist as exc:
                yield Error(id=self.get_id(), msg=self.get_message())


class ContextActionCheck(Check):
    """
    Checks for context action
    """

    # todo: check when all apps are loaded
    msg: str = "Attribute »{attribute}» does not exist or is not set at »{context}»"

    def messages(self) -> Iterable[CheckMessage]:
        viewset = self.context.vs  # noqa
        actions = self.context.vs_context_actions or list()  # noqa
        for action in actions:  # noqa
            is_view = viewset.has_view(action)
            # is_special = action in viewset.special_keys
            # if not (is_view or is_special):
            #    yield Error(id=f"viewset.{self.id}", msg=f"{self.msg} at {self.context}: {action}")
            if not is_view:
                yield Error(id=f"viewset.{self.id}", msg=f"{self.msg} at {self.context}: {action}")


class CheckExpression(Check):
    expression: bool
    msg: str = "foo"

    def messages(self) -> Iterable[CheckMessage]:
        if not self.expression:
            yield Error(id=f"viewset.{self.id}", msg=f"{self.msg} at {self.context}")
