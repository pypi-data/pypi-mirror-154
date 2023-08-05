from arpeggio.cleanpeg import NOT, prefix
from pulumi.resource import ResourceOptions
import jsons
import pulumi_aws.rds as rds
import pulumi_aws_native.rds as rds_native

def Instance(stem, props, username=None, password=None, instance_class=None, apply_immediately=None, snetgrp_name=None, secgrp_ids=None, optgrp_name=None, provider=None, parent=None, depends_on=None):
    db_instance = rds.Instance(
        f'rds-{stem}',
        # name='db-{stem}',
        identifier=f'rds-{stem}',
        instance_class=instance_class,
        engine='sqlserver-se',
        engine_version="15.00.4073.23.v1",
        apply_immediately=apply_immediately,
        username=username,
        password=password,
        storage_type='io1',
        iops=3000,
        allocated_storage=1500,
        max_allocated_storage=2000,
        # iam_database_authentication_enabled="true",
        publicly_accessible="true",
        license_model="license-included",
        skip_final_snapshot="True",
        performance_insights_enabled="True",
        vpc_security_group_ids=secgrp_ids,
        db_subnet_group_name=snetgrp_name,
        option_group_name=optgrp_name,
        tags=props.base_tags,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return db_instance

def SubnetGroup(stem, props, snet_ids=None, provider=None, parent=None, depends_on=None):
    sn_grp =rds.SubnetGroup(
        f'sngrp-{stem}',
        name=f'sngrp-{stem}',
        subnet_ids=snet_ids,
        tags=props.base_tags,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return sn_grp

def OptionGroup(stem, props, provider=None, parent=None, depends_on=None):
    db_instance = rds.OptionGroup(
        f'optgrp-{stem}',
        name=f'optgrp-{stem}',
        option_group_description="Option Group",
        engine_name="sqlserver-se",
        major_engine_version="15.00",
        options=[
            rds.OptionGroupOptionArgs(
                option_name="SQLSERVER_BACKUP_RESTORE",
                option_settings=[rds.OptionGroupOptionOptionSettingArgs(
                    name="IAM_ROLE_ARN",
                    value="arn:aws:iam::917340184633:role/service-role/SET-SQL-BACKUP-RESTORE",
                )],
            )
        ],
        tags=props.base_tags,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return db_instance