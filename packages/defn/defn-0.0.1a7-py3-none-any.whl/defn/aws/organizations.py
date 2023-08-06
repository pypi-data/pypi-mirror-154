from cdktf import Fn
from cdktf_cdktf_provider_aws import (
    DataAwsIdentitystoreGroup,
    DataAwsIdentitystoreGroupFilter,
)
from cdktf_cdktf_provider_aws.organizations import (
    OrganizationsAccount,
    OrganizationsOrganization,
)
from cdktf_cdktf_provider_aws.ssoadmin import (
    DataAwsSsoadminInstances,
    SsoadminAccountAssignment,
)

import defn.aws.sso


""" Creates Organizations, Accounts, and Administrator permission set """


def account(
    self,
    prefix: str,
    org: str,
    domain: str,
    acct: str,
    identitystore_group,
    sso_permission_set_admin,
):
    """Create the organization account."""
    if acct == org:
        # The master organization account can't set
        # iam_user_access_to_billing, role_name
        organizations_account = OrganizationsAccount(
            self,
            acct,
            name=acct,
            email=f"{prefix}{org}@{domain}",
            tags={"ManagedBy": "Terraform"},
        )
    else:
        # Organization account
        organizations_account = OrganizationsAccount(
            self,
            acct,
            name=acct,
            email=f"{prefix}{org}+{acct}@{domain}",
            iam_user_access_to_billing="ALLOW",
            role_name="OrganizationAccountAccessRole",
            tags={"ManagedBy": "Terraform"},
        )

    # Organization accounts grant Administrator permission set to the Administrator group
    SsoadminAccountAssignment(
        self,
        f"{acct}_admin_sso_account_assignment",
        instance_arn=sso_permission_set_admin.instance_arn,
        permission_set_arn=sso_permission_set_admin.arn,
        principal_id=identitystore_group.group_id,
        principal_type="GROUP",
        target_id=organizations_account.id,
        target_type="AWS_ACCOUNT",
    )


def organization(self, prefix: str, org: str, domain: str, accounts: list):
    """The organization must be imported."""
    OrganizationsOrganization(
        self,
        "organization",
        feature_set="ALL",
        enabled_policy_types=["SERVICE_CONTROL_POLICY", "TAG_POLICY"],
        aws_service_access_principals=[
            "cloudtrail.amazonaws.com",
            "config.amazonaws.com",
            "ram.amazonaws.com",
            "ssm.amazonaws.com",
            "sso.amazonaws.com",
            "tagpolicies.tag.amazonaws.com",
        ],
    )

    # Lookup pre-enabled AWS SSO instance
    ssoadmin_instances = DataAwsSsoadminInstances(self, "sso_instance")

    # Administrator SSO permission set with AdministratorAccess policy
    sso_permission_set_admin = defn.aws.sso.administrator(self, ssoadmin_instances)

    # Lookup pre-created Administrators group
    f = DataAwsIdentitystoreGroupFilter(
        attribute_path="DisplayName", attribute_value="Administrators"
    )
    identitystore_group = DataAwsIdentitystoreGroup(
        self,
        "administrators_sso_group",
        identity_store_id=Fn.element(ssoadmin_instances.identity_store_ids, 0),
        filter=[f],
    )

    # The master account (named "org") must be imported.
    for acct in accounts:
        account(
            self,
            prefix,
            org,
            domain,
            acct,
            identitystore_group,
            sso_permission_set_admin,
        )
