from typing import Any

from ..enums import Dialects
from ..queries import Query, QueryBuilder


class OracleQuery(Query):
    """
    Defines a query class for use with Oracle.
    """

    @classmethod
    def _builder(cls, **kwargs: Any) -> "OracleQueryBuilder":
        return OracleQueryBuilder(**kwargs)


class OracleQueryBuilder(QueryBuilder):
    QUOTE_CHAR = '"'
    QUERY_CLS = OracleQuery
    ALIAS_QUOTE_CHAR = '"'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(dialect=Dialects.ORACLE, **kwargs)

    def get_sql(self, *args: Any, **kwargs: Any) -> str:
        # Oracle does not support group by a field alias
        # Note: set directly in kwargs as they are re-used down the tree in the case of subqueries!
        kwargs["groupby_alias"] = False
        return super().get_sql(*args, **kwargs)

    def _offset_sql(self, **kwargs) -> str:
        if self._offset is None:
            return ""
        return " OFFSET {offset} ROWS".format(offset=self._offset.get_sql(**kwargs))

    def _limit_sql(self, **kwargs) -> str:
        if self._limit is None:
            return ""
        return " FETCH NEXT {limit} ROWS ONLY".format(limit=self._limit.get_sql(**kwargs))
