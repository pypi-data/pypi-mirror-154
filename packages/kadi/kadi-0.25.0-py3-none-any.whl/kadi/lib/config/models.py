# Copyright 2021 Karlsruhe Institute of Technology
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
from sqlalchemy.dialects.postgresql import JSONB

from kadi.ext.db import db
from kadi.lib.db import composite_index
from kadi.lib.db import SimpleTimestampMixin
from kadi.lib.utils import SimpleReprMixin


class ConfigItem(SimpleReprMixin, SimpleTimestampMixin, db.Model):
    """Model to store global or user-specific config items."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "key", "user_id"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "config_item"

    __table_args__ = (composite_index("key", "user_id"),)

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the config item, auto incremented."""

    key = db.Column(db.Text, nullable=False)
    """The key of the config item."""

    value = db.Column(JSONB, nullable=True)
    """The value of the config item."""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    """The optional ID of the user the config item belongs to.

    If not set, the config item is global. Currently still unused.
    """

    @classmethod
    def create(cls, *, key, value):
        """Create a new config item and add it to the database session.

        :param key: The key of the config item.
        :param value: The value of the config item, which needs to be JSON serializable.
        :return: The new :class:`.ConfigItem` object.
        """
        config_item = cls(key=key, value=value)

        db.session.add(config_item)
        return config_item

    @classmethod
    def update_or_create(cls, *, key, value):
        """Update an existing config item or create one if it does not exist yet.

        See :meth:`create` for an explanation of the parameters.

        :return: The new or updated :class:`.ConfigItem` object.
        """
        config_item = cls.query.filter_by(key=key).first()

        if not config_item:
            config_item = cls.create(key=key, value=value)
        else:
            config_item.value = value

        return config_item
