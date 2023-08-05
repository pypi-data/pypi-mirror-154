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
from flask import abort
from flask import current_app
from flask import render_template
from flask import request
from flask_babel import gettext as _
from flask_login import current_user

from .blueprint import bp
from kadi import __version__
from kadi.lib.config.core import get_sys_config
from kadi.lib.permissions.core import get_permitted_objects
from kadi.modules.collections.models import Collection
from kadi.modules.collections.models import CollectionState
from kadi.modules.collections.schemas import CollectionSchema
from kadi.modules.records.models import Record
from kadi.modules.records.models import RecordState
from kadi.modules.records.schemas import RecordSchema


@bp.get("/")
def index():
    """The index/home page.

    Will change depending on whether the current user is authenticated or not.
    """
    locales = list(current_app.config["LOCALES"].keys())
    preferred_locale = request.accept_languages.best_match(locales)

    if not current_user.is_authenticated:
        return render_template("main/index.html", preferred_locale=preferred_locale)

    records = (
        get_permitted_objects(current_user, "read", "record")
        .filter(Record.state == RecordState.ACTIVE)
        .order_by(Record.last_modified.desc())
        .limit(6)
    )
    collections = (
        get_permitted_objects(current_user, "read", "collection")
        .filter(Collection.state == CollectionState.ACTIVE)
        .order_by(Collection.last_modified.desc())
        .limit(4)
    )

    return render_template(
        "main/home.html",
        title=_("Home"),
        version=__version__,
        preferred_locale=preferred_locale,
        js_resources={
            "version": __version__,
            "records": RecordSchema(many=True, _internal=True).dump(records),
            "collections": CollectionSchema(many=True, _internal=True).dump(
                collections
            ),
        },
    )


@bp.get("/about")
def about():
    """The about page."""
    return render_template("main/about.html", title=_("About"), version=__version__)


@bp.get("/help")
def help():
    """The help page."""
    return render_template("main/help.html", title=_("Help"))


@bp.get("/terms-of-use")
def terms_of_use():
    """Page showing the terms of use, if configured."""
    config_item = "TERMS_OF_USE"

    if not get_sys_config(config_item):
        abort(404)

    return render_template(
        "main/legals.html",
        title=_("Terms of use"),
        endpoint="terms_of_use",
        config_item=config_item,
    )


@bp.get("/privacy-policy")
def privacy_policy():
    """Page showing the privacy policy, if configured."""
    config_item = "PRIVACY_POLICY"

    if not get_sys_config(config_item):
        abort(404)

    return render_template(
        "main/legals.html",
        title=_("Privacy policy"),
        endpoint="privacy_policy",
        config_item=config_item,
    )


@bp.get("/legal-notice")
def legal_notice():
    """Page showing the legal notice, if configured."""
    config_item = "LEGAL_NOTICE"

    if not get_sys_config(config_item):
        abort(404)

    return render_template(
        "main/legals.html",
        title=_("Legal notice"),
        endpoint="legal_notice",
        config_item=config_item,
    )
