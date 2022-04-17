# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from typing import Any

from flask_babel import lazy_gettext as _
from sqlalchemy import not_, or_
from sqlalchemy.orm.query import Query

from superset.connectors.sqla.models import SqlaTable
from superset.datasets.models import Dataset, table_association_table
from superset.tables.models import Table
from superset.views.base import BaseFilter


class DatasetIsNullOrEmptyFilter(BaseFilter):  # pylint: disable=too-few-public-methods
    name = _("Null or Empty")
    arg_name = "dataset_is_null_or_empty"

    def apply(self, query: Query, value: bool) -> Query:
        filter_clause = or_(SqlaTable.sql.is_(None), SqlaTable.sql == "")

        if not value:
            filter_clause = not_(filter_clause)

        return query.filter(filter_clause)


class DatasetIsPhysicalOrVirtual(BaseFilter):
    name = _("Null or Empty")
    arg_name = "dataset_is_null_or_empty"

    def apply(self, query: Query, value: bool) -> Query:
        filter_clause = Dataset.is_physical == True

        if not value:
            filter_clause = not_(filter_clause)

        return query.filter(filter_clause)


class DatasetAllTextFilter(BaseFilter):  # pylint: disable=too-few-public-methods
    name = _("All Text")
    arg_name = "dataset_all_text"

    def apply(self, query: Query, value: Any) -> Query:
        if not value:
            return query
        ilike_value = f"%{value}%"
        return query.filter(
            or_(
                Dataset.name.ilike(ilike_value),
                Dataset.expression.ilike((ilike_value)),
            )
        )


# example risom: (filters:!((col:tables,opr:schema,value:public)),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:25)
class DatasetSchemaFilter(BaseFilter):
    name = _("Schema")
    arg_name = "schema"

    def apply(self, query: Query, value: Any) -> Query:
        if not value:
            return query

        filter_clause = (
            (table_association_table.c.dataset_id == Dataset.id)
            & (table_association_table.c.table_id == Table.id)
            & (Table.schema == value)
        )
        return query.join(table_association_table).join(Table).filter(filter_clause)


class DatasetDatabaseFilter(BaseFilter):
    name = _("Database")
    arg_name = "db"

    def apply(self, query: Query, value: Any) -> Query:
        if not value:
            return query

        filter_clause = (
            (table_association_table.c.dataset_id == Dataset.id)
            & (table_association_table.c.table_id == Table.id)
            & (Table.database_id == value)
        )
        return query.join(table_association_table).join(Table).filter(filter_clause)
