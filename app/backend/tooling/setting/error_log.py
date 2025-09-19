# import
from logging import getLogger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError
from typing import Union, Iterable, Optional

# local import


# class
class Logs_Manager:

    # init
    def __init__(self):
        self.logger: object  = getLogger(__name__)
        self.error_hints: dict[str, str] = {
            "23505": "Unique constraint violated (duplicate value).",
            "23503": "Foreign key violation (referenced row missing or restricted).",
            "23502": "NOT NULL violation (a required column was NULL).",
            "23514": "CHECK constraint violated.",
        }
        self.diag_values: Iterable[str] = ("message_primary", "detail", "hint", "schema_name", "table_name", "column_name",
                            "constraint_name", "datatype_name")

    # helpers
    def _log_header(self, title: str, exc: Exception) -> None:
        self.logger.error(f'{title}: {str(exc)}')

    def _log_params(self, exc: Exception) -> None:
        param_book: dict[str, object] = {"statement": getattr(exc, "params", None),
                                         "params": getattr(exc, "params", None)}

        if param_book["statement"]:
            self.logger.error(f'Statement: {str(param_book["statement"])}')

        if param_book["params"]:
            self.logger.error(f'Params: {str(param_book["params"])}')

    def _dbapi_details(self, exc: Exception) -> None:
        # best possible extraction of DB-API details
        orig = getattr(exc, "orig", None)

        if not orig: return

        # psycopg attrs -> code/error
        psycopg_attrs: dict[str, object] = {"code": getattr(orig, "pgcode", None),
                                            "error": getattr(orig, "pgerror", None)}

        if psycopg_attrs["code"]:
            try:
                self.logger.error(f'PGERROR: {psycopg_attrs["error"].strip()}')
            except Exception:
                self.logger.error(f'PGERROR: {psycopg_attrs["error"]}')

        diag = getattr(orig, "diag", None)

        if diag:
            for field in self.diag_values:
                value = getattr(diag, field, None)

                if value:
                    self.logger.error(f'diag -> {field}: {value}')

    # public
    # SQLAlchemyError
    async def logger_sql_alchemy_error(
            self, exc: Union[SQLAlchemyError, Exception, str]) -> None:
        """
        Generic SQLAlchemyError logger
        :param exc: SQLAlchemyError or Exception
        :return: None
        """

        # header
        self._log_header(title="SQLAlchemyError", exc=exc)

        # statement / params and possible DB-API details
        self._log_params(exc=exc)
        self._dbapi_details(exc=exc)

    # OperationalError
    async def logger_sql_alchemy_operational_error(
            self, exc: Union[OperationalError, SQLAlchemyError, Exception]) -> None:
        """
        OperationalError logger (connection issues, timeouts, bad DNS, etc.)
        :param exc: OperationalError or SQLAlchemyError or Exception
        :return: None
        """

        # header
        self._log_header(title="OperationalError", exc=exc)

        # statement / params and possible DB-API details
        self._log_params(exc=exc)
        self._dbapi_details(exc=exc)

    # IntegrityError
    async def logger_sql_alchemy_integrity_error(self, exc: Exception) -> None:
        """
        IntegrityError logger (unique/foreign-key/not-null/check constraint violations)
        :param exc: Exception
        :return: None
        """

        # header
        self._log_header(title="IntegrityError", exc=exc)

        # statement / params and possible DB-API details
        if isinstance(exc, IntegrityError):
            self._log_params(exc=exc)
            self._dbapi_details(exc=exc)
        else:
            # non-integrity error
            self.logger.error('integrity_error_log_handler method called with non-IntegrityError exception type.')
