#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Query parser implementation
"""

import datetime
import traceback
from typing import Optional

from sql_metadata import Parser

from metadata.config.common import ConfigModel
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.ingestion.api.processor import Processor, ProcessorStatus
from metadata.ingestion.models.table_queries import QueryParserData, TableQuery
from metadata.utils.logger import ingestion_logger


class QueryParserProcessorConfig(ConfigModel):
    """
    Query parser pydantic configuration model
    """

    filter: Optional[str] = None


logger = ingestion_logger()


class QueryParserProcessor(Processor):
    """
    Extension of the `Processor` class

    Args:
        config (QueryParserProcessorConfig):
        metadata_config (MetadataServerConfig):

    Attributes:
        config (QueryParserProcessorConfig):
        metadata_config (MetadataServerConfig):
        status (ProcessorStatus):
    """

    config: QueryParserProcessorConfig
    status: ProcessorStatus

    def __init__(
        self,
        config: QueryParserProcessorConfig,
        metadata_config: OpenMetadataConnection,
    ):

        self.config = config
        self.metadata_config = metadata_config
        self.status = ProcessorStatus()

    @classmethod
    def create(
        cls, config_dict: dict, metadata_config: OpenMetadataConnection, **kwargs
    ):
        config = QueryParserProcessorConfig.parse_obj(config_dict)
        return cls(config, metadata_config)

    def process(self, record: TableQuery) -> QueryParserData:
        try:
            start_date = record.analysis_date
            if isinstance(record.analysis_date, str):
                start_date = datetime.datetime.strptime(
                    str(record.analysis_date), "%Y-%m-%d %H:%M:%S"
                ).date()
            parser = Parser(record.sql)
            columns_dict = {} if parser.columns_dict is None else parser.columns_dict
            query_parser_data = QueryParserData(
                tables=parser.tables,
                tables_aliases=parser.tables_aliases,
                columns=columns_dict,
                database=record.database,
                sql=record.sql,
                date=start_date.strftime("%Y-%m-%d"),
                service_name=record.service_name,
            )
        # pylint: disable=broad-except
        except Exception as err:
            if hasattr(record, "sql"):
                logger.debug(record.sql)
            logger.debug(traceback.format_exc())
            logger.error(err)
            query_parser_data = None

        return query_parser_data

    def close(self):
        pass

    def get_status(self) -> ProcessorStatus:
        return self.status
