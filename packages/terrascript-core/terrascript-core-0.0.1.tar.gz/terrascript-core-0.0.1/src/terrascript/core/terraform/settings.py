from typing import Optional, Union

from ..lang.decorators import schema, schema_args
from ..lang.types import SchemaArgs, Schema
from ..lang.decorators import arg
from ..lang.terraform import Terraform
from .backend.local import Local
from .backend.remote import Remote
from .backend.s3 import S3


@schema
class RequiredProvider(Schema):
    @staticmethod
    def op_() -> str:
        return "="

    def __init__(
        self,
        *,
        version: str,
        source: str,
    ):
        super().__init__(
            RequiredProvider.Args(
                version=version,
                source=source,
            )
        )

    @schema_args
    class Args(SchemaArgs):
        """
        A version constraint specifying which subset of available provider versions
        the module is compatible with.
        """

        version: str = arg()

        """
        The global source address for the provider you intend to use, such as hashicorp/aws.
        """
        source: str = arg()


@schema
class RequiredProviders(Schema):
    def __init__(
        self,
        *,
        aws: Optional[RequiredProvider] = None,
        google: Optional[RequiredProvider] = None,
        azurerm: Optional[RequiredProvider] = None,
    ):
        super().__init__(
            RequiredProviders.Args(
                aws=aws,
                google=google,
                azurerm=azurerm,
            )
        )

    @schema_args
    class Args(SchemaArgs):
        """
        Aws provider support.
        """

        aws: Optional[RequiredProvider] = arg(default=None)

        """
        Google provider support.
        """
        google: Optional[RequiredProvider] = arg(default=None)

        """
        Azure provider support.
        """
        azurerm: Optional[RequiredProvider] = arg(default=None)


@schema
class Settings(Terraform):
    def __init__(
        self,
        *,
        required_providers: RequiredProviders,
        required_version: Optional[str] = None,
        backend: Optional[Union[Local, Remote, S3]] = None,
    ):
        super().__init__(
            args=Settings.Args(
                required_providers=required_providers,
                required_version=required_version,
                backend=backend,
            ),
        )

    @schema_args
    class Args(SchemaArgs):
        """
        Specifies all of the providers required by the current module, mapping each local provider
        name to a source address and a version constraint.
        """

        required_providers: RequiredProviders = arg()

        """
        The required_version setting accepts a version constraint string, which specifies
        which versions of Terraform can be used with your configuration.
        """
        required_version: Optional[str] = arg(default=None)

        """
        The local backend configuration block.
        """
        backend: Optional[Union[Local, Remote, S3]] = arg(default=None)
