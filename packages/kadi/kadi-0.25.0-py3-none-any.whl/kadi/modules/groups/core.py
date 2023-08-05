# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from elasticsearch_dsl import Q
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from .models import Group
from .models import GroupState
from .models import GroupVisibility
from .utils import delete_group_image
from kadi.ext.db import db
from kadi.lib.conversion import strip_markdown
from kadi.lib.db import update_object
from kadi.lib.permissions.core import add_role
from kadi.lib.permissions.core import delete_permissions
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.permissions.core import setup_permissions
from kadi.lib.resources.utils import search_resources
from kadi.lib.revisions.core import create_revision
from kadi.lib.revisions.core import delete_revisions
from kadi.lib.utils import signal_resource_change
from kadi.modules.groups.utils import get_user_groups


def create_group(
    *,
    identifier,
    title,
    creator=None,
    description="",
    visibility=GroupVisibility.PRIVATE,
    state=GroupState.ACTIVE,
):
    """Create a new group.

    This will also create all default permissions of the group.

    Note that this function issues a database commit or rollback.

    :param identifier: See :attr:`.Group.identifier`.
    :param title: See :attr:`.Group.title`.
    :param creator: (optional) The user that created the group. Defaults to the current
        user.
    :param description: (optional) See :attr:`.Group.description`.
    :param visibility: (optional) See :attr:`.Group.visibility`.
    :param state: (optional) See :attr:`.Group.state`.
    :return: The created group  or ``None`` if the group could not be created.
    """
    creator = creator if creator is not None else current_user

    group = Group.create(
        identifier=identifier,
        title=title,
        creator=creator,
        description=description,
        plain_description=strip_markdown(description),
        visibility=visibility,
        state=state,
    )

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return None

    setup_permissions("group", group.id)
    add_role(creator, "group", group.id, "admin")

    revision_created = create_revision(group, user=creator)
    db.session.commit()

    if revision_created:
        signal_resource_change(group, user=creator, created=True)

    return group


def update_group(group, **kwargs):
    r"""Update an existing group.

    Note that this function issues a database commit or rollback.

    :param group: The group to update.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`.
    :return: ``True`` if the group was updated successfully, ``False`` otherwise.
    """
    if group.state != GroupState.ACTIVE:
        return False

    if "description" in kwargs:
        kwargs["plain_description"] = strip_markdown(kwargs["description"])

    update_object(group, **kwargs)

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return False

    revision_created = create_revision(group)
    db.session.commit()

    if revision_created:
        signal_resource_change(group)

    return True


def delete_group(group):
    """Delete an existing group.

    This will perform a soft deletion, i.e. only the group's state will be changed.

    Note that this function issues a database commit.

    :param group: The group to delete.
    """
    revision_created = False

    if group.state == GroupState.ACTIVE:
        group.state = GroupState.DELETED
        revision_created = create_revision(group)

    db.session.commit()

    if revision_created:
        signal_resource_change(group)


def restore_group(group):
    """Restore a deleted group.

    Note that this function issues a database commit.

    :param group: The group to restore.
    """
    revision_created = False

    if group.state == GroupState.DELETED:
        group.state = GroupState.ACTIVE
        revision_created = create_revision(group)

    db.session.commit()

    if revision_created:
        signal_resource_change(group)


def purge_group(group):
    """Purge an existing group.

    This will completely delete the group from the database.

    :param group: The group to purge.
    """
    delete_group_image(group)

    delete_revisions(group)
    delete_permissions("group", group.id)

    db.session.delete(group)


def search_groups(
    query,
    sort="_score",
    visibility=False,
    users=None,
    member_only=False,
    page=1,
    per_page=10,
):
    """Search for and filter all groups that the current user can read.

    Uses :func:`kadi.lib.resources.utils.search_resources`.

    :param query: The search query as string to search for the title, identifier and
        plain description of the group.
    :param sort: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param visibility: (optional) A value to filter the visibility of the searched
        groups with.
    :param users: (optional) A list of user IDs the searched groups need to be created
        by. All given users are filtered using an *OR* operation.
    :param member_only: (optional) Flag indicating whether to exclude groups without
        membership.
    :param page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param per_page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :return: The search results as returned by
        :func:`kadi.lib.resources.utils.search_resources`.
    """
    groups_query = get_permitted_objects(current_user, "read", "group").filter(
        Group.state == GroupState.ACTIVE
    )

    if visibility in GroupVisibility.__values__:
        groups_query = groups_query.filter(Group.visibility == visibility)

    if users:
        groups_query = groups_query.filter(Group.user_id.in_(users))

    if member_only:
        groups_query = groups_query.intersect(get_user_groups(current_user))

    group_ids = [g.id for g in groups_query.with_entities(Group.id)]

    if query:
        base_query_params = {
            "query": query,
            "fields": [
                "identifier",
                "identifier.text",
                "title",
                "title.text",
                "plain_description",
            ],
        }

        exact_query = Q("multi_match", boost=5, **base_query_params)
        fuzzy_query = Q("multi_match", fuzziness="AUTO:2,6", **base_query_params)

        query = Q("bool", should=[exact_query, fuzzy_query])

    return search_resources(
        Group,
        query=query,
        sort=sort,
        filter_ids=group_ids,
        page=page,
        per_page=per_page,
    )
