'''
[![npm version](https://badge.fury.io/js/cdk-github.svg)](https://badge.fury.io/js/cdk-github)
[![PyPI version](https://badge.fury.io/py/cdk-github.svg)](https://badge.fury.io/py/cdk-github)
[![release](https://github.com/wtfjoke/cdk-github/actions/workflows/release.yml/badge.svg)](https://github.com/wtfjoke/cdk-github/actions/workflows/release.yml)
![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

# CDK-GitHub

[AWS CDK](https://aws.amazon.com/cdk/) v2 L3 constructs for GitHub.

This project aims to make GitHub's API accessible through CDK with various helper constructs to create resources in GitHub.
The target is to replicate most of the functionality of the [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest/docs).

Internally [AWS CloudFormation custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) will be used to track GitHub resources (such as Secrets).

# Installation

JavaScript/TypeScript:
`npm install cdk-github`

Python:
`pip install cdk-github`

# Constructs

This library provides the following constructs:

* [ActionSecret](API.md#actionsecret-a-nameactionsecret-idcdk-githubactionsecreta) - Creates a [GitHub Action (repository) secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) from a given AWS Secrets Manager secret.
* [ActionEnvironmentSecret](API.md#actionenvironmentsecret-a-nameactionenvironmentsecret-idcdk-githubactionenvironmentsecreta) - Creates a [GitHub Action environment secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-an-environment) from a given AWS Secrets Manager secret.

# Authentication

Currently the constructs only support authentication via a [GitHub Personal Access Token](https://github.com/settings/tokens/new). The token needs to be a stored in a AWS SecretsManager Secret and passed to the construct as parameter.

# Examples

## ActionSecret

### TypeScript

```python
import { ActionSecret } from 'cdk-github';

export class ActionSecretStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const sourceSecret = Secret.fromSecretNameV2(this, 'secretToStoreInGitHub', 'testcdkgithub');
    const githubTokenSecret = Secret.fromSecretNameV2(this, 'ghSecret', 'GITHUB_TOKEN');

    new ActionSecret(this, 'GitHubActionSecret', {
      githubTokenSecret,
      repositoryName: 'cdk-github',
      repositoryOwner: 'wtfjoke',
      repositorySecretName: 'aRandomGitHubSecret',
      sourceSecret,
    });
  }
}
```

See full example in [ActionSecretStack](src/examples/action-secret/action-secret-stack.ts)

### Python

```python
import cdkgithub

class ActionSecretStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_secret = sm.Secret.from_secret_name_v2(
            self, "secretToStoreInGitHub", "testcdkgithub"
        )
        github_token_secret = sm.Secret.from_secret_name_v2(
            self, "ghSecret", "GITHUB_TOKEN"
        )
        cdkgithub.ActionSecret(
            self,
            "GitHubActionSecret",
            github_token_secret=github_token_secret,
            repository_name="cdk-github",
            repository_owner="wtfjoke",
            repository_secret_name="aRandomPythonGitHubSecret",
            source_secret=source_secret,
        )
```

## ActionEnvironmentSecret

```python
import { ActionEnvironmentSecret } from 'cdk-github';

export class ActionEnvironmentSecretStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const sourceSecret = Secret.fromSecretNameV2(this, 'secretToStoreInGitHub', 'testcdkgithub');
    const githubTokenSecret = Secret.fromSecretNameV2(this, 'ghSecret', 'GITHUB_TOKEN');

    new ActionEnvironmentSecret(this, 'GitHubActionEnvironmentSecret', {
      githubTokenSecret,
      environment: 'dev',
      repositoryName: 'cdk-github',
      repositoryOwner: 'wtfjoke',
      repositorySecretName: 'aRandomGitHubSecret',
      sourceSecret,
    });
  }
}
```

See full example in [ActionEnvironmentSecretStack](src/examples/action-environment-secret/action-environment-secret-stack.ts)
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

import aws_cdk.aws_secretsmanager
import constructs


class ActionEnvironmentSecret(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github.ActionEnvironmentSecret",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        environment: builtins.str,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_name: builtins.str,
        repository_owner: builtins.str,
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param environment: The GithHub environment which the secret should be stored in.
        :param github_token_secret: The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository_name: The GitHub repository name.
        :param repository_owner: The GitHub repository owner.
        :param repository_secret_name: The GitHub secret name to be stored.
        :param source_secret: The AWS secret which should be stored as a GitHub as a secret.
        '''
        props = ActionEnvironmentSecretProps(
            environment=environment,
            github_token_secret=github_token_secret,
            repository_name=repository_name,
            repository_owner=repository_owner,
            repository_secret_name=repository_secret_name,
            source_secret=source_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-github.ActionEnvironmentSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "environment": "environment",
        "github_token_secret": "githubTokenSecret",
        "repository_name": "repositoryName",
        "repository_owner": "repositoryOwner",
        "repository_secret_name": "repositorySecretName",
        "source_secret": "sourceSecret",
    },
)
class ActionEnvironmentSecretProps:
    def __init__(
        self,
        *,
        environment: builtins.str,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_name: builtins.str,
        repository_owner: builtins.str,
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param environment: The GithHub environment which the secret should be stored in.
        :param github_token_secret: The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository_name: The GitHub repository name.
        :param repository_owner: The GitHub repository owner.
        :param repository_secret_name: The GitHub secret name to be stored.
        :param source_secret: The AWS secret which should be stored as a GitHub as a secret.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "environment": environment,
            "github_token_secret": github_token_secret,
            "repository_name": repository_name,
            "repository_owner": repository_owner,
            "repository_secret_name": repository_secret_name,
            "source_secret": source_secret,
        }

    @builtins.property
    def environment(self) -> builtins.str:
        '''The GithHub environment which the secret should be stored in.'''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def github_token_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''The AWS secret in which the OAuth GitHub (personal) access token is stored.'''
        result = self._values.get("github_token_secret")
        assert result is not None, "Required property 'github_token_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''The GitHub repository name.'''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_owner(self) -> builtins.str:
        '''The GitHub repository owner.'''
        result = self._values.get("repository_owner")
        assert result is not None, "Required property 'repository_owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_secret_name(self) -> builtins.str:
        '''The GitHub secret name to be stored.'''
        result = self._values.get("repository_secret_name")
        assert result is not None, "Required property 'repository_secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''The AWS secret which should be stored as a GitHub as a secret.'''
        result = self._values.get("source_secret")
        assert result is not None, "Required property 'source_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionEnvironmentSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionSecret(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github.ActionSecret",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_name: builtins.str,
        repository_owner: builtins.str,
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param github_token_secret: The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository_name: The GitHub repository name.
        :param repository_owner: The GitHub repository owner.
        :param repository_secret_name: The GitHub secret name to be stored.
        :param source_secret: The AWS secret which should be stored as a GitHub as a secret.
        '''
        props = ActionSecretProps(
            github_token_secret=github_token_secret,
            repository_name=repository_name,
            repository_owner=repository_owner,
            repository_secret_name=repository_secret_name,
            source_secret=source_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-github.ActionSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "github_token_secret": "githubTokenSecret",
        "repository_name": "repositoryName",
        "repository_owner": "repositoryOwner",
        "repository_secret_name": "repositorySecretName",
        "source_secret": "sourceSecret",
    },
)
class ActionSecretProps:
    def __init__(
        self,
        *,
        github_token_secret: aws_cdk.aws_secretsmanager.ISecret,
        repository_name: builtins.str,
        repository_owner: builtins.str,
        repository_secret_name: builtins.str,
        source_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param github_token_secret: The AWS secret in which the OAuth GitHub (personal) access token is stored.
        :param repository_name: The GitHub repository name.
        :param repository_owner: The GitHub repository owner.
        :param repository_secret_name: The GitHub secret name to be stored.
        :param source_secret: The AWS secret which should be stored as a GitHub as a secret.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "github_token_secret": github_token_secret,
            "repository_name": repository_name,
            "repository_owner": repository_owner,
            "repository_secret_name": repository_secret_name,
            "source_secret": source_secret,
        }

    @builtins.property
    def github_token_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''The AWS secret in which the OAuth GitHub (personal) access token is stored.'''
        result = self._values.get("github_token_secret")
        assert result is not None, "Required property 'github_token_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''The GitHub repository name.'''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_owner(self) -> builtins.str:
        '''The GitHub repository owner.'''
        result = self._values.get("repository_owner")
        assert result is not None, "Required property 'repository_owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_secret_name(self) -> builtins.str:
        '''The GitHub secret name to be stored.'''
        result = self._values.get("repository_secret_name")
        assert result is not None, "Required property 'repository_secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''The AWS secret which should be stored as a GitHub as a secret.'''
        result = self._values.get("source_secret")
        assert result is not None, "Required property 'source_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ActionEnvironmentSecret",
    "ActionEnvironmentSecretProps",
    "ActionSecret",
    "ActionSecretProps",
]

publication.publish()
