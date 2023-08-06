import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.group import Group
from ..models.name_and_uuid import NameAndUuid
from ..models.notification_severity import NotificationSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="PagerDutyProfile")


@attr.s(auto_attribs=True)
class PagerDutyProfile:
    """A PagerDutyProfile contains user-specific configuration on how to notify
    PagerDuty of events.

        Attributes:
            name (str):
            integration_key (str):
            url (Union[Unset, str]):
            uuid (Union[Unset, str]):
            description (Union[Unset, str]):
            dashboard_url (Union[Unset, str]):
            default_event_severity (Union[Unset, NotificationSeverity]):
            default_event_component_template (Union[Unset, str]):
            default_event_group_template (Union[Unset, str]):
            default_event_class_template (Union[Unset, str]):
            created_by_user (Union[Unset, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
            created_by_group (Union[Unset, Group]):
            run_environment (Union[Unset, None, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
                URL.
                When used to identify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
    """

    name: str
    integration_key: str
    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    default_event_severity: Union[Unset, NotificationSeverity] = UNSET
    default_event_component_template: Union[Unset, str] = UNSET
    default_event_group_template: Union[Unset, str] = UNSET
    default_event_class_template: Union[Unset, str] = UNSET
    created_by_user: Union[Unset, str] = UNSET
    created_by_group: Union[Unset, Group] = UNSET
    run_environment: Union[Unset, None, NameAndUuid] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        integration_key = self.integration_key
        url = self.url
        uuid = self.uuid
        description = self.description
        dashboard_url = self.dashboard_url
        default_event_severity: Union[Unset, str] = UNSET
        if not isinstance(self.default_event_severity, Unset):
            default_event_severity = self.default_event_severity.value

        default_event_component_template = self.default_event_component_template
        default_event_group_template = self.default_event_group_template
        default_event_class_template = self.default_event_class_template
        created_by_user = self.created_by_user
        created_by_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.created_by_group, Unset):
            created_by_group = self.created_by_group.to_dict()

        run_environment: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.run_environment, Unset):
            run_environment = self.run_environment.to_dict() if self.run_environment else None

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "integration_key": integration_key,
            }
        )
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if description is not UNSET:
            field_dict["description"] = description
        if dashboard_url is not UNSET:
            field_dict["dashboard_url"] = dashboard_url
        if default_event_severity is not UNSET:
            field_dict["default_event_severity"] = default_event_severity
        if default_event_component_template is not UNSET:
            field_dict["default_event_component_template"] = default_event_component_template
        if default_event_group_template is not UNSET:
            field_dict["default_event_group_template"] = default_event_group_template
        if default_event_class_template is not UNSET:
            field_dict["default_event_class_template"] = default_event_class_template
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if created_by_group is not UNSET:
            field_dict["created_by_group"] = created_by_group
        if run_environment is not UNSET:
            field_dict["run_environment"] = run_environment
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        integration_key = d.pop("integration_key")

        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        description = d.pop("description", UNSET)

        dashboard_url = d.pop("dashboard_url", UNSET)

        _default_event_severity = d.pop("default_event_severity", UNSET)
        default_event_severity: Union[Unset, NotificationSeverity]
        if isinstance(_default_event_severity, Unset):
            default_event_severity = UNSET
        else:
            default_event_severity = NotificationSeverity(_default_event_severity)

        default_event_component_template = d.pop("default_event_component_template", UNSET)

        default_event_group_template = d.pop("default_event_group_template", UNSET)

        default_event_class_template = d.pop("default_event_class_template", UNSET)

        created_by_user = d.pop("created_by_user", UNSET)

        _created_by_group = d.pop("created_by_group", UNSET)
        created_by_group: Union[Unset, Group]
        if isinstance(_created_by_group, Unset):
            created_by_group = UNSET
        else:
            created_by_group = Group.from_dict(_created_by_group)

        _run_environment = d.pop("run_environment", UNSET)
        run_environment: Union[Unset, None, NameAndUuid]
        if _run_environment is None:
            run_environment = None
        elif isinstance(_run_environment, Unset):
            run_environment = UNSET
        else:
            run_environment = NameAndUuid.from_dict(_run_environment)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        pager_duty_profile = cls(
            name=name,
            integration_key=integration_key,
            url=url,
            uuid=uuid,
            description=description,
            dashboard_url=dashboard_url,
            default_event_severity=default_event_severity,
            default_event_component_template=default_event_component_template,
            default_event_group_template=default_event_group_template,
            default_event_class_template=default_event_class_template,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
            run_environment=run_environment,
            created_at=created_at,
            updated_at=updated_at,
        )

        pager_duty_profile.additional_properties = d
        return pager_duty_profile

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
