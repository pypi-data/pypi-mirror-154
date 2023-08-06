'''
# test-contruct-lib

test

fake minor version

another fake change
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import constructs


class HelloWorld(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="test-contruct-lib.HelloWorld",
):
    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="sayHello")
    def say_hello(self) -> None:
        return typing.cast(None, jsii.invoke(self, "sayHello", []))


__all__ = [
    "HelloWorld",
]

publication.publish()
